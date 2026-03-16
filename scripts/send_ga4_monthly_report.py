#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import os
import smtplib
import ssl
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List
from zoneinfo import ZoneInfo

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    matplotlib = None
    plt = None

try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Filter,
        FilterExpression,
        Metric,
        OrderBy,
        RunReportRequest,
    )
    from google.oauth2.service_account import Credentials
except ImportError:
    BetaAnalyticsDataClient = None
    DateRange = Dimension = Filter = FilterExpression = Metric = OrderBy = RunReportRequest = Credentials = None


GA_READONLY_SCOPE = "https://www.googleapis.com/auth/analytics.readonly"
DEFAULT_TIMEZONE = "Asia/Kolkata"
DEFAULT_WINDOW_DAYS = 30


@dataclass
class ReportConfig:
    output_dir: Path
    sample_data: bool
    skip_email: bool
    timezone_name: str
    window_days: int
    site_name: str
    property_id: str
    service_account_json: str
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_use_ssl: bool
    email_from: str
    email_to: List[str]


@dataclass
class ReportingPeriod:
    generated_at: datetime
    start_date: date
    end_date: date
    previous_start_date: date
    previous_end_date: date

    @property
    def label(self) -> str:
        return f"{self.start_date:%b %d, %Y} - {self.end_date:%b %d, %Y}"

    @property
    def previous_label(self) -> str:
        return f"{self.previous_start_date:%b %d, %Y} - {self.previous_end_date:%b %d, %Y}"


class ConfigError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a monthly GA4 visitor report with charts and email it."
    )
    parser.add_argument(
        "--output-dir",
        default=os.getenv("GA4_REPORT_OUTPUT_DIR", ".analytics-reports/monthly"),
        help="Directory where HTML, JSON, and chart images will be written.",
    )
    parser.add_argument(
        "--sample-data",
        action="store_true",
        help="Use synthetic data instead of calling the Google Analytics Data API.",
    )
    parser.add_argument(
        "--skip-email",
        action="store_true",
        help="Generate artifacts but do not send the email.",
    )
    parser.add_argument(
        "--timezone",
        default=os.getenv("REPORT_TIMEZONE", DEFAULT_TIMEZONE),
        help="IANA timezone name used for the reporting window.",
    )
    parser.add_argument(
        "--window-days",
        type=int,
        default=int(os.getenv("REPORT_WINDOW_DAYS", DEFAULT_WINDOW_DAYS)),
        help="Rolling window size in days. The report ends on the previous day in the configured timezone.",
    )
    parser.add_argument(
        "--site-name",
        default=os.getenv("REPORT_SITE_NAME", "Rajeev Jain website"),
        help="Display name used in the email subject and report header.",
    )
    return parser.parse_args()


def parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def split_csv(value: str | None) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def build_config(args: argparse.Namespace) -> ReportConfig:
    smtp_port_raw = os.getenv("SMTP_PORT") or "587"
    try:
        smtp_port = int(smtp_port_raw)
    except ValueError as exc:
        raise ConfigError(f"SMTP_PORT must be an integer, got {smtp_port_raw!r}") from exc

    config = ReportConfig(
        output_dir=Path(args.output_dir),
        sample_data=args.sample_data,
        skip_email=args.skip_email,
        timezone_name=args.timezone,
        window_days=args.window_days,
        site_name=args.site_name,
        property_id=os.getenv("GA4_PROPERTY_ID", "").strip(),
        service_account_json=os.getenv("GA4_SERVICE_ACCOUNT_JSON", "").strip(),
        smtp_host=os.getenv("SMTP_HOST", "").strip(),
        smtp_port=smtp_port,
        smtp_username=os.getenv("SMTP_USERNAME", "").strip(),
        smtp_password=os.getenv("SMTP_PASSWORD", "").strip(),
        smtp_use_ssl=parse_bool(os.getenv("SMTP_USE_SSL"), default=False),
        email_from=os.getenv("EMAIL_FROM", "").strip(),
        email_to=split_csv(os.getenv("EMAIL_TO")),
    )

    if config.window_days <= 0:
        raise ConfigError("REPORT_WINDOW_DAYS must be a positive integer.")

    if plt is None:
        raise ConfigError(
            "matplotlib is not installed. Run pip install -r scripts/analytics_requirements.txt."
        )

    if not config.sample_data:
        missing = []
        if not config.property_id:
            missing.append("GA4_PROPERTY_ID")
        if not config.service_account_json:
            missing.append("GA4_SERVICE_ACCOUNT_JSON")
        if missing:
            raise ConfigError("Missing GA4 configuration: " + ", ".join(missing))
        if BetaAnalyticsDataClient is None:
            raise ConfigError(
                "The Google Analytics dependencies are not installed. "
                "Run pip install -r scripts/analytics_requirements.txt."
            )

    if not config.skip_email:
        missing = []
        if not config.smtp_host:
            missing.append("SMTP_HOST")
        if not config.email_from:
            missing.append("EMAIL_FROM")
        if not config.email_to:
            missing.append("EMAIL_TO")
        if (config.smtp_username and not config.smtp_password) or (
            config.smtp_password and not config.smtp_username
        ):
            raise ConfigError(
                "SMTP_USERNAME and SMTP_PASSWORD must either both be set or both be empty."
            )
        if missing:
            raise ConfigError("Missing email configuration: " + ", ".join(missing))

    return config


