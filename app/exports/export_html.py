import os
import plotly.io as pio
from datetime import datetime

def export_html_report(df, summary_stats, missing_report, insights, plots, export_dir="exports/reports"):
    """
    Generates an interactive HTML report with summary stats, null flags, smart insights, and Plotly charts.
    Saves a single self-contained HTML file.
    """
    os.makedirs(export_dir, exist_ok=True)

    html_sections = []

    # Title
    html_sections.append("<h1 style='text-align:center;'>📊 AutoEDA Report</h1>")
    html_sections.append(f"<p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")

    # Dataset Metadata
    html_sections.append("<h2>📦 Dataset Metadata</h2>")
    html_sections.append(f"<p><strong>Rows:</strong> {df.shape[0]}<br>")
    html_sections.append(f"<strong>Columns:</strong> {df.shape[1]}</p>")

    html_sections.append("<table border='1' cellspacing='0' cellpadding='5'><tr><th>Column</th><th>Data Type</th><th>Missing (%)</th></tr>")
    for col in df.columns:
        null_pct = df[col].isnull().mean() * 100
        html_sections.append(f"<tr><td>{col}</td><td>{df[col].dtype}</td><td>{null_pct:.2f}%</td></tr>")
    html_sections.append("</table>")

    # Summary Stats
    html_sections.append("<h2>📋 Summary Statistics</h2>")
    html_sections.append(summary_stats.to_html(border=1, justify="center"))

    # Null Flagging
    html_sections.append("<h2>🧯 Null Flagging</h2>")
    if not missing_report.empty:
        html_sections.append(missing_report.to_html(index=False, border=1, justify="center"))
    else:
        html_sections.append("<p>No major missing value issues found.</p>")

    # Smart Insights
    html_sections.append("<h2>⚠️ Smart Insights</h2>")
    if insights:
        html_sections.append("<ul>")
        for i in insights:
            html_sections.append(f"<li>{i}</li>")
        html_sections.append("</ul>")
    else:
        html_sections.append("<p>No significant insights generated.</p>")

    # Interactive Charts
    html_sections.append("<h2>📈 Visualizations</h2>")
    for name, fig in plots.items():
        if fig is not None:
            html_sections.append(f"<h3>{name}</h3>")
            html_sections.append(pio.to_html(fig, include_plotlyjs='cdn', full_html=False))

    # Combine all sections into one HTML string
    full_html = "<html><head><meta charset='utf-8'><title>AutoEDA Report</title></head><body>"
    full_html += "\n".join(html_sections)
    full_html += "</body></html>"

    # Save the HTML
    filename = f"autoeda_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(export_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_html)

    return filepath
