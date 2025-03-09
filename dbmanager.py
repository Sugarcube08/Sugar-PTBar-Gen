import csv
import os
import json

def check_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['DESIGN NO.', 'SKU', 'Product Name', 'SIZE', 'COLOR', 'MRP', 'Item Type', 'Pattern', 'BRAND', 'HSN CODE', 'REMARKS(leave empty)'])
            print('File created successfully')
        return True
    else:
        return False
    
def add_data(file_path, data):
    file_empty = os.stat(file_path).st_size == 0
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if file_empty:
            writer.writerow(['DESIGN NO.', 'SKU', 'Product Name', 'SIZE', 'COLOR', 'MRP', 'Item Type', 'Pattern', 'BRAND', 'HSN CODE', 'REMARKS(leave empty)'])
        writer.writerow(data)
    print('Data added successfully')
 
def read_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)  # print all rows

def DB_cleaner(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    # Remove duplicates
    header = data[0]
    unique_data = [header]
    seen = set()
    for row in data[1:]:
        row_tuple = tuple(row)
        if row_tuple != tuple(header) and row_tuple not in seen:
            seen.add(row_tuple)
            unique_data.append(row)
    
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(unique_data)
    print('Database cleaned successfully')

def load_config(config_path):
    """Loads brand configuration from JSON file."""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Configuration file missing or invalid. Using default values.")
        return {"Brand": "Unknown"}

if __name__ == '__main__':
    file_path = "assets/database.csv"
    config = load_config("assets/config.json")
    brand = config.get("Brand", "Unknown")
    check_file(file_path)
    operation = input('Enter operation to Perform(Or Leave Empty to Default):\n1. Add Data Manually \n2. Add Data By File(Automatically)\n3. Read Data\n>>> ').strip() or '1'
    if operation == '1':
        while True:
            flag = input('Press Enter to Input Data or type "exit" to Exit: ').strip().lower()
            if flag == 'exit':
                break
            else:
                data = []
                data.append(input('Enter Design Number: ').upper())
                data.append(input('Enter SKU: '))
                data.append(input('Enter Product Name: '))
                data.append(input('Enter Size: ').upper())    
                data.append(input('Enter Color: ').upper())
                while True:
                    try:
                        data.append(float(input('Enter MRP: ')))
                        break
                    except ValueError:
                        print("Invalid MRP. Please enter a number.")
                data.append(input('Enter Item Type(Shirt, T-Shirt, Polo, Pants etc.): '))
                data.append(input('Enter Pattern(Or Leave Empty for Plain): ').strip() or 'Plain')
                data.append(input(f'Enter Brand(Or Leave empty to enter {brand}): ').strip() or brand)
                data.append(input('Enter HSN Code: '))
                add_data(file_path, data)
        print('Data added successfully')
    elif operation == '2':
        sub_operation = input('Enter Operation to Perform:\n1. Upload File\n2. Download Format File (CSV)\n>>> ').strip()
        if sub_operation == '1':
            file_name = input('Enter File Name(Or leave Empty for Default Location "DB-Upload.csv"): ').strip() or 'DB-Upload.csv'
            with open(file_name, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    add_data(file_path, row)
            print('Data Uploaded Successfully')
        elif sub_operation == '2':
            with open('DB-Upload.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['DESIGN NO.', 'SKU', 'Product Name', 'SIZE', 'COLOR', 'MRP', 'Item Type', 'Pattern', 'BRAND', 'HSN CODE', 'REMARKS(leave empty)'])
            print('Format File Created Successfully')
    elif operation == '3':
        read_data(file_path)
    else:    
        print('Invalid Operation')
        exit()
    
    # Clean the database after any operation
    DB_cleaner(file_path)