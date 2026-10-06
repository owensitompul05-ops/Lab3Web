import os
import re
import base64
import subprocess
import markdown
from pygments.formatters import HtmlFormatter

def image_to_base64(match, base_dir):
    alt_text = match.group(1)
    img_path = match.group(2)
    
    # Resolve relative path
    full_path = os.path.normpath(os.path.join(base_dir, img_path))
    if os.path.exists(full_path):
        with open(full_path, "rb") as img_file:
            b64_data = base64.b64encode(img_file.read()).decode("utf-8")
            ext = os.path.splitext(full_path)[1].lower().replace(".", "")
            if ext == "jpg":
                ext = "jpeg"
            return f'<div class="img-container"><img src="data:image/{ext};base64,{b64_data}" alt="{alt_text}"><div class="caption">{alt_text}</div></div>'
    return match.group(0)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(base_dir, "README.md")
    html_output_path = os.path.join(base_dir, "laporan.html")
    pdf_output_path = os.path.join(base_dir, "Laporan_Praktikum_3_CSS_Dasar.pdf")

    with open(readme_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert markdown image syntax ![alt](path) to base64 embedded html before markdown conversion
    md_text = re.sub(r'!\[(.*?)\]\((.*?)\)', lambda m: image_to_base64(m, base_dir), md_text)

    # Convert markdown to HTML
    html_body = markdown.markdown(
        md_text,
        extensions=[
            'fenced_code',
            'tables',
            'codehilite',
            'nl2br'
        ],
        extension_configs={
            'codehilite': {
                'guess_lang': False,
                'css_class': 'codehilite',
                'linenums': False
            }
        }
    )

    pygments_css = HtmlFormatter(style="default").get_style_defs('.codehilite')

    full_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laporan Praktikum 3 - CSS Dasar</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 15mm 15mm 15mm 15mm;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', Arial, sans-serif;
            font-size: 10.5pt;
            line-height: 1.6;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }}

        /* Header Title Banner */
        h1:first-of-type {{
            font-size: 20pt;
            font-weight: 700;
            color: #0f172a;
            border-bottom: 3px solid #0284c7;
            padding-bottom: 8px;
            margin-top: 0;
            margin-bottom: 12px;
        }}

        h2 {{
            font-size: 14pt;
            font-weight: 600;
            color: #0369a1;
            border-bottom: 1.5px solid #e2e8f0;
            padding-bottom: 6px;
            margin-top: 24px;
            margin-bottom: 12px;
            page-break-after: avoid;
        }}

        h3 {{
            font-size: 12pt;
            font-weight: 600;
            color: #1e293b;
            margin-top: 18px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }}

        h4 {{
            font-size: 11pt;
            font-weight: 600;
            color: #334155;
            margin-top: 14px;
            margin-bottom: 6px;
            page-break-after: avoid;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 10px;
            text-align: justify;
        }}

        hr {{
            border: 0;
            height: 1px;
            background-color: #e2e8f0;
            margin: 20px 0;
        }}

        /* Table Styling */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 14px 0 20px 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }}

        th, td {{
            border: 1px solid #cbd5e1;
            padding: 8px 12px;
            text-align: left;
            vertical-align: top;
        }}

        th {{
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 600;
        }}

        tr:nth-child(even) td {{
            background-color: #f8fafc;
        }}

        /* Blockquotes / Callouts */
        blockquote {{
            margin: 12px 0;
            padding: 10px 16px;
            background-color: #f0fdf4;
            border-left: 4px solid #16a34a;
            color: #166534;
            font-style: italic;
            border-radius: 0 6px 6px 0;
            page-break-inside: avoid;
        }}

        blockquote p {{
            margin: 0;
        }}

        /* Code & Pre */
        code {{
            font-family: 'Consolas', 'Fira Code', 'Courier New', monospace;
            font-size: 9.5pt;
            background-color: #f1f5f9;
            color: #0f172a;
            padding: 2px 5px;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
        }}

        pre, .codehilite {{
            background-color: #f8fafc !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 6px;
            padding: 12px 14px !important;
            margin: 12px 0 16px 0;
            font-size: 9pt;
            line-height: 1.45;
            overflow-x: auto;
            page-break-inside: avoid;
        }}

        pre code, .codehilite code {{
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
            color: inherit;
        }}

        /* Images and Captions */
        .img-container {{
            text-align: center;
            margin: 14px 0 18px 0;
            page-break-inside: avoid;
        }}

        .img-container img {{
            max-width: 92%;
            max-height: 380px;
            height: auto;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
            display: inline-block;
        }}

        .img-container .caption {{
            font-size: 9pt;
            color: #64748b;
            margin-top: 6px;
            font-style: italic;
        }}

        /* Lists */
        ul, ol {{
            margin-top: 0;
            margin-bottom: 12px;
            padding-left: 24px;
        }}

        li {{
            margin-bottom: 4px;
        }}

        /* Link Styling */
        a {{
            color: #0284c7;
            text-decoration: none;
        }}

        /* Pygments Syntax Highlighting Theme */
        {pygments_css}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"HTML generated successfully: {html_output_path}")

    # Generate PDF using Chrome
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    file_url = "file:///" + html_output_path.replace("\\", "/")
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_output_path}",
        "--no-pdf-header-footer",
        file_url
    ]

    print("Running Chrome print-to-pdf...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_output_path):
        size_kb = os.path.getsize(pdf_output_path) / 1024
        print(f"PDF successfully generated: {pdf_output_path} ({size_kb:.1f} KB)")
    else:
        print(f"PDF generation failed! Stderr: {res.stderr}")

if __name__ == "__main__":
    main()
