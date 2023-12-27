import csv
import inspect
import logging
import os
import sys

import PySimpleGUI as sg
import nltk
import pandas as pd
import pdfplumber

loggers =None

def log_file_console():
    logger_name=inspect.stack()[1][3]
    logger=logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    fh=logging.FileHandler("automation.log",mode='w')
    sh=logging.StreamHandler(sys.stdout)
    formater = logging.Formatter("%(asctime)s [%(levelname)s] : %(message)s")
    fh.setFormatter(formater)
    logger.addHandler(fh)
    logger.addHandler(sh)
    # logger.basicConfig(level=,
    #                     format="%(asctime)s [%(levelname)s] %(message)s",
    #                     handlers=[
    #                         logging.FileHandler("logs.log"),
    #                         logging.StreamHandler(sys.stdout)
    #                     ])
    return logger

if(loggers == None):
    loggers = log_file_console()

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

        df = pd.DataFrame()
        with open(log_file, 'w') as log:
          # with open("Results.csv", 'w') as log:
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
                    # print("Source file not found.\n");
                    loggers.info(f"{source_filename},{target_filename},,-,-,-,-,Source file not found.\n")
                    log.write(f"{source_filename},{target_filename},,-,-,-,-,Source file not found.\n")
                    continue

                if os.path.isfile(target_path):
                    target_size = os.path.getsize(target_path)
                    target_page_count = get_page_count(target_path)
                else:
                    non_identical_count += 1
                    loggers.info(f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},,-,-,-,Target file not found.\n")
                    log.write(f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},,-,-,-,Target file not found.\n")
                    # print("Target file not found.\n");
                    continue

                loggers.info(f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},{convert_bytes_to_human_readable(target_size)},{source_page_count},{target_page_count},")
                log.write(
                    f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},{convert_bytes_to_human_readable(target_size)},{source_page_count},{target_page_count},")
                # if source_size == target_size and source_page_count == target_page_count:
                if source_page_count == target_page_count:
                    # identical_count += 1

                    # Input PDF file paths
                    pdf_path1 = source_filename
                    pdf_path2 = target_filename

                    # Output PDF file path with differing words highlighted in red
                    output_path = 'out.pdf'
                    mismatched_lines = compare_and_highlight(source_path, target_path, output_path)

                    # Paths to the two text files you want to compare
                    # file1_path = r'text1.txt'
                    # file2_path = r'text2.txt'

                    # mismatched_lines = compare_lines_in_files(file1_path, file2_path)

                    if mismatched_lines:
                        non_identical_count += 1
                        # print("Differences between the files:")
                        loggers.info("Differences between the files.\n")
                        log.write("Differences between the files.\n")
                        # for line in mismatched_lines:
                            # print(line)

                    else:
                        identical_count += 1
                        # print("No differences found between the files.")
                        loggers.info("No differences found between the files.\n")
                        log.write("No differences found between the files.\n")

                else:
                    non_identical_count += 1
                    # print("Non Identical")
                    loggers.info("Non Identical,")
                    log.write("Non Identical,")

                    if source_size != target_size:
                        # print("File size does not match.\n")
                        loggers.info("File size does not match.\n")
                        log.write("File size does not match.\n")

                    elif source_page_count != target_page_count:
                        # print("Page count does not match.\n")
                        loggers.info("Page count does not match.\n")
                        log.write("Page count does not match.\n")

                    loggers.info("\n")
                    log.write("\n")

    df = pd.read_csv("Results.txt")
    df.to_csv("Results.csv", index=False)

    end_time = time.time()
    print("\nComparison summary:")
    print(f"Processed {processed_files} files.")
    print(f"Identical: {identical_count} files.")
    print(f"Non Identical: {non_identical_count} files.")
    print(f"Script end time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")

import hashlib
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
    # lines_file1 = text1.readlines()
    # lines_file2 = text2.readlines()

    # text1.splitlines()
    # text2.splitlines()

    # file1write = open("text1.txt", 'w' , encoding='utf-8')
    # file1write.write(text1.strip())
    # file1write.close()
    #
    # file2write = open("text2.txt", 'w' ,encoding='utf-8')
    # file2write.write(text2.strip())
    # file2write.close()
    mismatched_lines = compare_lines_in_files(text1.splitlines(), text2.splitlines())
    return mismatched_lines

def compare_lines_in_files(file1_path, file2_path):
    try:
        # with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
        #     lines_file1 = file1.readlines()
        #     lines_file2 = file2.readlines()

            mismatched_lines = []
            mainloopbreakFlag =  False

            # Compare each line in file1 to all lines in file2
            for line_num, line1 in enumerate(file1_path, start=1):
                line1 = line1.strip()  # Remove leading/trailing whitespace
                found_match = False

                for line_num2, line2 in enumerate(file2_path, start=1):
                    line2 = line2.strip()  # Remove leading/trailing whitespace

                    # Perform a case-insensitive comparison
                    if line1.lower() == line2.lower():
                        found_match = True
                        break

                if not found_match:
                    mismatched_lines.append(f"Line {line_num} in File 1: '{line1}' has no match in File 2")
                    mainloopbreakFlag = True
                    break

            # Compare each line in file2 to all lines in file1 (vice versa)
            for line_num2, line2 in enumerate(file2_path, start=1):
                line2 = line2.strip()  # Remove leading/trailing whitespace
                found_match = False
                if (mainloopbreakFlag):
                    break
                for line_num, line1 in enumerate(file1_path, start=1):
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

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


import time

if __name__ == "__main__":
    # print("########### Execution Started ###########")
    loggers.info("########### Execution Started ##########")
    start_time = time.time()
    print('Script start time: :' + str(start_time))

    source_folder = "source/"
    target_folder = "target/"
    csv_file = "file_list.csv"
    log_file = "Results.txt"
    print("Hi")
    compare_pdfs(source_folder, target_folder, csv_file, log_file)

    end_time = time.time()
    TimeTaken = convert(end_time - start_time)
    print('Time Taken For Execution:' + str(TimeTaken))
    logging.info('Time Taken For Execution:' + str(TimeTaken))
    # print("##################### Execution Completed in " + str(TimeTaken) + " ################")
    loggers.info("##################### Execution Completed in " + str(TimeTaken) + " ################")
    sg.Popup('Execution completed in ' + str(TimeTaken))
