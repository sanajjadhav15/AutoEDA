# exports/export_pdf.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os
import tempfile
import matplotlib.pyplot as plt

try:
    import plotly.io as pio
    import plotly.graph_objects as go
    # Set default renderer and ensure kaleido is working
    try:
        if pio.kaleido.scope is not None:
            pio.kaleido.scope.default_format = "png"
            pio.kaleido.scope.default_engine = "kaleido"
    except (AttributeError, Exception):
        # Kaleido scope not available, will handle in export function
        pass
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

def export_pdf_report(df, summary_stats, missing_report, insights, plots_dict):
    styles = getSampleStyleSheet()
    story = []
    temp_files_to_cleanup = []  # Track temp files for cleanup after PDF generation

    # === Title ===
    story.append(Paragraph("📊 AutoEDA Executive Report", styles['Title']))
    story.append(Spacer(1, 12))

    # === Dataset Metadata ===
    meta_info = f"""
    <b>Dataset Overview</b><br/>
    Rows: {df.shape[0]}<br/>
    Columns: {df.shape[1]}<br/>
    Numeric Columns: {df.select_dtypes(include='number').shape[1]}<br/>
    Categorical Columns: {df.select_dtypes(include='object').shape[1]}<br/>
    Null Values Present: {'Yes' if df.isnull().sum().sum() > 0 else 'No'}
    """
    story.append(Paragraph(meta_info, styles['Normal']))
    story.append(Spacer(1, 12))

    # === Summary Statistics ===
    story.append(Paragraph("<b>Summary Statistics</b>", styles['Heading2']))
    if summary_stats is not None and not summary_stats.empty:
        # Convert summary stats to table format (first 5 rows to keep it manageable)
        summary_table_data = [summary_stats.columns.to_list()] + summary_stats.round(2).head(5).values.tolist()
        summary_table = Table(summary_table_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        story.append(summary_table)
    else:
        story.append(Paragraph("No summary statistics available.", styles['Normal']))
    story.append(Spacer(1, 12))

    # === Missing Value Report ===
    story.append(Paragraph("<b>Null Value Flags</b>", styles['Heading2']))
    if not missing_report.empty:
        null_table = [missing_report.columns.to_list()] + missing_report.values.tolist()
        table = Table(null_table)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        story.append(table)
    else:
        story.append(Paragraph("No columns with high missing values.", styles['Normal']))
    story.append(Spacer(1, 12))

    # === Smart Insights ===
    story.append(Paragraph("<b>Smart Insights</b>", styles['Heading2']))
    if insights and isinstance(insights, dict):
        # Handle dictionary of categorized insights
        for category, insight_list in insights.items():
            if insight_list:  # Only show categories that have insights
                story.append(Paragraph(f"<b>{category}</b>", styles['Heading3']))
                for ins in insight_list:
                    story.append(Paragraph(f"• {ins}", styles['Normal']))
                story.append(Spacer(1, 6))
    elif insights and isinstance(insights, list):
        # Handle simple list of insights (fallback)
        for ins in insights:
            story.append(Paragraph(f"• {ins}", styles['Normal']))
    else:
        story.append(Paragraph("No critical insights generated.", styles['Normal']))
    story.append(Spacer(1, 12))

    # === Plots ===
    story.append(Paragraph("<b>Visualizations</b>", styles['Heading2']))
    
    if not plots_dict:
        story.append(Paragraph("No visualizations available.", styles['Normal']))
    else:
        for name, fig in plots_dict.items():
            temp_file_path = None
            try:
                if fig is not None:
                    # Create temporary file
                    temp_file_path = tempfile.mktemp(suffix=".png")
                    temp_files_to_cleanup.append(temp_file_path)
                    
                    # Handle Plotly figures with improved error handling
                    if hasattr(fig, 'write_image'):
                        try:
                            # Try with specific settings for better compatibility
                            fig.write_image(
                                temp_file_path,
                                format="png",
                                width=800,
                                height=500,
                                scale=1
                            )
                        except Exception as plotly_error:
                            # Fallback: try with different settings
                            try:
                                fig.write_image(
                                    temp_file_path,
                                    format="png",
                                    width=600,
                                    height=400
                                )
                            except Exception as second_error:
                                # Try with minimal settings
                                try:
                                    fig.write_image(temp_file_path)
                                except Exception:
                                    # Last resort: skip this plot
                                    story.append(Paragraph(f"<b>{name}</b> - Could not generate image", styles['Heading3']))
                                    story.append(Paragraph("Plot generation failed due to image export issues.", styles['Normal']))
                                    story.append(Spacer(1, 12))
                                    continue
                    else:
                        # Handle matplotlib figures
                        fig.savefig(temp_file_path, bbox_inches="tight", dpi=100)
                    
                    # Only add image if file was created successfully
                    if os.path.exists(temp_file_path) and os.path.getsize(temp_file_path) > 0:
                        img = Image(temp_file_path, width=480)
                        story.append(Paragraph(f"<b>{name}</b>", styles['Heading3']))
                        story.append(img)
                        story.append(Spacer(1, 12))
                    else:
                        story.append(Paragraph(f"<b>{name}</b> - Image file empty", styles['Heading3']))
                        story.append(Paragraph("Generated image file was empty or corrupted.", styles['Normal']))
                        story.append(Spacer(1, 12))
                        
            except Exception as e:
                # If image export fails, show error message
                story.append(Paragraph(f"<b>{name}</b> - Export Error", styles['Heading3']))
                story.append(Paragraph(f"Could not generate visualization: {str(e)[:100]}...", styles['Normal']))
                story.append(Spacer(1, 12))

    # === Build PDF ===
    output_path = os.path.join("exports", "autoeda_report.pdf")
    
    # Ensure exports directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    doc.build(story)
    
    # Clean up temporary files after PDF is built
    for temp_file in temp_files_to_cleanup:
        try:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        except (PermissionError, OSError):
            # If we can't delete it immediately, it will be cleaned up by the OS later
            pass
    
    return output_path
