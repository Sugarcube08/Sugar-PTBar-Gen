# 🏷️ Sugar-PTBar-Gen 

## 🚀 Introduction
This project is a **Bulk Label & PT file Generator** that creates formatted product labels based on a **CSV database**. It automatically generates barcodes, calculates rates with discounts and GST, and stores the data for future reference. The tool integrates multiple components for smooth functionality.

## ✨ Features
- 📄 Generate **product labels** with barcodes in **PDF format**.
- 📂 Maintain and manage a **database of products**.
- ⚙️ Configure brand and supplier details via a JSON-based **config file**.
- 🔄 Automatic **barcode generation and updating**.
- 📑 Merge newly generated labels into a single PDF.

---

## 📌 Instructions
### 1️⃣ **Installation**
Ensure you have Python installed. Then, install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2️⃣ **Setup Configuration**
Before using the system, configure the **config.json** file by running:
```bash
python config.py
```
This will prompt you to enter details such as:
- 🏠 Address
- 🏭 Supplier Name
- 🖼️ Logo Path
- 🔢 Barcode Type
- 🏷️ Brand
- 🏢 Group
- 🔖 Barcode Number

The configuration file is stored at `assets/config.json`.

### 3️⃣ **Prepare the Database**
Run the following command to create the initial product database:
```bash
python dbmanager.py
```
This will generate `assets/database.csv` and allow you to add products.

---

## 🛠️ How to Use
### 🔹 **1. Running the Main Script**
Execute the main script:
```bash
python main.py
```
You will be prompted to choose an operation:
- `1️⃣`: Generate a **unique barcode**.
- `2️⃣`: Search the database and generate a **product label**.

### 🔹 **2. Generating Labels**
- 🗂️ The script fetches **product details** from `database.csv`.
- 🔍 The barcode is generated and printed on the label.
- 📑 Labels are stored in `labels.pdf`.

### 🔹 **3. Searching for Products**
You can search for a product in the database by SKU.
```bash
Enter or Scan SKU to search: <SKU>
```
If found, it retrieves the details and proceeds to label generation.

---

## 🔧 How to Handle
### 🔹 **1. Modifying the Configuration**
- ✏️ Edit `config.json` manually or rerun `config.py`.
- 🛑 Ensure the JSON format remains valid.

### 🔹 **2. Editing the Database**
- 📌 Run `dbmanager.py` to add new product data.
- 📊 Open `database.csv` in a spreadsheet editor for bulk edits.

### 🔹 **3. Resetting Barcodes**
- ✏️ Open `config.json` and modify the `Barcode-No` value.
- 🔄 This resets the barcode counter.

---

## ⚠️ Cautions
- ❌ **Do not manually edit the `labels.pdf` file** while the script is running.
- 📂 Ensure all **CSV and JSON files are correctly formatted**.
- ⚠️ The script **overwrites existing labels**—make backups if needed.
- 🛑 When running `config.py`, ensure you provide **valid input**, or configuration issues may arise.
- 🚫 Avoid **deleting the `temp/` folder**, as it stores intermediate label files.

---

## 🙌 Acknowledgment
Special thanks to **ReportLab**, **PyPDF2**, and the **Python community** for providing excellent libraries for barcode and PDF generation. 💡

---

## 📜 Requirements
The project dependencies are listed in `requirements.txt`:
```
reportlab
pypdf2
```
To install them, use:
```bash
pip install -r requirements.txt
```

---

## 📜 License
This project is open-source. Modify and distribute as needed.

---
# Made with ❤️ by SugarCube
---

---
## ☕ Support Me
If you like this project, consider buying me
 a coffee!
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20Me-orange?style=flat-square&logo=buy-me-a-coffee)](https://www.buymeacoffee.com/sugarcube08)   
---
