import csv
import os
import json


def check_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Design', 'SKU' , 'Product Name' , 'SIZE' , 'COLOR' , 'MRP' , 'Item Type' , 'Pattern' , 'BRAND', 'HSN CODE'])
            print('File created successfully')
        return True
    else:
        return False
    
def add_data(file_path, data):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    print('Data added successfully')
 
def read_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)  # print all rows
            
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
    operation = input('Enter operation to Perform(Or Leave Empty to Default):\n1. Add Data\n2. Read Data\n>>> ').strip() or '1'
    if operation == '1':
        while True:
            flag = input('Press Enter to Input Data or type "exit" to Exit: ').strip().lower()
            if flag == 'exit':
                break
            else:
                data = []
                data.append(input(f'Enter Design Number: {0}: ').upper())
                data.append(input(f'Enter SKU: {1}: '))
                data.append(input(f'Enter Product Name: {2}: '))
                data.append(input(f'Enter Size: {3}: ').upper())    
                data.append(input(f'Enter Color: {4}: ').upper())
                while True:
                    try:
                        data.append(float(input(f'Enter MRP: {5}: ')))
                        break
                    except ValueError:
                        print("Invalid MRP. Please enter a number.")
                data.append(input(f'Enter Item Type(Shirt, T-Shirt, Polo, Pants etc.): {6}: '))
                data.append(input(f'Enter Pattern(Or Leave Empty for Plain): {7}: ').strip() or 'Plain')
                data.append(input(f'Enter Brand(Or Leave empty to enter {brand}): {8}: ').strip() or brand)
                data.append(input(f'Enter HSN Code: {9}: '))
                add_data(file_path, data)
        print('Data added successfully')
    elif operation == '2':
        read_data(file_path)
    else:    
        print('Invalid Operation')
        exit()