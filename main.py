import difflib
import filecmp
import os

import PyPDF2
import pandas
import pdfplumber
import nltk
import time
import csv
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader

def get_page_count(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return len(pdf.pages)

def convert_bytes_to_human_readable(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            break
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} {unit}"

def compare_pdfs(source_folder, target_folder, csv_file, log_file):
    processed_files = 0
    identical_count = 0
    non_identical_count = 0

    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        with open(log_file, 'w') as log:
           with open("Results.csv", 'w') as log:
            log.write("Source_FileName,Traget file name,Source_FileSize,Target_FileSize,Source_PageCount,Target_PageCount,Identical,Comments\n")
            
            for row in csv_reader:
                source_filename = row["Source_FileName"]
                target_filename = row["Traget file name"]

                source_path = os.path.join(source_folder, f"{source_filename}.pdf")
                target_path = os.path.join(target_folder, f"{target_filename}.pdf")

                processed_files += 1

                if os.path.isfile(source_path):
                    source_size = os.path.getsize(source_path)
                    source_page_count = get_page_count(source_path)
                else:
                    log.write(f"{source_filename},{target_filename},,-,-,-,-,Source file not found.\n")
                    continue

                if os.path.isfile(target_path):
                    target_size = os.path.getsize(target_path)
                    target_page_count = get_page_count(target_path)
                else:
                    log.write(f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},,-,-,-,Target file not found.\n")
                    continue

                log.write(f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},{convert_bytes_to_human_readable(target_size)},{source_page_count},{target_page_count},")

                # if source_size == target_size and source_page_count == target_page_count:
                if source_page_count == target_page_count:
                    identical_count += 1

                    # Input PDF file paths
                    pdf_path1 = source_filename
                    pdf_path2 = target_filename

                    # Output PDF file path with differing words highlighted in red
                    output_path = 'out.pdf'
                    compare_and_highlight(source_path, target_path, output_path)

                    # Paths to the two text files you want to compare
                    file1_path = r'text1.txt'
                    file2_path = r'text2.txt'

                    mismatched_lines = compare_lines_in_files(file1_path, file2_path)

                    if mismatched_lines:
                        print("Differences between the files:")
                        log.write("Differences between the files.\n")
                        # for line in mismatched_lines:
                        #     print(line)
                    else:
                        print("No differences found between the files.")
                        log.write("No differences found between the files.\n")

                else:
                    non_identical_count += 1
                    log.write("Non Identical,")

                    if source_size != target_size:
                        log.write("File size does not match.\n")
                    elif source_page_count != target_page_count:
                        log.write("Page count does not match.\n")

                    log.write("\n")


    end_time = time.time()
    print("\nComparison summary:")
    print(f"Processed {processed_files} files.")
    print(f"Identical: {identical_count} files.")
    print(f"Non Identical: {non_identical_count} files.")
    print(f"Script end time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")

import hashlib
from difflib import SequenceMatcher

def hash_file(fileName1, fileName2):
    # Use hashlib to store the hash of a file
    h1 = hashlib.sha1()
    h2 = hashlib.sha1()

    with open(fileName1, "rb") as file:
        # Use file.read() to read the size of file
        # and read the file in small chunks
        # because we cannot read the large files.
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h1.update(chunk)

    with open(fileName2, "rb") as file:
        # Use file.read() to read the size of file a
        # and read the file in small chunks
        # because we cannot read the large files.
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h2.update(chunk)

        # hexdigest() is of 160 bits
        print(h1.hexdigest(), h2.hexdigest())
        return h1.hexdigest(), h2.hexdigest()


import fitz  # PyMuPDF
from textblob import TextBlob


# Function to extract text from a PDF

def extract_text(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()
    return text



# Function to compare PDFs and highlight differing words in red

def compare_and_highlight(pdf_path1, pdf_path2, output_path):
    nltk.download('punkt')

    text1 = extract_text(pdf_path1)
    text2 = extract_text(pdf_path2)

    file2write = open("text1.txt", 'w' , encoding='utf-8')
    file2write.write(text1.strip().rstrip())
    file2write.close()

    file2write = open("text2.txt", 'w' ,encoding='utf-8')
    file2write.write(text2.strip().rstrip())
    file2write.close()



def compare_lines_in_files(file1_path, file2_path):
    try:
        with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
            lines_file1 = file1.readlines()
            lines_file2 = file2.readlines()

            mismatched_lines = []

            # Compare each line in file1 to all lines in file2
            for line_num, line1 in enumerate(lines_file1, start=1):
                line1 = line1.strip()  # Remove leading/trailing whitespace
                found_match = False

                for line_num2, line2 in enumerate(lines_file2, start=1):
                    line2 = line2.strip()  # Remove leading/trailing whitespace

                    # Perform a case-insensitive comparison
                    if line1.lower() == line2.lower():
                        found_match = True
                        break

                if not found_match:
                    mismatched_lines.append(f"Line {line_num} in File 1: '{line1}' has no match in File 2")

            # Compare each line in file2 to all lines in file1 (vice versa)
            for line_num2, line2 in enumerate(lines_file2, start=1):
                line2 = line2.strip()  # Remove leading/trailing whitespace
                found_match = False

                for line_num, line1 in enumerate(lines_file1, start=1):
                    line1 = line1.strip()  # Remove leading/trailing whitespace

                    # Perform a case-insensitive comparison
                    if line2.lower() == line1.lower():
                        found_match = True
                        break

                if not found_match:
                    mismatched_lines.append(f"Line {line_num2} in File 2: '{line2}' has no match in File 1")

            return mismatched_lines

    except FileNotFoundError:
        print("One or both files not found.")
        return []


if __name__ == "__main__":
    source_folder = "source/"
    target_folder = "target/"
    csv_file = "file_list.csv"
    log_file = "comparison_log.txt"
    print("hi....")

    compare_pdfs(source_folder, target_folder, csv_file, log_file)
    # Compare PDFs and highlight differing words in red



