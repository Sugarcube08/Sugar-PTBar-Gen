import json
import os
import csv
from reportlab.lib.pagesizes import mm
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import code128  # Import barcode generator

def auto_wrap_text(canvas, text, x, y, max_width, font_size , font="Helvetica", line_spacing=2):
    """
    Automatically wraps text within max_width and draws it on the canvas.
    - canvas: PDF canvas object
    - text: The text to wrap
    - x, y: Starting position
    - max_width: Maximum width before wrapping
    - font: Font type
    - font_size: Font size
    - line_spacing: Space between wrapped lines
    """
    words = text.split()
    current_line = ""
    lines = []
    
    canvas.setFont(font, font_size)

    for word in words:
        if canvas.stringWidth(current_line + " " + word, font, font_size) < max_width:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for i, line in enumerate(lines):
        canvas.drawString(x, y - (i * (font_size + line_spacing)), line)  # Draw wrapped text line

def get_datetime_filename(base, ext):
    """Generate a filename with current datetime for uniqueness."""
    dt = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{base}_{dt}{ext}"

# DO NOT THOUCH THIS FUNCTION NEVER EVER IN THE HELL, 
# TRESSPASSERS WILL BE SHOT DEAD
# SURVIVORS WILL BE SHOT AGAIN
def create_UniLabel(output_pdf, product, color, size, Net_Qty, mrp, Address , barcode_value, logo_path):
    """
    Creates a label PDF and appends it to output_pdf (labels.pdf)
    """
    # Always generate a new file with a datetime-based name
    output_pdf = get_datetime_filename('UNI_labels', '.pdf')

    # Label dimensions (in mm)
    label_width, label_height = 80 * mm, 55 * mm

    # Define temp file path
    temp_pdf = os.path.join(os.getcwd(), "temp/temp.pdf")

    # Ensure temp directory exists
    os.makedirs("temp", exist_ok=True)

    # ✅ Create a PDF canvas for temp file
    c = canvas.Canvas(temp_pdf, pagesize=(label_width, label_height))

    # Draw logo (centered at top)
    if logo_path and os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        logo_width, logo_height = 45 * mm, 8 * mm  # Adjust as needed
        c.drawImage(logo, (label_width - logo_width) / 2, label_height - 10 * mm, width=logo_width, height=logo_height)

    # Define text position
    text_x, text_y = 3 * mm, label_height - 13* mm
    max_width = label_width - 10 * mm
    # Add text fields
    c.setFont("Courier", 8)
    auto_wrap_text(c, f"Product Code : {product}", text_x, text_y, max_width,font_size=8)
    c.drawString(text_x, text_y - 4 * mm, f"Color : {color}")
    c.setFont("Courier", 12)
    c.drawString(text_x, text_y - 9 * mm, f"Size    : {size}")
    c.setFont("Courier", 8)
    c.drawString(text_x, text_y - 12 * mm, f"Net Qty   : {Net_Qty}")
    c.setFont("Courier-Bold", 14)
    c.drawString(text_x, text_y - 17 * mm, f"MRP   : {mrp}")
    c.setFont("Courier", 10)
    auto_wrap_text(c, f"Address : {Address}", text_x, text_y - 22 * mm, max_width, font_size=8)
    # Generate and draw barcode (centered)
    barcode = code128.Code128(barcode_value, barWidth=0.15 * mm, barHeight=6 * mm)
    barcode_x = (label_width - barcode.width) / 2  # Center horizontally
    barcode_y = text_y - 35 * mm  # Adjust barcode position
    barcode.drawOn(c, barcode_x, barcode_y)

    # Draw barcode value (centered below barcode)
    c.setFont("Courier-Bold", 10)
    barcode_text_x = (label_width - c.stringWidth(barcode_value, "Courier-Bold", 10)) / 2
    barcode_text_y = barcode_y - 4 * mm  # Position slightly below barcode
    c.drawString(barcode_text_x, barcode_text_y, barcode_value)

    # ✅ Save the temporary PDF file
    c.showPage()
    c.save()

    # ✅ Move temp PDF to output_pdf (no merging)
    os.replace(temp_pdf, output_pdf)
    print(f"✅ {output_pdf} created.")


