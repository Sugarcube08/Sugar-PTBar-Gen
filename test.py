import json
import os
import csv
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import code128  # Import barcode generator
from PyPDF2 import PdfReader, PdfWriter

def auto_mode():
    while True:
        OP = input("Enter Operation to Do\n1. for UNI-Barcode\n2. for PT-Barcode\n0. for Exit \n>>> ")
        if OP == "1":
            while True: 
                opr = input("Choose Operation\n1. for Upload file\n2. for Download Example CSV\n0. for Exit\n>>> ")
                if opr == "1":
                    with open('UNI-operation.csv', 'r') as f:
                        reader = csv.reader(f)
                        next(reader)
                        for row in reader:
                            print(*row)
                                    
                        
                elif opr == "2":
                    with open('UNI-operation.csv', 'w') as f:
                        writer = csv.writer(f)
                        writer.writerow(['SKU'])
                elif opr == "0":
                    break
                else:
                    print("Invalid Operation")
                    continue
        elif OP == "2":
            print("PT-Barcode")
            #ptfile_data()
        elif OP == "0":
            break
    
    
if __name__ == "__main__":
    auto_mode()