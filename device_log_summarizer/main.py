"""Device Log Summarizer CLI.

Reads device telemetry CSV, aggregates records by device, excludes devices
whose mean temperature is above 80.0, writes JSON, and prints a terminal table.
Uses only Python's standard library.
"""

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


def summarize_csv(csv_path: Path) -> tuple[list[dict], list[str]]:
    """Return filtered summary rows and non-fatal data warnings."""
    warnings: list[str] = []
    aggregates: dict[str, dict] = defaultdict(
        lambda: {"record_count": 0, "temperature_sum": 0.0, "error_count": 0}
    )

    with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"device_id", "status", "temperature"}
        headers = set(reader.fieldnames or [])
        missing = required - headers
        if missing:
            raise ValueError(
                "CSV is missing required column(s): " + ", ".join(sorted(missing))
            )

        for line_number, row in enumerate(reader, start=2):
            device_id = (row.get("device_id") or "").strip()
            status = (row.get("status") or "").strip().upper()
            raw_temperature = (row.get("temperature") or "").strip()

            if not device_id:
                warnings.append(f"Line {line_number}: skipped row with empty device_id.")
                continue

            try:
                temperature = float(raw_temperature)
            except (TypeError, ValueError, OverflowError):
                warnings.append(
                    f"Line {line_number}: skipped row for {device_id!r} "
                    "because temperature is missing or not numeric."
                )
                continue

            if not math.isfinite(temperature):
                warnings.append(
                    f"Line {line_number}: skipped row for {device_id!r} "
                    "because temperature is not finite."
                )
                continue

            # Count rows with a usable device_id and numeric finite temperature.
            aggregates[device_id]["record_count"] += 1
            aggregates[device_id]["temperature_sum"] += temperature
            if status == "ERROR":
                aggregates[device_id]["error_count"] += 1

    results: list[dict] = []
    for device_id, values in sorted(aggregates.items()):
        average = values["temperature_sum"] / values["record_count"]
        if average > 80.0:
            continue
        results.append({
            "device_id": device_id,
            "record_count": values["record_count"],
            "average_temperature": round(average, 2),
            "error_count": values["error_count"],
        })

    return results, warnings


def print_table(results: list[dict]) -> None:
    headers = ("DEVICE", "RECORDS", "AVG TEMP (°C)", "ERRORS")
    rows = [
        (
            row["device_id"],
            str(row["record_count"]),
            f'{row["average_temperature"]:.2f}',
            str(row["error_count"]),
        )
        for row in results
    ]
    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows)) if rows else len(headers[i])
        for i in range(len(headers))
    ]

    def format_row(row: tuple[str, ...]) -> str:
        return " | ".join(value.ljust(widths[i]) for i, value in enumerate(row))

    print(format_row(headers))
    print("-+-".join("-" * width for width in widths))
    if not rows:
        print("(no devices passed the temperature filter)")
    else:
        for row in rows:
            print(format_row(row))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize device telemetry from CSV into filtered JSON."
    )
    parser.add_argument(
        "--input", type=Path, default=Path("data/device_telemetry.csv"),
        help="Input CSV path (default: data/device_telemetry.csv)",
    )
    parser.add_argument(
        "--output", type=Path, default=Path("outputs/device_summary.json"),
        help="Output JSON path (default: outputs/device_summary.json)",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: input CSV not found: {args.input}", file=sys.stderr)
        return 1

    try:
        results, warnings = summarize_csv(args.input)
    except (OSError, csv.Error, ValueError) as exc:
        print(f"Error: could not process CSV: {exc}", file=sys.stderr)
        return 1

    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as handle:
            json.dump(results, handle, indent=2)
            handle.write("\n")
    except OSError as exc:
        print(f"Error: could not write JSON output: {exc}", file=sys.stderr)
        return 1

    print_table(results)
    print(f"\nSaved {len(results)} device summary row(s) to {args.output}")
    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