# DO NOT THOUCH THIS FUNCTION NEVER EVER IN THE HELL, 
# TRESSPASSERS WILL BE SHOT DEAD
# SURVIVORS WILL BE SHOT AGAIN
def create_PTLabel(output_pdf, product, d_no, size, mrp, barcode_value, logo_path):
    """
    Creates a label PDF and appends it to output_pdf (labels.pdf)
    """
    # Always generate a new file with a datetime-based name
    output_pdf = get_datetime_filename('PT_labels', '.pdf')

    # Label dimensions (in mm)
    label_width, label_height = 38.7 * mm, 25 * mm

    # Define temp file path
    temp_pdf = os.path.join(os.getcwd(), "temp/temp.pdf")

    # Ensure temp directory exists
    os.makedirs("temp", exist_ok=True)

    # ✅ Create a PDF canvas for temp file
    c = canvas.Canvas(temp_pdf, pagesize=(label_width, label_height))

    # Draw logo (centered at top)
    if logo_path and os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        logo_width, logo_height = 22 * mm, 5 * mm  # Adjust as needed
        c.drawImage(logo, (label_width - logo_width) / 2, label_height - 5 * mm, width=logo_width, height=logo_height)

    # Define text position
    text_x, text_y = 3 * mm, label_height - 8 * mm

    # Add text fields
    c.setFont("Helvetica", 8)
    c.drawString(text_x, text_y, f"Prod   : {product}")
    c.drawString(text_x, text_y - 3 * mm, f"D. No. : {d_no}")
    c.drawString(text_x, text_y - 6 * mm, f"Size    : {size}")
    c.drawString(text_x, text_y - 9 * mm, f"MRP   : {mrp}")

    # Generate and draw barcode (centered)
    barcode = code128.Code128(barcode_value, barWidth=0.3 * mm, barHeight=3 * mm)
    barcode_x = (label_width - barcode.width) / 2  # Center horizontally
    barcode_y = text_y - 13 * mm  # Adjust barcode position
    barcode.drawOn(c, barcode_x, barcode_y)

    # Draw barcode value (centered below barcode)
    c.setFont("Courier-Bold", 8)
    barcode_text_x = (label_width - c.stringWidth(barcode_value, "Courier-Bold", 8)) / 2
    barcode_text_y = barcode_y - 3 * mm  # Position slightly below barcode
    c.drawString(barcode_text_x, barcode_text_y, barcode_value)

    # ✅ Save the temporary PDF file
    c.showPage()
    c.save()

    # ✅ Move temp PDF to output_pdf (no merging)
    os.replace(temp_pdf, output_pdf)
    print(f"✅ {output_pdf} created.")


def create_ptfile(data, ptfile_path=None):
    # Always generate a new file with a datetime-based name if not provided
    if ptfile_path is None:
        ptfile_path = get_datetime_filename('ptfile', '.csv')
    with open(ptfile_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['BarcodeNo.', 'Season', 'Group', 'HSN Code','Item Type', 'Item Detail', 'Brand', 'Sub Brand', 'Pattern', 'Design', 'Section', 'Color', 'Sub Category', 'Unit','Available Quantity',  'Size', 'Discount %', 'MRP','Rate', 'Amount', 'GST %',  'Purchase Type', 'Supplier Name', 'Fomate', 'LT', 'Barcode Type', 'Location', 'Invoice No', 'Date'])
        writer.writerow(data)
    return ptfile_path

def date_time():
    """Returns the current date and time in 'dd-mm-yyyy HH:MM:SS' format."""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
  
def load_config(config_path):
    """Loads brand configuration from JSON file."""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Configuration file missing or invalid. Using default values.")
        return {"Brand": "Unknown"}
    
def rate_calculator(mrp, discount, type):
    if type == "1":
        amount = mrp - (mrp * (discount / 100))
        if amount < 1049:
            gst = 100*5/(100+5)
            rate = amount - (amount * (gst/100))
            return rate 
        else:
            gst = 100*12/(100+12)
            rate = amount - (amount * (gst/100))
            return rate
    else:
        amount = mrp - (mrp * (discount / 100))
        if amount < 999:
            rate = amount + (amount * 0.05)
            return rate
        else:
            rate = amount + (amount * 0.12)
    
def GST_calculator(rate, type):
    if type == "1":
        if rate < 1049:           
            return 5
        else:
           return 12
        
    else:
        if rate < 999:
            return 5
        else:
            return 12
    
def search_csv(csv_filename, search_column, search_value):
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get(search_column, "").strip().lower() == search_value.strip().lower():
                return row  # Return the matching row
    return None  # No match found

