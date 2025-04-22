import csv
from jinja2 import Template
import os
import glob
import shutil
from pathlib import Path

# Define your HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parcel Label</title>
    
    <style>
    @page {
        size: 50mm 75mm;
        margin: 0;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Kalpurush', 'Poppins', sans-serif;
    }

    body {
        font-family: 'Kalpurush', 'Poppins', sans-serif;
        font-size: 7pt;
    }

    .parcel-label {
        width: 50mm;
        height: 75mm;
        background: #fff;
        border: none;
        border-radius: 2mm;
        padding: 3mm;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .label-logo {
        height: 5mm;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }

    .label-logo img {
        max-height: 100%;
        max-width: 100%;
        height: 7mm;
        width: auto;
        display: block;
        margin: auto;
    }

    .customer-info {
        border: 1px solid #000;
        border-radius: 1mm;
        padding: 2mm;
        font-size: 7pt;
        line-height: 1.2;
    }

    .customer-info p {
        margin-bottom: 1mm;
        font-size: 7pt;
        color: #000;
    }

    .mrcnt-name p {
        font-size: 7pt;
        text-align: center;
        color: #111;
    }

    .label-footer {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 6pt;
        color: #000;
        margin-top: 1mm;
    }

    @font-face {
    font-family: 'Kalpurush';
    src: url('https://www.omicronlab.com/download/fonts/kalpurush.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}

    </style>
</head>
<body>
    <div class="parcel-label d-flex flex-column align-items-center justify-content-between">
        <div class="label-top">
            <div class="label-logo d-flex justify-content-center align-items-center">
                <img src="logo.png" alt="Logo">
            </div>
        </div>
        <div class="label-body">
            <div class="mrcnt-name d-flex flex-column justify-content-center align-items-center">
            </div>
            <div class="customer-info d-flex flex-column gap-1 mt-2">
                <b><p>Name: {{ name }}</p></b>
                <b><p>Phone: {{ phone }}</p></b>
                <b><p>COD: {{ collectableamount }}</p></b>
                <p><b>Address:</b> {{ address }}</p>
                <p><b>Product:</b> {{ product }}</p>
            </div>
        </div>
        <div class="label-footer d-flex justify-content-center align-items-center w-100 mt-2">
            <div class="power-by d-flex flex-column justify-content-end gap-1">
                <p>Thanks for Shopping at</p>
                <p>www.divaniz.com</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Function to find a file in the script's directory or subdirectories
def find_file(filename, search_paths=None):
    if search_paths is None:
        # Default search paths: script's directory and 'images' subdirectory
        search_paths = [
            Path.cwd(),  # Current working directory
            Path.cwd() / "images",  # images/ subdirectory
        ]
    
    for search_path in search_paths:
        file_path = search_path / filename
        if file_path.exists():
            return file_path
    return None

# Function to generate HTML from CSV
def generate_html_from_csv(csv_file, template):
    # Ensure the output directory exists
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Read CSV file
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Generate an HTML file for each row in CSV
        for index, row in enumerate(reader, start=1):
            name = row["Name"]
            phone = row["Number"]
            collectableamount = row["Amount"]
            address = row["Address"]
            product = row["Product"]
            
            tmpl = Template(template)
            rendered_html = tmpl.render(name=name, phone=phone, collectableamount=collectableamount, address=address, product=product)
            
            output_filename = output_dir / f"{index}.html"
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                output_file.write(rendered_html)
            print(f"Generated: {output_filename}")

# Copy resources (logo.png and kalpurush.ttf) to output directory
def copy_resources():
    output_dir = Path('output')
    resources = ['logo.png', 'kalpurush.ttf']
    
    for resource in resources:
        resource_path = find_file(resource)
        if resource_path:
            shutil.copy(resource_path, output_dir / resource)
            print(f"Copied: {resource} to {output_dir / resource}")
        else:
            print(f"Warning: {resource} not found in search paths.")

# Process all CSV files in the "divaniz_invoice" directory
for csv_path in glob.glob('divaniz_invoice/*.csv'):
    generate_html_from_csv(csv_path, html_template)

# Copy logo.png and kalpurush.ttf to output directory
copy_resources()

# Merge individual HTML files into a single merge.html file
merged_output_path = Path("output/merge.html")
with open(merged_output_path, "w", encoding="utf-8") as merged_file:
    # Write the full HTML structure, including styles
    merged_file.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n')
    merged_file.write('<meta charset="UTF-8">\n')
    merged_file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    merged_file.write('<title>Merged Labels</title>\n')
    # Embed the CSS directly
    merged_file.write('<style>\n')
    merged_file.write("""
    @page {
        size: 50mm 75mm;
        margin: 0;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Kalpurush', 'Poppins', sans-serif;
    }

    body {
        font-family: 'Kalpurush', 'Poppins', sans-serif;
        font-size: 7pt;
    }

    .parcel-label {
        width: 50mm;
        height: 75mm;
        background: #fff;
        border: none;
        border-radius: 2mm;
        padding: 3mm;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        page-break-after: always;
    }

    .label-logo {
        height: 5mm;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }

    .label-logo img {
        max-height: 100%;
        max-width: 100%;
        height: 7mm;
        width: auto;
        display: block;
        margin: auto;
    }

    .customer-info {
        border: 1px solid #000;
        border-radius: 1mm;
        padding: 2mm;
        font-size: 7pt;
        line-height: 1.2;
    }

    .customer-info p {
        margin-bottom: 1mm;
        font-size: 7pt;
        color: #000;
    }

    .mrcnt-name p {
        font-size: 7pt;
        text-align: center;
        color: #111;
    }

    .label-footer {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 6pt;
        color: #000;
        margin-top: 1mm;
    }

    @font-face {
        font-family: 'Kalpurush';
        src: url('kalpurush.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
    }
    """)
    merged_file.write('</style>\n')
    merged_file.write('</head>\n<body>\n')
    
    # Loop through each HTML file in the output directory (skip merge.html)
    for html_file in sorted(glob.glob("output/*.html")):
        if "merge.html" in html_file:
            continue
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Extract the inner HTML of <body>
            body_start = content.find("<body>")
            body_end = content.find("</body>")
            if body_start != -1 and body_end != -1:
                inner_body = content[body_start + len("<body>"):body_end].strip()
                merged_file.write(inner_body + "\n\n")
    
    merged_file.write('</body>\n</html>')

print(f"Generated: {merged_output_path}")