def compute_reporting_period(timezone_name: str, window_days: int) -> ReportingPeriod:
    local_now = datetime.now(timezone.utc).astimezone(ZoneInfo(timezone_name))
    end_date = local_now.date() - timedelta(days=1)
    start_date = end_date - timedelta(days=window_days - 1)
    previous_end_date = start_date - timedelta(days=1)
    previous_start_date = previous_end_date - timedelta(days=window_days - 1)
    return ReportingPeriod(
        generated_at=local_now,
        start_date=start_date,
        end_date=end_date,
        previous_start_date=previous_start_date,
        previous_end_date=previous_end_date,
    )


def create_client(service_account_json: str):
    credentials_info = json.loads(service_account_json)
    credentials = Credentials.from_service_account_info(
        credentials_info, scopes=[GA_READONLY_SCOPE]
    )
    return BetaAnalyticsDataClient(credentials=credentials)


def parse_metric_value(raw: str) -> int | float | str:
    try:
        if "." in raw:
            return float(raw)
        return int(raw)
    except (TypeError, ValueError):
        return raw


def metric_order_by(metric_name: str) -> List[Any]:
    return [OrderBy(metric=OrderBy.MetricOrderBy(metric_name=metric_name), desc=True)]


def event_name_filter(event_names: Iterable[str]) -> Any:
    return FilterExpression(
        filter=Filter(
            field_name="eventName",
            in_list_filter=Filter.InListFilter(values=list(event_names)),
        )
    )


def run_report(
    client: Any,
    property_id: str,
    start_date: date,
    end_date: date,
    dimensions: List[str],
    metrics: List[str],
    *,
    limit: int = 10,
    order_bys: List[Any] | None = None,
    dimension_filter: Any | None = None,
) -> List[Dict[str, Any]]:
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[
            DateRange(start_date=start_date.isoformat(), end_date=end_date.isoformat())
        ],
        dimensions=[Dimension(name=name) for name in dimensions],
        metrics=[Metric(name=name) for name in metrics],
        limit=limit,
        order_bys=order_bys or [],
        dimension_filter=dimension_filter,
    )
    response = client.run_report(request)
    rows: List[Dict[str, Any]] = []
    for row in response.rows:
        parsed: Dict[str, Any] = {}
        for index, name in enumerate(dimensions):
            parsed[name] = row.dimension_values[index].value
        for index, name in enumerate(metrics):
            parsed[name] = parse_metric_value(row.metric_values[index].value)
        rows.append(parsed)
    return rows


