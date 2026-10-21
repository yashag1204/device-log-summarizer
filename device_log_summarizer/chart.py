"""Create a bar chart of average temperature per summarized device."""

import argparse
import json
import sys
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")  # Allows saving charts without a display/window.
    import matplotlib.pyplot as plt
except ImportError:
    print("Error: matplotlib is required. Install it with: python -m pip install matplotlib",
          file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Chart average device temperatures.")
    parser.add_argument("--input", type=Path, default=Path("outputs/device_summary.json"))
    parser.add_argument("--output", type=Path, default=Path("outputs/average_temperature.png"))
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: JSON input not found: {args.input}", file=sys.stderr)
        return 1

    try:
        with args.input.open(encoding="utf-8") as handle:
            rows = json.load(handle)
        if not isinstance(rows, list):
            raise ValueError("JSON root must be a list of device summary objects.")
        for row in rows:
            if not isinstance(row, dict) or "device_id" not in row or "average_temperature" not in row:
                raise ValueError("Each JSON item must include device_id and average_temperature.")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: could not read valid summary JSON: {exc}", file=sys.stderr)
        return 1

    labels = [str(row["device_id"]) for row in rows]
    try:
        temperatures = [float(row["average_temperature"]) for row in rows]
    except (TypeError, ValueError, OverflowError):
        print("Error: average_temperature values must be numeric.", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5.5), constrained_layout=True)
    if rows:
        bars = ax.bar(labels, temperatures)
        ax.bar_label(bars, fmt="%.2f", padding=4)
        ax.set_ylim(0, max(temperatures) * 1.18 if max(temperatures) > 0 else 1)
    else:
        ax.text(0.5, 0.5, "No devices passed the temperature filter",
                ha="center", va="center", transform=ax.transAxes)
        ax.set_xticks([])

    ax.set_title("Average Temperature per Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature (°C)")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    fig.savefig(args.output, dpi=160)
    plt.close(fig)
    print(f"Chart saved to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
