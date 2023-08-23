import pdfplumber
from openpyxl import Workbook
import os
import re

def grade_to_marks(grade):
    if grade == 'O':
        return '90 - 100'
    elif grade == 'A+':
        return '80 - 89'
    elif grade == 'A':
        return '70 - 79'
    elif grade == 'B+':
        return '60 - 69'
    elif grade == 'B':
        return '50 - 59'
    elif grade == 'C':
        return '45 - 49'
    elif grade == 'D':
        return '40 - 44'
    elif grade == 'F':
        return 'Below 40'
    elif grade == 'ABS':
        return '00'
    elif grade == 'M':
        return '00'
    else:
        return 'NA'

def calculate_equiv_percentage(cgpa):
    cgpa = float(cgpa)
    if 4.5 < cgpa <= 10:
        equiv_percentage = (cgpa - 0.50) * 10
    elif 4 <= cgpa <= 4.5:
        equiv_percentage = 40
    else:
        equiv_percentage = cgpa * 10
    return equiv_percentage


def extract_data_from_pdf(pdf_path):
    data = {"Name": "", "RollNo.": "", "Subjects": {}, "SGPA": "NA", "CGPA": "NA", "SGPA Equivalent": "NA", "CGPA Equivalent": "NA"}
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

    lines = text.split('\n')
    
    name_match = re.search(r'Name:\s*([\w\s]+)', text)
    roll_match = re.search(r'Roll No.:\s*(\w+)', text)
    sgpa_match = re.search(r'SGPA:\s*([\d.]+)', text)
    cgpa_match = re.search(r'CGPA:\s*([\d.]+)', text)
    sgpa_equiv_match = re.search(r'Equiv% : (\d+\.\d+)', text)
    
    if name_match:
        data["Name"] = name_match.group(1).strip()
    if roll_match:
        data["RollNo."] = roll_match.group(1).strip()
    if sgpa_match:
        data["SGPA"] = sgpa_match.group(1).strip()
    if cgpa_match:
        data["CGPA"] = cgpa_match.group(1).strip()
    if sgpa_equiv_match:
        data["SGPA Equivalent"] = sgpa_equiv_match.group(1).strip()

    subjects_start = False
    for line in lines:
        if "Total Credits:" in line:
            subjects_start = False
        if subjects_start and line:
            parts = line.split()
            if len(parts) >= 5:
                subject_name = " ".join(parts[:-5])
                grade = parts[-4]
                marks = grade_to_marks(grade)
                data["Subjects"][subject_name] = marks
        if "Subjects" in line:
            subjects_start = True

    return data

def save_to_excel(data, excel_file_path):
    workbook = Workbook()
    sheet = workbook.active

    headers = ["Name", "RollNo."] + list(data["Subjects"].keys()) + ["SGPA", "CGPA"]
    sheet.append(headers)

    row_data = [data["Name"], data["RollNo."]] + list(data["Subjects"].values()) + [data["SGPA"], data["CGPA"]]
    sheet.append(row_data)

    workbook.save(excel_file_path)
    print(f"Data extracted from PDFs and saved to '{excel_file_path}'.")

# Path to the folder containing PDF files
pdf_folder = r"C:\Users\bhaba\my preparation\books\COMMERCE\Results\Marks_Downloader\mark_sheets_2nd_Semester"
output_excel_file = "output.xlsx"

pdf_files = [file for file in os.listdir(pdf_folder) if file.lower().endswith(".pdf")]

output_excel_path = os.path.join(pdf_folder, output_excel_file)

workbook = Workbook()
sheet = workbook.active

headers = ["Name", "RollNo."]
for pdf_file in pdf_files:
    extracted_data = extract_data_from_pdf(os.path.join(pdf_folder, pdf_file))
    headers += list(extracted_data["Subjects"].keys()) + ["SGPA", "SGPA Equivalent Percentage", "CGPA", "CGPA Equivalent Percentage"]

sheet.append(headers)

for pdf_file in pdf_files:
    extracted_data = extract_data_from_pdf(os.path.join(pdf_folder, pdf_file))
    row_data = [extracted_data["Name"], extracted_data["RollNo."]]
    sgpa = extracted_data["SGPA"]
    cgpa = extracted_data["CGPA"]
    row_data += list(extracted_data["Subjects"].values()) + [sgpa, calculate_equiv_percentage(sgpa), cgpa, calculate_equiv_percentage(cgpa)]
    sheet.append(row_data)

workbook.save(output_excel_path)
print(f"Data extracted from PDFs and saved to '{output_excel_path}'.")
