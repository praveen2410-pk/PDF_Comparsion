import os
import pdfplumber
import time
import csv
from reportlab.lib.pagesizes import letter

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

                if source_size == target_size and source_page_count == target_page_count:
                    identical_count += 1
                    log.write("Identical,File compared successfully\n")
                else:
                    non_identical_count += 1
                    log.write("Non Identical,")

                    if source_size != target_size:
                        log.write("File size does not match.")
                    elif source_page_count != target_page_count:
                        log.write("Page count does not match.")

                    log.write("\n")

    end_time = time.time()
    print("\nComparison summary:")
    print(f"Processed {processed_files} files.")
    print(f"Identical: {identical_count} files.")
    print(f"Non Identical: {non_identical_count} files.")
    print(f"Script end time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")

if __name__ == "__main__":
    source_folder = "source/"
    target_folder = "target/"
    csv_file = "file_list.csv"
    log_file = "comparison_log.txt"
    print("hi....")

    compare_pdfs(source_folder, target_folder, csv_file, log_file)
