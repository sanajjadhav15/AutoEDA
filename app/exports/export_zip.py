import os
import tempfile
from plotly.graph_objs import Figure

def save_all_charts(plots: dict, export_dir="exports/plots") -> list:
    """
    Saves each Plotly figure from the plots dictionary as a .png file.
    Returns a list of saved file paths.
    """
    os.makedirs(export_dir, exist_ok=True)
    saved_files = []

    for name, fig in plots.items():
        if isinstance(fig, Figure):  # Valid Plotly figure
            filename = f"{name.replace(' ', '_').replace('-', '_').lower()}.png"
            filepath = os.path.join(export_dir, filename)
            try:
                fig.write_image(filepath)
                saved_files.append(filepath)
            except Exception as e:
                print(f"[save_all_charts] Failed to save '{name}': {e}")
                # Try with different format if PNG fails
                try:
                    html_filename = f"{name.replace(' ', '_').replace('-', '_').lower()}.html"
                    html_filepath = os.path.join(export_dir, html_filename)
                    fig.write_html(html_filepath)
                    saved_files.append(html_filepath)
                    print(f"[save_all_charts] Saved as HTML instead: {name}")
                except Exception as e2:
                    print(f"[save_all_charts] Failed to save as HTML too '{name}': {e2}")
        else:
            print(f"[save_all_charts] Skipping '{name}' — not a valid Plotly figure")

    return saved_files
