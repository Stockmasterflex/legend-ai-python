import argparse
import math
from pathlib import Path
from typing import Dict, Iterable, Optional

from prometheus_client.parser import text_string_to_metric_families


def parse_metrics(path: Path):
    data = path.read_text()
    return list(text_string_to_metric_families(data))


def _match_labels(labels: Dict[str, str], filters: Dict[str, str]) -> bool:
    return all(labels.get(key) == value for key, value in filters.items())


def _parse_le(value: str) -> float:
    if value.lower() in {"+inf", "inf"}:
        return math.inf
    try:
        return float(value)
    except ValueError:
        return math.inf


def histogram_percentile(
    families: Iterable,
    bucket_name: str,
    count_name: str,
    label_filters: Dict[str, str],
    percentile: float,
):
    buckets: Dict[float, float] = {}
    total_count = 0.0
    for family in families:
        if family.name == bucket_name:
            for sample in family.samples:
                if _match_labels(sample.labels, label_filters):
                    le = _parse_le(sample.labels.get("le", "+Inf"))
                    buckets[le] = sample.value
        elif family.name == count_name:
            for sample in family.samples:
                if _match_labels(sample.labels, label_filters):
                    total_count += sample.value

    if not buckets or total_count <= 0:
        return None, int(total_count)

    threshold = total_count * percentile
    cumulative = 0.0
    for le in sorted(buckets):
        cumulative = buckets[le]
        if cumulative >= threshold:
            return (None if math.isinf(le) else le), int(total_count)
    return sorted(buckets)[-1], int(total_count)


def total_count(families, count_name, label_filters=None):
    label_filters = label_filters or {}
    total = 0.0
    for family in families:
        if family.name != count_name:
            continue
        for sample in family.samples:
            if _match_labels(sample.labels, label_filters):
                total += sample.value
    return int(total)


def error_counter(families, name):
    for family in families:
        if family.name != name:
            continue
        for sample in family.samples:
            return sample.value
    return 0.0


def format_latency(seconds: Optional[float]) -> str:
    if seconds is None:
        return "n/a"
    return f"{seconds * 1000:.1f} ms"


def main():
    parser = argparse.ArgumentParser(description="SLO report based on Prometheus telemetry.")
    parser.add_argument(
        "--metrics-file",
        "-m",
        type=Path,
        default=Path("artifacts/metrics.prom"),
        help="Path to the Prometheus exposition file.",
    )
    args = parser.parse_args()

    families = parse_metrics(args.metrics_file)

    analyze_p95, _ = histogram_percentile(
        families,
        bucket_name="analyze_request_duration_seconds_bucket",
        count_name="analyze_request_duration_seconds_count",
        label_filters={"interval": "1day"},
        percentile=0.95,
    )

    scan_p95, _ = histogram_percentile(
        families,
        bucket_name="scan_request_duration_seconds_bucket",
        count_name="scan_request_duration_seconds_count",
        label_filters={"status": "ok"},
        percentile=0.95,
    )

    analyze_errors = error_counter(families, "analyze_errors_total")
    scan_errors = error_counter(families, "scan_errors_total")
    total_errors = analyze_errors + scan_errors
    analyze_total = total_count(
        families,
        "analyze_request_duration_seconds_count",
        {"interval": "1day"},
    )
    scan_total = total_count(families, "scan_request_duration_seconds_count")
    total_requests = analyze_total + scan_total

    error_rate = None
    if total_requests > 0:
        error_rate = (total_errors / total_requests) * 100

    print("SLO REPORT")
    print("-" * 40)
    print(f"Analyze /api/analyze p95 (1day): {format_latency(analyze_p95)}")
    print(f"Scan /api/scan p95 (ok status): {format_latency(scan_p95)}")
    if error_rate is None:
        print("Error rate: n/a (no requests recorded)")
    else:
        print(f"Error rate: {error_rate:.2f}% ({total_errors} errors over {total_requests} requests)")


if __name__ == "__main__":
    main()
