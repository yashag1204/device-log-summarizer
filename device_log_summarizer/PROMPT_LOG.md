# AI Prompt Log

## Initial prompt

> Write a Python script that loads the JSON summary produced by my device telemetry
> CSV aggregation script and creates a Matplotlib bar chart comparing average
> temperature per device. Include a title, axis labels, and readable device labels.
> Save the chart as a PNG file.

## Bug / formatting issue found during review

The first chart draft did not reserve enough vertical space for the value labels above
the bars. On higher values, the labels could sit against the top of the plotting area
or be clipped. It also did not handle an empty JSON list clearly.

## Follow-up prompt

> Fix the chart layout so value labels above the bars remain visible. Use a figure
> layout that avoids clipping, add a little headroom to the y-axis, include a light
> horizontal grid, and show a helpful message if the JSON list is empty. Also save
> the figure to a PNG and close it after saving.

## Review notes

I reviewed the generated code, checked that it reads `average_temperature` from the
JSON output, added input validation and error messages, set a non-interactive Matplotlib
backend for command-line use, and tested it against the sample JSON.