def amount_calculator(mrp, discount):
    amount = mrp - (mrp * (discount / 100))
    return amount

def barcode_updater():
    config = load_config("assets/config.json")
    barcode = int(config.get("Barcode-No", "Unknown"))
    barcode += 1
    config["Barcode-No"] = str(barcode)
    with open("assets/config.json", "w") as file:
        json.dump(config, file)
    return str(barcode)

def ptfile_data(search_value):
    # Search for product in CSV file
    csv_filename = "assets/database.csv"
    search_column = "SKU"
    product = search_csv(csv_filename, search_column, search_value)
    config = load_config("assets/config.json")
    data = []
    data.append(barcode_updater())
    data.append(config.get("Season", "").strip() or "")
    data.append(config.get("Group", "Unknown").strip() or "")
    data.append(product.get("HSN CODE", "Unknown").strip() or "")
    data.append(product.get("Item Type", "Unknown").strip() or "")
    data.append(product.get("SKU", "Unknown").strip() or "")
    data.append(config.get("Brand", "Unknown").strip())
    data.append(product.get("Sub Brand", "").strip() or "")
    data.append(product.get("Pattern", "Unknown").strip() or "")
    data.append(product.get("Design", "Unknown").strip() or "")
    data.append(product.get("Section", "").strip() or "")
    data.append(product.get("COLOR", "Unknown").strip() or "")
    data.append(product.get("Sub Category", "").strip() or "")
    data.append(product.get("Unit", "PCS").strip() or "PCS")
    data.append("1")
    data.append(product.get("SIZE", "Unknown").strip() or "")
    data.append(input("Enter Discount %: ").strip() or "0")
    data.append(int(product.get("MRP", "Unknown").strip() or ""))
    type = input("Enter Type of GST\n1. for INCLUSIVE\n2. for EXCLUSIVE\n(Leave Leave Empty for1)\n>>> ").strip() or "1"
    data.append(rate_calculator(float(product.get("MRP", "Unknown").strip()), float(data[16]), type))
    data.append(amount_calculator(float(product.get("MRP", "Unknown").strip()), float(data[16])))
    data.append(GST_calculator(data[18], type))
    data.append(input("Enter Purchase Type(Or Leave of GST): ").strip() or "GST")
    data.append(config.get("Supplier Name", "Unknown"))
    data.append(input("Enter Format(Or Leave for SHOP PURCHASE): ").strip() or "SHOP PURCHASE")
    data.append(input("Enter LT(Or Leave for 0): ").strip() or "0")
    data.append(config.get("Barcode Type", "Unknown"))
    data.append(config.get("Location", "Unknown"))
    data.append(input("Enter Invoice No: ").strip() or "0")
    data.append(date_time())
    create_PTLabel(
                    output_pdf="PT_labels.pdf",
                    product=data[5].upper(),
                    d_no=data[9].upper(),
                    size=data[15].upper(),
                    mrp=data[17],
                    barcode_value=data[0],
                    logo_path="assets/logo.png"  # Ensure this file exists
                )
    if data[14] == "1":
        create_ptfile(data)
    else:
        for i in range(int(data[14])):
            data[0] = barcode_updater()
            create_ptfile(data)

