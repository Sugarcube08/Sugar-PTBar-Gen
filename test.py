import csv
import json
import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from barcode import Code128
from barcode.writer import ImageWriter

# Convert mm to pixels
def mm_to_pixels(mm, dpi=300):
    return int((mm / 25.4) * dpi)

# Search for a specific row in CSV
def search_csv(csv_filename, search_column, search_value):
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get(search_column, "").strip().lower() == search_value.strip().lower():
                return row  # Return the matching row
    return None  # No match found

# Generate barcode
def generate_barcode(sku, output_path):
    if not sku:
        print("⚠ SKU is empty! Barcode will not be generated.")
        return None
    barcode = Code128(sku, writer=ImageWriter())
    barcode_path = f"{output_path}.png"
    barcode.save(output_path)
    return barcode_path

# Generate a label with merged data
def generate_label(product, label_format_file, constant_data_file):
    # Load label format
    with open(label_format_file, "r") as file:
        label_format = json.load(file)

    # Load constant data
    with open(constant_data_file, "r") as file:
        constant_data = json.load(file)

    # Merge product data with constant data
    complete_data = {**constant_data, **product}

    dpi = label_format["dpi"]
    label_width_px = mm_to_pixels(label_format["label_size_mm"][0], dpi)
    label_height_px = mm_to_pixels(label_format["label_size_mm"][1], dpi)

    pdf_filename = "label.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=(label_width_px, label_height_px))

    # Create label image
    label = Image.new("RGB", (label_width_px, label_height_px), "white")
    draw = ImageDraw.Draw(label)

    # Load font
    try:
        font = ImageFont.truetype(label_format["font"], size=30)
    except OSError:
        print("⚠ Font not found! Using default font.")
        font = ImageFont.load_default()

    # Get positions from JSON
    positions = label_format.get("text_positions_mm", {})

    # Draw text on label
    for key, pos_mm in positions.items():
        pos_px = (mm_to_pixels(pos_mm[0], dpi), mm_to_pixels(pos_mm[1], dpi))
        text_value = complete_data.get(key, "N/A")  # Default to "N/A" if missing
        draw.text(pos_px, text_value, fill="black", font=font)

    # Generate barcode
    barcode_path = generate_barcode(product.get("SKU", ""), "barcode")
    if barcode_path and os.path.exists(barcode_path):
        barcode_img = Image.open(barcode_path)

        # Get barcode position
        barcode_x_px, barcode_y_px = mm_to_pixels(label_format["barcode_position_mm"][0], dpi), mm_to_pixels(label_format["barcode_position_mm"][1], dpi)
        label.paste(barcode_img, (barcode_x_px, barcode_y_px))

    # Save label as PNG and add to PDF
    label.save("temp_label.png", "PNG")
    c.drawInlineImage("temp_label.png", 0, 0, label_width_px, label_height_px)
    c.showPage()

    c.save()
    print(f"✅ Label saved as {pdf_filename}")
    
if __name__ == "__main__":

    # Ask user for search parameter
    csv_filename = "assets/database.csv"
    constant_data_file = "assets/config.json"
    label_format_file = "assets/UniBar.json"

    search_column = input("Enter column name to search (e.g., SKU, Brand, Product Name) or (leave empty for SKU): ").strip() or "SKU"
    search_value = input(f"Enter value to search in {search_column}: ").strip()

    # Search CSV for the matching row
    product = search_csv(csv_filename, search_column, search_value)

    if product:
        print("✅ Product found. Merging with constant data and generating label...")
        generate_label(product, label_format_file, constant_data_file)
    else:
        print("❌ No matching product found.")