def safe_report(
    warnings: List[str],
    label: str,
    fn: Callable[[], List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    try:
        return fn()
    except Exception as exc:
        warnings.append(f"{label}: {exc}")
        return []


def fetch_live_report(config: ReportConfig, period: ReportingPeriod) -> Dict[str, Any]:
    client = create_client(config.service_account_json)
    warnings: List[str] = []

    overview_metrics = [
        "totalUsers",
        "activeUsers",
        "newUsers",
        "sessions",
        "engagedSessions",
        "screenPageViews",
        "averageSessionDuration",
    ]

    overview_current = safe_report(
        warnings,
        "overview_current",
        lambda: run_report(
            client,
            config.property_id,
            period.start_date,
            period.end_date,
            [],
            overview_metrics,
            limit=1,
        ),
    )
    overview_previous = safe_report(
        warnings,
        "overview_previous",
        lambda: run_report(
            client,
            config.property_id,
            period.previous_start_date,
            period.previous_end_date,
            [],
            overview_metrics,
            limit=1,
        ),
    )

    pdf_filter = event_name_filter(["resume_pdf_click", "cv_pdf_click", "pdf_link_click"])
    pdf_clicks_current = safe_report(
        warnings,
        "pdf_clicks_current",
        lambda: run_report(
            client,
            config.property_id,
            period.start_date,
            period.end_date,
            ["eventName"],
            ["eventCount"],
            limit=10,
            order_bys=metric_order_by("eventCount"),
            dimension_filter=pdf_filter,
        ),
    )
    pdf_clicks_previous = safe_report(
        warnings,
        "pdf_clicks_previous",
        lambda: run_report(
            client,
            config.property_id,
            period.previous_start_date,
            period.previous_end_date,
            ["eventName"],
            ["eventCount"],
            limit=10,
            order_bys=metric_order_by("eventCount"),
            dimension_filter=pdf_filter,
        ),
    )

    sections = {
        "channels": safe_report(
            warnings,
            "channels",
            lambda: run_report(
                client,
                config.property_id,
                period.start_date,
                period.end_date,
                ["sessionDefaultChannelGroup"],
                ["sessions"],
                order_bys=metric_order_by("sessions"),
            ),
        ),
        "sources": safe_report(
            warnings,
            "sources",
            lambda: run_report(
                client,
                config.property_id,
                period.start_date,
                period.end_date,
                ["sessionSourceMedium"],
                ["sessions"],
                order_bys=metric_order_by("sessions"),
            ),
        ),
        "landing_pages": safe_report(
            warnings,
            "landing_pages",
            lambda: run_report(
                client,
                config.property_id,
                period.start_date,
                period.end_date,
                ["landingPagePlusQueryString"],
                ["sessions"],
                order_bys=metric_order_by("sessions"),
            ),
        ),
        "pages": safe_report(
            warnings,
            "pages",
            lambda: run_report(
                client,
                config.property_id,
                period.start_date,
                period.end_date,
                ["pagePathPlusQueryString"],
                ["screenPageViews"],
                order_bys=metric_order_by("screenPageViews"),
            ),
        ),
        "countries": safe_report(
            warnings,
            "countries",
            lambda: run_report(
                client,
                config.property_id,
                period.start_date,
                period.end_date,
                ["country"],
                ["activeUsers"],
                order_bys=metric_order_by("activeUsers"),
            ),
        ),
        "cities": safe_report(
            warnings,
            "cities",
            lambda: run_report(
                client,
                config.property_id,
                period.start_date,
                period.end_date,
                ["city", "country"],
                ["activeUsers"],
                order_bys=metric_order_by("activeUsers"),
            ),
        ),
        "languages": safe_report(
            warnings,
            "languages",
            lambda: run_report(
                client,
                config.property_id,
                period.start_date,
                period.end_date,
                ["language"],
                ["activeUsers"],
                order_bys=metric_order_by("activeUsers"),
            ),
        ),
        "devices": safe_report(
            warnings,
            "devices",
            lambda: run_report(
                client,
                config.property_id,
                period.start_date,
                period.end_date,
                ["deviceCategory"],
                ["activeUsers"],
                order_bys=metric_order_by("activeUsers"),
            ),
        ),
        "browsers": safe_report(
            warnings,
            "browsers",
            lambda: run_report(
                client,
                config.property_id,
                period.start_date,
                period.end_date,
                ["browser"],
                ["activeUsers"],
                order_bys=metric_order_by("activeUsers"),
            ),
        ),
        "operating_systems": safe_report(
            warnings,
            "operating_systems",
            lambda: run_report(
                client,
                config.property_id,
                period.start_date,
                period.end_date,
                ["operatingSystem"],
                ["activeUsers"],
                order_bys=metric_order_by("activeUsers"),
            ),
        ),
    }

    return {
        "warnings": warnings,
        "overview_current": overview_current[0] if overview_current else {},
        "overview_previous": overview_previous[0] if overview_previous else {},
        "pdf_clicks_current": pdf_clicks_current,
        "pdf_clicks_previous": pdf_clicks_previous,
        "sections": sections,
    }


def sample_rows(
    items: Iterable[tuple[str, int]], dimension_name: str, metric_name: str
) -> List[Dict[str, Any]]:
    return [{dimension_name: key, metric_name: value} for key, value in items]


def fetch_sample_report(period: ReportingPeriod) -> Dict[str, Any]:
    return {
        "warnings": ["Sample data mode enabled. No live Google Analytics data was queried."],
        "overview_current": {
            "totalUsers": 483,
            "activeUsers": 427,
            "newUsers": 281,
            "sessions": 611,
            "engagedSessions": 442,
            "screenPageViews": 1387,
            "averageSessionDuration": 98.4,
        },
        "overview_previous": {
            "totalUsers": 395,
            "activeUsers": 354,
            "newUsers": 231,
            "sessions": 522,
            "engagedSessions": 377,
            "screenPageViews": 1192,
            "averageSessionDuration": 84.2,
        },
        "pdf_clicks_current": sample_rows(
            [("resume_pdf_click", 19), ("cv_pdf_click", 11), ("pdf_link_click", 33)],
            "eventName",
            "eventCount",
        ),
        "pdf_clicks_previous": sample_rows(
            [("resume_pdf_click", 12), ("cv_pdf_click", 7), ("pdf_link_click", 21)],
            "eventName",
            "eventCount",
        ),
        "sections": {
            "channels": sample_rows(
                [
                    ("Organic Search", 261),
                    ("Direct", 182),
                    ("Referral", 79),
                    ("Social", 63),
                    ("Unassigned", 26),
                ],
                "sessionDefaultChannelGroup",
                "sessions",
            ),
            "sources": sample_rows(
                [
                    ("google / organic", 248),
                    ("(direct) / (none)", 182),
                    ("linkedin.com / referral", 42),
                    ("github.com / referral", 29),
                    ("scholar.google.com / referral", 23),
                ],
                "sessionSourceMedium",
                "sessions",
            ),
            "landing_pages": sample_rows(
                [
                    ("/", 401),
                    ("/files/Rajeev_Jain_Resume.pdf", 57),
                    ("/files/Rajeev_Jain_CV.pdf", 31),
                    ("/atma_siddhi.html", 14),
                    ("/atma_siddhi_hindi.html", 9),
                ],
                "landingPagePlusQueryString",
                "sessions",
            ),
            "pages": sample_rows(
                [
                    ("/", 981),
                    ("/files/Rajeev_Jain_Resume.pdf", 85),
                    ("/files/Rajeev_Jain_CV.pdf", 42),
                    ("/atma_siddhi.html", 26),
                    ("/atma_siddhi_hindi.html", 14),
                ],
                "pagePathPlusQueryString",
                "screenPageViews",
            ),
            "countries": sample_rows(
                [
                    ("United States", 301),
                    ("India", 74),
                    ("United Kingdom", 21),
                    ("Germany", 12),
                    ("Canada", 9),
                ],
                "country",
                "activeUsers",
            ),
            "cities": [
                {"city": "Chicago", "country": "United States", "activeUsers": 91},
                {"city": "New York", "country": "United States", "activeUsers": 36},
                {"city": "San Francisco", "country": "United States", "activeUsers": 27},
                {"city": "Bengaluru", "country": "India", "activeUsers": 18},
                {"city": "London", "country": "United Kingdom", "activeUsers": 11},
            ],
            "languages": sample_rows(
                [("en-us", 292), ("en-gb", 41), ("en-in", 34), ("de-de", 10), ("fr-fr", 6)],
                "language",
                "activeUsers",
            ),
            "devices": sample_rows(
                [("desktop", 289), ("mobile", 108), ("tablet", 30)],
                "deviceCategory",
                "activeUsers",
            ),
            "browsers": sample_rows(
                [("Chrome", 246), ("Safari", 75), ("Firefox", 47), ("Edge", 35), ("Mobile Safari", 19)],
                "browser",
                "activeUsers",
            ),
            "operating_systems": sample_rows(
                [("Windows", 171), ("Macintosh", 95), ("iOS", 48), ("Android", 44), ("Linux", 39)],
                "operatingSystem",
                "activeUsers",
            ),
        },
    }


def humanize_event_name(name: str) -> str:
    return name.replace("_", " ").strip().title()


def format_integer(value: Any) -> str:
    try:
        return f"{int(round(float(value))):,}"
    except (TypeError, ValueError):
        return str(value)


def format_duration(seconds: Any) -> str:
    try:
        total_seconds = int(round(float(seconds)))
    except (TypeError, ValueError):
        return str(seconds)
    minutes, remainder = divmod(total_seconds, 60)
    if minutes:
        return f"{minutes}m {remainder}s"
    return f"{remainder}s"


def format_delta(current: Any, previous: Any) -> str:
    try:
        current_value = float(current)
        previous_value = float(previous)
    except (TypeError, ValueError):
        return ""
    if previous_value == 0:
        return "new" if current_value else "0%"
    delta = ((current_value - previous_value) / previous_value) * 100
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.1f}%"


def build_metric_cards(report: Dict[str, Any]) -> List[Dict[str, str]]:
    current = report["overview_current"]
    previous = report["overview_previous"]

    pdf_current_map = {row["eventName"]: row["eventCount"] for row in report["pdf_clicks_current"]}
    pdf_previous_map = {row["eventName"]: row["eventCount"] for row in report["pdf_clicks_previous"]}

    metrics = [
        ("activeUsers", "Active users", format_integer),
        ("sessions", "Sessions", format_integer),
        ("screenPageViews", "Page views", format_integer),
        ("averageSessionDuration", "Avg. session", format_duration),
        ("resume_pdf_click", "Resume clicks", format_integer),
        ("cv_pdf_click", "CV clicks", format_integer),
    ]

    cards = []
    for key, label, formatter in metrics:
        if key in current:
            current_value = current.get(key, 0)
            previous_value = previous.get(key, 0)
        else:
            current_value = pdf_current_map.get(key, 0)
            previous_value = pdf_previous_map.get(key, 0)
        cards.append(
            {
                "label": label,
                "value": formatter(current_value),
                "delta": format_delta(current_value, previous_value),
            }
        )
    return cards


def combine_location_label(row: Dict[str, Any]) -> str:
    city = row.get("city", "").strip()
    country = row.get("country", "").strip()
    if city and country:
        return f"{city}, {country}"
    return city or country or "(not set)"


def shorten_label(value: str, max_length: int = 48) -> str:
    cleaned = value or "(not set)"
    if len(cleaned) <= max_length:
        return cleaned
    return cleaned[: max_length - 1] + "..."


def create_bar_chart(
    rows: List[Dict[str, Any]],
    label_fn: Callable[[Dict[str, Any]], str],
    value_key: str,
    title: str,
    color: str,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(9, 4.8))

    if rows:
        plotted_rows = list(reversed(rows[:8]))
        labels = [shorten_label(label_fn(row)) for row in plotted_rows]
        values = [float(row.get(value_key, 0)) for row in plotted_rows]
        bars = plt.barh(labels, values, color=color)
        plt.xlim(0, max(values) * 1.15 if any(values) else 1)
        for bar, value in zip(bars, values):
            plt.text(
                bar.get_width() + max(values) * 0.02 if any(values) else 0.02,
                bar.get_y() + bar.get_height() / 2,
                format_integer(value),
                va="center",
                fontsize=9,
                color="#18202c",
            )
    else:
        plt.text(0.5, 0.5, "No data available", ha="center", va="center", fontsize=14)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.xticks([])
        plt.yticks([])

    plt.title(title, loc="left", fontsize=15, fontweight="bold")
    plt.grid(axis="x", linestyle="--", alpha=0.25)
    plt.box(False)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close()


def build_chart_manifest(output_dir: Path, report: Dict[str, Any]) -> List[Dict[str, str]]:
    charts_dir = output_dir / "charts"
    chart_specs = [
        (
            "channels.png",
            report["sections"].get("channels", []),
            lambda row: row.get("sessionDefaultChannelGroup", "(not set)"),
            "sessions",
            "Traffic channels",
            "#103b5c",
        ),
        (
            "sources.png",
            report["sections"].get("sources", []),
            lambda row: row.get("sessionSourceMedium", "(not set)"),
            "sessions",
            "Top traffic sources",
            "#b35a3f",
        ),
        (
            "landing-pages.png",
            report["sections"].get("landing_pages", []),
            lambda row: row.get("landingPagePlusQueryString", "(not set)"),
            "sessions",
            "Top landing pages",
            "#0f766e",
        ),
        (
            "locations.png",
            report["sections"].get("cities", []),
            combine_location_label,
            "activeUsers",
            "Top visitor locations",
            "#8b5cf6",
        ),
        (
            "devices.png",
            report["sections"].get("devices", []),
            lambda row: row.get("deviceCategory", "(not set)").title(),
            "activeUsers",
            "Device categories",
            "#cb8b2c",
        ),
        (
            "pdf-clicks.png",
            report["pdf_clicks_current"],
            lambda row: humanize_event_name(row.get("eventName", "(not set)")),
            "eventCount",
            "Resume and CV clicks",
            "#1d4ed8",
        ),
    ]

    manifest = []
    for filename, rows, label_fn, value_key, title, color in chart_specs:
        output_path = charts_dir / filename
        create_bar_chart(rows, label_fn, value_key, title, color, output_path)
        manifest.append({"cid": filename, "path": str(output_path), "title": title})
    return manifest


def render_table(
    rows: List[Dict[str, Any]],
    columns: List[tuple[str, str, Callable[[Dict[str, Any]], str]]],
) -> str:
    if not rows:
        return "<p class=\"empty-state\">No data available.</p>"

    head = "".join(f"<th>{html.escape(label)}</th>" for _, label, _ in columns)
    body_rows = []
    for row in rows:
        cells = []
        for _, _, formatter in columns:
            cells.append(f"<td>{html.escape(formatter(row))}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    return (
        "<table><thead><tr>"
        + head
        + "</tr></thead><tbody>"
        + "".join(body_rows)
        + "</tbody></table>"
    )


def render_html_report(
    config: ReportConfig,
    period: ReportingPeriod,
    report: Dict[str, Any],
    cards: List[Dict[str, str]],
    charts: List[Dict[str, str]],
) -> str:
    generated = period.generated_at.strftime("%B %d, %Y %I:%M %p %Z")
    warning_html = ""
    if report["warnings"]:
        warning_items = "".join(
            f"<li>{html.escape(item)}</li>" for item in report["warnings"]
        )
        warning_html = (
            "<section class=\"warnings\"><h2>Warnings</h2><ul>"
            + warning_items
            + "</ul></section>"
        )

    def table_block(
        title: str,
        rows: List[Dict[str, Any]],
        columns: List[tuple[str, str, Callable[[Dict[str, Any]], str]]],
    ) -> str:
        return (
            f"<section><h2>{html.escape(title)}</h2>"
            + render_table(rows, columns)
            + "</section>"
        )

    metric_cards_html = "".join(
        "<div class=\"metric-card\">"
        f"<div class=\"metric-card__label\">{html.escape(card['label'])}</div>"
        f"<div class=\"metric-card__value\">{html.escape(card['value'])}</div>"
        f"<div class=\"metric-card__delta\">vs prior window: {html.escape(card['delta'])}</div>"
        "</div>"
        for card in cards
    )

    chart_sections = "".join(
        "<section class=\"chart-block\">"
        f"<h2>{html.escape(item['title'])}</h2>"
        f"<img src=\"cid:{html.escape(item['cid'])}\" alt=\"{html.escape(item['title'])}\">"
        "</section>"
        for item in charts
    )

    return f"""\
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{html.escape(config.site_name)} monthly analytics report</title>
    <style>
      body {{
        margin: 0;
        padding: 24px;
        background: #f5efe6;
        color: #18202c;
        font-family: Arial, Helvetica, sans-serif;
        line-height: 1.5;
      }}
      .shell {{
        max-width: 1080px;
        margin: 0 auto;
        background: #fffdf9;
        border: 1px solid rgba(24, 32, 44, 0.1);
        border-radius: 20px;
        padding: 28px;
      }}
      .eyebrow {{
        margin: 0 0 6px;
        color: #b35a3f;
        font-size: 12px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}
      h1 {{
        margin: 0;
        font-size: 30px;
      }}
      .subhead {{
        margin: 10px 0 0;
        color: #425166;
      }}
      .metrics {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        margin: 24px 0 32px;
      }}
      .metric-card {{
        border: 1px solid rgba(24, 32, 44, 0.1);
        border-radius: 16px;
        padding: 14px 16px;
        background: #ffffff;
      }}
      .metric-card__label {{
        color: #65748b;
        font-size: 13px;
      }}
      .metric-card__value {{
        margin-top: 6px;
        font-size: 26px;
        font-weight: 700;
      }}
      .metric-card__delta {{
        margin-top: 4px;
        color: #425166;
        font-size: 12px;
      }}
      .chart-grid {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 18px;
        margin: 12px 0 30px;
      }}
      .chart-block {{
        padding: 16px;
        border: 1px solid rgba(24, 32, 44, 0.08);
        border-radius: 16px;
        background: #fff;
      }}
      .chart-block img {{
        width: 100%;
        height: auto;
        display: block;
      }}
      section {{
        margin-top: 24px;
      }}
      h2 {{
        margin: 0 0 12px;
        font-size: 19px;
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
      }}
      th, td {{
        padding: 10px 12px;
        border-bottom: 1px solid rgba(24, 32, 44, 0.08);
        text-align: left;
        vertical-align: top;
      }}
      th {{
        color: #65748b;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
      }}
      .empty-state {{
        color: #65748b;
      }}
      .warnings {{
        border-left: 4px solid #cb8b2c;
        padding-left: 14px;
      }}
      @media (max-width: 700px) {{
        .metrics,
        .chart-grid {{
          grid-template-columns: 1fr;
        }}
      }}
    </style>
  </head>
  <body>
    <div class="shell">
      <p class="eyebrow">Monthly Analytics Report</p>
      <h1>{html.escape(config.site_name)}</h1>
      <p class="subhead">Reporting window: {html.escape(period.label)}<br>Previous comparison window: {html.escape(period.previous_label)}<br>Generated: {html.escape(generated)}</p>

      <div class="metrics">{metric_cards_html}</div>

      <div class="chart-grid">{chart_sections}</div>

      {table_block(
          "Traffic channels",
          report["sections"].get("channels", []),
          [
              ("sessionDefaultChannelGroup", "Channel", lambda row: row.get("sessionDefaultChannelGroup", "(not set)")),
              ("sessions", "Sessions", lambda row: format_integer(row.get("sessions", 0))),
          ],
      )}

      {table_block(
          "Top traffic sources",
          report["sections"].get("sources", []),
          [
              ("sessionSourceMedium", "Source / medium", lambda row: row.get("sessionSourceMedium", "(not set)")),
              ("sessions", "Sessions", lambda row: format_integer(row.get("sessions", 0))),
          ],
      )}

      {table_block(
          "Top landing pages",
          report["sections"].get("landing_pages", []),
          [
              ("landingPagePlusQueryString", "Landing page", lambda row: row.get("landingPagePlusQueryString", "(not set)")),
              ("sessions", "Sessions", lambda row: format_integer(row.get("sessions", 0))),
          ],
      )}

      {table_block(
          "Most viewed pages",
          report["sections"].get("pages", []),
          [
              ("pagePathPlusQueryString", "Page", lambda row: row.get("pagePathPlusQueryString", "(not set)")),
              ("screenPageViews", "Page views", lambda row: format_integer(row.get("screenPageViews", 0))),
          ],
      )}

      {table_block(
          "Countries",
          report["sections"].get("countries", []),
          [
              ("country", "Country", lambda row: row.get("country", "(not set)")),
              ("activeUsers", "Active users", lambda row: format_integer(row.get("activeUsers", 0))),
          ],
      )}

      {table_block(
          "Cities",
          report["sections"].get("cities", []),
          [
              ("location", "Location", combine_location_label),
              ("activeUsers", "Active users", lambda row: format_integer(row.get("activeUsers", 0))),
          ],
      )}

      {table_block(
          "Languages",
          report["sections"].get("languages", []),
          [
              ("language", "Language", lambda row: row.get("language", "(not set)")),
              ("activeUsers", "Active users", lambda row: format_integer(row.get("activeUsers", 0))),
          ],
      )}

      {table_block(
          "Device categories",
          report["sections"].get("devices", []),
          [
              ("deviceCategory", "Device", lambda row: row.get("deviceCategory", "(not set)").title()),
              ("activeUsers", "Active users", lambda row: format_integer(row.get("activeUsers", 0))),
          ],
      )}

      {table_block(
          "Browsers",
          report["sections"].get("browsers", []),
          [
              ("browser", "Browser", lambda row: row.get("browser", "(not set)")),
              ("activeUsers", "Active users", lambda row: format_integer(row.get("activeUsers", 0))),
          ],
      )}

      {table_block(
          "Operating systems",
          report["sections"].get("operating_systems", []),
          [
              ("operatingSystem", "Operating system", lambda row: row.get("operatingSystem", "(not set)")),
              ("activeUsers", "Active users", lambda row: format_integer(row.get("activeUsers", 0))),
          ],
      )}

      {table_block(
          "Resume and CV clicks",
          report["pdf_clicks_current"],
          [
              ("eventName", "Event", lambda row: humanize_event_name(row.get("eventName", "(not set)"))),
              ("eventCount", "Clicks", lambda row: format_integer(row.get("eventCount", 0))),
          ],
      )}

      {warning_html}
    </div>
  </body>
</html>
"""


def render_text_report(
    config: ReportConfig,
    period: ReportingPeriod,
    report: Dict[str, Any],
    cards: List[Dict[str, str]],
) -> str:
    lines = [
        f"{config.site_name} monthly analytics report",
        f"Reporting window: {period.label}",
        f"Comparison window: {period.previous_label}",
        f"Generated: {period.generated_at.strftime('%B %d, %Y %I:%M %p %Z')}",
        "",
        "Summary:",
    ]
    for card in cards:
        lines.append(f"- {card['label']}: {card['value']} ({card['delta']} vs prior window)")

    def add_section(title: str, rows: List[Dict[str, Any]], formatter: Callable[[Dict[str, Any]], str]) -> None:
        lines.append("")
        lines.append(title + ":")
        if not rows:
            lines.append("- No data available")
            return
        for row in rows[:5]:
            lines.append(f"- {formatter(row)}")

    add_section(
        "Top channels",
        report["sections"].get("channels", []),
        lambda row: f"{row.get('sessionDefaultChannelGroup', '(not set)')}: {format_integer(row.get('sessions', 0))} sessions",
    )
    add_section(
        "Top locations",
        report["sections"].get("cities", []),
        lambda row: f"{combine_location_label(row)}: {format_integer(row.get('activeUsers', 0))} active users",
    )
    add_section(
        "Resume and CV clicks",
        report["pdf_clicks_current"],
        lambda row: f"{humanize_event_name(row.get('eventName', '(not set)'))}: {format_integer(row.get('eventCount', 0))}",
    )

    if report["warnings"]:
        lines.append("")
        lines.append("Warnings:")
        for item in report["warnings"]:
            lines.append(f"- {item}")

    return "\n".join(lines)


def write_artifacts(
    config: ReportConfig,
    period: ReportingPeriod,
    report: Dict[str, Any],
    cards: List[Dict[str, str]],
    charts: List[Dict[str, str]],
    html_report: str,
    text_report: str,
) -> None:
    config.output_dir.mkdir(parents=True, exist_ok=True)
    (config.output_dir / "report.html").write_text(html_report, encoding="utf-8")
    (config.output_dir / "report.txt").write_text(text_report, encoding="utf-8")
    (config.output_dir / "report.json").write_text(
        json.dumps(
            {
                "site_name": config.site_name,
                "reporting_window": period.label,
                "comparison_window": period.previous_label,
                "generated_at": period.generated_at.isoformat(),
                "summary_cards": cards,
                "warnings": report["warnings"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (config.output_dir / "charts.json").write_text(
        json.dumps(charts, indent=2), encoding="utf-8"
    )


def send_email(
    config: ReportConfig,
    period: ReportingPeriod,
    html_report: str,
    text_report: str,
    charts: List[Dict[str, str]],
) -> None:
    subject = f"{config.site_name} monthly analytics report | {period.label}"
    message = MIMEMultipart("related")
    message["Subject"] = subject
    message["From"] = config.email_from
    message["To"] = ", ".join(config.email_to)

    alternative = MIMEMultipart("alternative")
    alternative.attach(MIMEText(text_report, "plain", "utf-8"))
    alternative.attach(MIMEText(html_report, "html", "utf-8"))
    message.attach(alternative)

    for chart in charts:
        path = Path(chart["path"])
        with path.open("rb") as image_file:
            image = MIMEImage(image_file.read())
        image.add_header("Content-ID", f"<{chart['cid']}>")
        image.add_header("Content-Disposition", "inline", filename=path.name)
        message.attach(image)

    if config.smtp_use_ssl:
        with smtplib.SMTP_SSL(
            config.smtp_host,
            config.smtp_port,
            context=ssl.create_default_context(),
        ) as server:
            if config.smtp_username:
                server.login(config.smtp_username, config.smtp_password)
            server.send_message(message)
        return

    with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=60) as server:
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.ehlo()
        if config.smtp_username:
            server.login(config.smtp_username, config.smtp_password)
        server.send_message(message)


def main() -> int:
    try:
        args = parse_args()
        config = build_config(args)
        period = compute_reporting_period(config.timezone_name, config.window_days)
        report = (
            fetch_sample_report(period)
            if config.sample_data
            else fetch_live_report(config, period)
        )
        cards = build_metric_cards(report)
        charts = build_chart_manifest(config.output_dir, report)
        html_report = render_html_report(config, period, report, cards, charts)
        text_report = render_text_report(config, period, report, cards)
        write_artifacts(config, period, report, cards, charts, html_report, text_report)
        if not config.skip_email:
            send_email(config, period, html_report, text_report, charts)
        print(f"Wrote analytics report to {config.output_dir}")
        if config.skip_email:
            print("Email sending skipped.")
        else:
            print(f"Sent analytics report email to {', '.join(config.email_to)}")
        return 0
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Unhandled error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
