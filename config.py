import json
import os

def check_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)
            print('File created successfully\n')
        return True
    else:
        return False

def add_data(file_path, data):
    with open(file_path, 'r') as file:
        file_data = json.load(file)
    with open(file_path, 'w') as file:
        file_data.update(data)
        json.dump(file_data, file)
    print('Data added successfully\n')
    
if __name__ == "__main__":
    file_path = "assets/config.json"
    check_file(file_path)
    while True:
        data = {}
        data['Address'] = input('Enter Address: ')
        data['Supplier Name'] = input('Enter Supplier Name: ')
        data['logo.png'] = input('Enter Logo Path: ')
        data['Barcode Type'] = input('Enter Barcode Type: ')
        data['Location'] = input('Enter Location: ')
        data['Brand'] = input('Enter Brand: ')
        data['Group'] = input('Enter Group: ')
        data['Barcode-No'] = input('Enter Last Barcode-No: ')
        print(data)
        confirm = input('Confirm Data Entry(Y/N): ').strip().lower()
        if confirm == 'y':
            add_data(file_path, data)   
            print('JSON Configured added successfully')
            break
        else:
            print('Retry Configuring File\n')
            continue
    print('Data added successfully')