def auto_ptfile_data(row, search_value):
    # Search for product in CSV file
    csv_filename = "assets/database.csv"
    search_column = "SKU"
    product = search_csv(csv_filename, search_column, search_value)
    print(product)
    config = load_config("assets/config.json")
    data = []
    
    # Error handling for row[3] (Available Quantity)
    available_qty_str = row[3].strip() if len(row) > 3 else ""
    try:
        available_qty = int(available_qty_str)
    except (ValueError, TypeError):
        print(f"Invalid or missing Available Quantity: '{available_qty_str}'. Skipping row: {row}")
        return

    if available_qty == 0:
        print("Leaving Due to No inventory")
    elif available_qty == 1:
        data.append(barcode_updater())
        data.append(config.get("Season", "").strip() or "")
        data.append(config.get("Group", "Unknown").strip() or "")
        data.append(product.get("HSN CODE", "Unknown").strip() or "")
        data.append(product.get("Item Type", "Unknown").strip() or "")
        data.append(product.get("SKU", "Unknown").strip() or "")
        data.append(product.get("BRAND", "Unknown").strip())
        data.append(product.get("Sub Brand", "").strip() or "")
        data.append(product.get("Pattern", "Unknown").strip() or "")
        data.append(product.get("DESIGN NO.", "Unknown").strip() or "")
        data.append(product.get("Section", "").strip() or "")
        data.append(product.get("COLOR", "Unknown").strip() or "")
        data.append(product.get("Sub Category", "").strip() or "")
        data.append(product.get("Unit", "PCS").strip() or "PCS")
        data.append("1")
        data.append(product.get("SIZE", "Unknown").strip() or "")
        data.append(row[1].strip() or "0")
        data.append(int(product.get("MRP", "Unknown").strip() or ""))
        type = row[2].strip() or "1"
        data.append(rate_calculator(float(product.get("MRP", "Unknown").strip()), float(data[16]), type))
        data.append(amount_calculator(float(product.get("MRP", "Unknown").strip()), float(data[16])))
        data.append(GST_calculator(data[18], type))
        data.append(row[4].strip() or "GST")
        data.append(config.get("Supplier Name", "Unknown"))
        data.append(row[5].strip() or "SHOP PURCHASE")
        data.append(row[6].strip() or "0")
        data.append(config.get("Barcode Type", "Unknown"))
        data.append(config.get("Location", "Unknown"))
        data.append(row[7].strip() or "0")
        data.append(date_time())
        create_ptfile(data)
        create_PTLabel(
                        output_pdf="PT_labels.pdf",
                        product=data[5].upper(),
                        d_no=data[9].upper(),
                        size=data[15].upper(),
                        mrp=data[17],
                        barcode_value=data[0],
                        logo_path="assets/logo.png"  # Ensure this file exists
                    )
    else:
        for i in range(available_qty):
            data.append(barcode_updater())
            data.append(config.get("Season", "").strip() or "")
            data.append(config.get("Group", "Unknown").strip() or "")
            data.append(product.get("HSN CODE", "Unknown").strip() or "")
            data.append(product.get("Item Type", "Unknown").strip() or "")
            data.append(product.get("SKU", "Unknown").strip() or "")
            data.append(product.get("BRAND", "Unknown").strip())
            data.append(product.get("Sub Brand", "").strip() or "")
            data.append(product.get("Pattern", "Unknown").strip() or "")
            data.append(product.get("DESIGN NO.", "Unknown").strip() or "")
            data.append(product.get("Section", "").strip() or "")
            data.append(product.get("COLOR", "Unknown").strip() or "")
            data.append(product.get("Sub Category", "").strip() or "")
            data.append(product.get("Unit", "PCS").strip() or "PCS")
            data.append(row[3].strip() or "0")
            data.append(product.get("SIZE", "Unknown").strip() or "")
            data.append(row[1].strip() or "0")
            data.append(int(product.get("MRP", "Unknown").strip() or ""))
            type = row[2].strip() or "1"
            data.append(rate_calculator(float(product.get("MRP", "Unknown").strip()), float(data[16]), type))
            data.append(amount_calculator(float(product.get("MRP", "Unknown").strip()), float(data[16])))
            data.append(GST_calculator(data[18], type))
            data.append(row[4].strip() or "GST")
            data.append(config.get("Supplier Name", "Unknown"))
            data.append(row[5].strip() or "SHOP PURCHASE")
            data.append(row[6].strip() or "0")
            data.append(config.get("Barcode Type", "Unknown"))
            data.append(config.get("Location", "Unknown"))
            data.append(row[7].strip() or "0")
            data.append(date_time())
            create_ptfile(data)
            create_PTLabel(
                            output_pdf="PT_labels.pdf",
                            product=data[5].upper(),
                            d_no=data[9].upper(),
                            size=data[15].upper(),
                            mrp=data[17],
                            barcode_value=data[0],
                            logo_path="assets/logo.png"  # Ensure this file exists
                        )

def Unilabel(data):
    config = load_config("assets/config.json")
    product = search_csv("assets/database.csv", "SKU", data)
    if product:
        create_UniLabel(
            output_pdf=None,  # output_pdf is ignored, always datetime-named
            product=product.get("SKU", "Unknown"),
            color=product.get("COLOR", "Unknown").upper(),
            size=product.get("SIZE", "Unknown").upper(),
            Net_Qty=1,
            mrp=product.get("MRP", "Unknown"),
            Address=config.get("Address", "Unknown"),
            barcode_value=product.get("SKU", "Unknown").strip(),
            logo_path="assets/logo.png"  # Ensure this file exists
        )
    else:
        print("Product Not Found")
        return

