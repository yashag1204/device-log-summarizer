# Device Log Summarizer CLI

A small Python CLI project for the Software Engineering Intern assessment. It cleans
sensor values, reads telemetry CSV data, summarizes each device, filters high-average
temperature devices, exports JSON, prints a terminal table, and generates a bar chart.

## Project files

- `clean_sensor.py` — Section 1 cleaning function and three simple tests.
- `main.py` — Section 2 CSV aggregation, filtering, JSON export, and terminal table.
- `chart.py` — Section 3 Matplotlib chart generator.
- `data/device_telemetry.csv` — sample input data.
- `outputs/device_summary.json` — generated filtered summary.
- `outputs/average_temperature.png` — generated chart.
- `PROMPT_LOG.md` — AI prompting and review notes.

## Requirements

- Python 3.9+
- Matplotlib for the chart (`main.py` and `clean_sensor.py` use only the standard library).

Install Matplotlib if needed:

```bash
python -m pip install matplotlib
```

## Run

Run commands from the project root:

```bash
python clean_sensor.py
python main.py
python chart.py
```

Optional file paths:

```bash
python main.py --input data/device_telemetry.csv --output outputs/device_summary.json
python chart.py --input outputs/device_summary.json --output outputs/average_temperature.png
```

## Sample behavior

Devices with average temperature **greater than 80.0°C** are excluded. A device averaging
exactly 80.0°C remains in the output, because the assessment says “above 80.0.”

## Assumptions and data handling

1. `device_telemetry.csv` is sample data created for this submission because the assessment
   describes the required CSV columns but does not include the actual CSV file.
2. Rows with a blank `device_id` or a missing, non-numeric, NaN, or infinite temperature
   are skipped with a warning. `record_count` counts only rows with a non-empty device ID
   and a valid finite numeric temperature.
3. Status is trimmed and compared case-insensitively to `ERROR`; unknown or blank statuses
   are not counted as errors, but otherwise valid temperature rows still count.
4. Negative temperatures are retained in Section 2 because that section does not specify
   excluding them. Section 1 has its own explicit negative-value rule.
5. JSON contains only devices that pass the average-temperature filter, as requested.
6. The mean is rounded to two decimal places for clean output; filtering uses the unrounded
   mean so rounding cannot change whether a device is excluded.