def manual_mode():
      while True:
        operation = input("Enter Operation to Do\n1. for UNI-Barcode\n2. for PT-Barcode\n0. for Exit \n>>> ")
        if operation == "1":
            while True: 
                data = input("Enter of Scan SKU to print or type exit to leave: ")
                if data.lower() == "exit":
                    break
                elif data.lower() != "exit":
                    Unilabel(data)
                    continue
                else:
                    print("Invalid Input")
                    continue
        elif operation == "2":
            while True:
                flag = input("Press Enter to Scan SKU or type exit to leave: ").strip().lower()
                if flag == "exit":
                    break
                else:
                    while True:
                        search_value = input("Enter or Scan SKU to search: ")
                        if search_value:
                            ptfile_data(search_value)
                            break
                        else:
                            print("No SKU Entered")
                            continue   
        elif operation == "0":
            break

def auto_mode():
    while True:
        operation = input("Enter Operation to Do\n1. for UNI-Barcode\n2. for PT-Barcode\n0. for Exit \n>>> ")
        if operation == "1":
            while True: 
                sub_operation = input("Choose Operation\n1. for Upload file\n2. for Download Example CSV\n0. for Exit\n>>> ")
                if sub_operation == "1":
                    file = input("Enter the file name to upload: ")
                    with open(file, 'r') as f:
                        reader = csv.reader(f)
                        next(reader)
                        for row in reader:
                            # Always generate a new UNI label file for each row
                            Unilabel(row[0])
                
                elif sub_operation == "2":
                    # Auto-renaming logic for UNI-operation.csv using datetime
                    filename = get_datetime_filename('UNI-operation', '.csv')
                    with open(filename, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['SKU'])
                    print(f"Example CSV saved as: {filename}")
                elif sub_operation == "0":
                    break
                else:
                    print("Invalid Operation")
                    continue
        elif operation == "2":
            while True:
                sub_operation = input("Choose Operation\n1. for Upload file\n2. for Download Example CSV\n0. for Exit\n>>> ")
                if sub_operation == "1":
                    file = input("Enter the file name to upload: ")
                    impression_rows = []
                    impression_header = None
                    with open(file, 'r') as f:
                        reader = csv.reader(f)
                        header = next(reader)
                        impression_header = header + ['REMARK']
                        for row in reader:
                            error_remark = ''
                            # Check for essential fields (columns with *)
                            essentials_idx = [i for i, col in enumerate(header) if '*' in col]
                            missing_essentials = [header[i] for i in essentials_idx if len(row) <= i or not row[i].strip()]
                            if missing_essentials:
                                error_remark = f"Missing essential fields: {', '.join(missing_essentials)}"
                                impression_rows.append(row + [error_remark])
                                continue
                            try:
                                print(row, row[0])
                                auto_ptfile_data(row, row[0])
                            except Exception as e:
                                error_remark = f"Processing error: {str(e)}"
                                impression_rows.append(row + [error_remark])
                                continue
                    # Write impression file if any errors
                    if impression_rows:
                        impression_filename = get_datetime_filename('import_impression', '.csv')
                        with open(impression_filename, 'w', newline='') as impf:
                            writer = csv.writer(impf)
                            writer.writerow(impression_header)
                            writer.writerows(impression_rows)
                        print(f"Impression file generated: {impression_filename}")
                
                elif sub_operation == "2":
                    # Auto-renaming logic for PT-operation.csv using datetime
                    filename = get_datetime_filename('PT-operation', '.csv')
                    with open(filename, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['SKU*', 'Discount %*','GST Type (1. Inclusive or 2. Exclusive)*', 'Available Quantity*', 'Purchase Type(GST or other or Leave Blank)', 'Format(e.g. SHOP PURCHASE or leave blank)', 'LT', 'Invoice No*'])
                    print(f"Example CSV saved as: {filename}")
                elif sub_operation == "0":
                    break
                else:
                    print("Invalid Operation")
                    continue
        elif operation == "0":
            break
    

if __name__ == '__main__':
    while True:
        mode = input("Enter Mode\n1. for Manual\n2. for Automatic Mode\n>>> ")
        if mode == "1":
            manual_mode()
        elif mode == "2":
            auto_mode()
        else:
            print("Invalid Mode")
            continue
        break