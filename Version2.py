import os
import pdfplumber
import csv
import difflib

def convert_bytes_to_human_readable(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            break
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} {unit}"

def compare_pdfs(source_folder, target_folder, csv_file, log_file):
    # Prepare CSV file for writing
    with open(csv_file, 'w', newline='') as csv_out:
        fieldnames = ['Source_FileName', 'Traget file name', 'Source_FileSize', 'Target_FileSize',
                      'Source_PageCount', 'Target_PageCount', 'Identical', 'Comments']
        csv_writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
        csv_writer.writeheader()

        # Read CSV file
        with open("file_list.csv", 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                source_filename = row.get("Source_FileName", "")
                target_filename = row.get("Traget file name", "")

                source_path = os.path.join(source_folder, source_filename + ".pdf")
                target_path = os.path.join(target_folder, target_filename + ".pdf")

                print(f"Processing files: {source_path}, {target_path}")

                if not os.path.isfile(source_path) or not os.path.isfile(target_path):
                    print(f"Files {source_filename} or {target_filename} do not exist.")
                    csv_writer.writerow({'Source_FileName': source_filename,
                                         'Traget file name': target_filename,
                                         'Source_FileSize': '-',
                                         'Target_FileSize': '-',
                                         'Source_PageCount': '-',
                                         'Target_PageCount': '-',
                                         'Identical': 'Non Identical',
                                         'Comments': 'Files do not exist'})
                    continue

                source_size = os.path.getsize(source_path)
                target_size = os.path.getsize(target_path)

                if source_size == target_size:
                    source_page_count = get_page_count(source_path)
                    target_page_count = get_page_count(target_path)

                    if source_page_count == target_page_count:
                        source_content = extract_content_from_pdf(source_path)
                        target_content = extract_content_from_pdf(target_path)

                        match_percentage = calculate_content_match_percentage(source_content, target_content)

                        with open(log_file, 'a', encoding='utf-8') as log:
                            log.write(f"Processing files: {source_path}, {target_path}\n")
                            log.write(f"Source and target file sizes match ({convert_bytes_to_human_readable(source_size)}).\n")
                            log.write(f"Source and target page counts match ({source_page_count} pages).\n")

                            if source_content == target_content:
                                log.write(f"Files {source_filename} and {target_filename} are identical.\n")
                                identical = 'Identical'
                                comments = 'File compared successfully'
                            else:
                                differences = get_content_differences(source_content, target_content)
                                log.write(f"Files {source_filename} and {target_filename} are different.\n")
                                log.write(f"Changes:\n")
                                log.write(differences)
                                log.write(f"Content match percentage: {match_percentage:.2f}%\n")
                                identical = 'Non Identical'
                                comments = 'Content does not match'
                            log.write("\n")

                            print(f"Files {source_filename} and {target_filename} processed.")
                            print(f"Source and target file sizes match ({convert_bytes_to_human_readable(source_size)}).")
                            print(f"Source and target page counts match ({source_page_count} pages).")

                            if source_content == target_content:
                                print(f"Files {source_filename} and {target_filename} are identical.")
                            else:
                                print(f"Files {source_filename} and {target_filename} are different.")
                                print(f"Content match percentage: {match_percentage:.2f}%")
                        csv_writer.writerow({'Source_FileName': source_filename,
                                             'Traget file name': target_filename,
                                             'Source_FileSize': convert_bytes_to_human_readable(source_size),
                                             'Target_FileSize': convert_bytes_to_human_readable(target_size),
                                             'Source_PageCount': source_page_count,
                                             'Target_PageCount': target_page_count,
                                             'Identical': identical,
                                             'Comments': comments})
                    else:
                        with open(log_file, 'a', encoding='utf-8') as log:
                            log.write(f"Processing files: {source_path}, {target_path}\n")
                            log.write(f"Source and target file sizes match ({convert_bytes_to_human_readable(source_size)}).\n")
                            log.write(f"Source and target page counts do not match.\n")
                            log.write(f"Target file does not match with the source file.\n\n")

                            print(f"Processing files: {source_path}, {target_path}")
                            print(f"Source and target file sizes match ({convert_bytes_to_human_readable(source_size)}).")
                            print(f"Source and target page counts do not match.")
                            print(f"Target file does not match with the source file.")
                        csv_writer.writerow({'Source_FileName': source_filename,
                                             'Traget file name': target_filename,
                                             'Source_FileSize': convert_bytes_to_human_readable(source_size),
                                             'Target_FileSize': convert_bytes_to_human_readable(target_size),
                                             'Source_PageCount': source_page_count,
                                             'Target_PageCount': target_page_count,
                                             'Identical': 'Non Identical',
                                             'Comments': 'Page count does not match'})
                else:
                    with open(log_file, 'a', encoding='utf-8') as log:
                        log.write(f"Processing files: {source_path}, {target_path}\n")
                        log.write(f"Source and target file sizes do not match.\n")
                        log.write(f"Target file does not match with the source file.\n\n")

                        print(f"Processing files: {source_path}, {target_path}")
                        print(f"Source and target file sizes do not match.")
                        print(f"Target file does not match with the source file.")
                    csv_writer.writerow({'Source_FileName': source_filename,
                                         'Traget file name': target_filename,
                                         'Source_FileSize': convert_bytes_to_human_readable(source_size),
                                         'Target_FileSize': convert_bytes_to_human_readable(target_size),
                                         'Source_PageCount': '-',
                                         'Target_PageCount': '-',
                                         'Identical': 'Non Identical',
                                         'Comments': 'File size does not match'})

def get_page_count(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page_count = len(pdf.pages)
    return page_count

def extract_content_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            # You can include other content extraction logic here (e.g., images, values)

        return text

def get_content_differences(source_content, target_content):
    d = difflib.Differ()
    diff = list(d.compare(source_content.splitlines(), target_content.splitlines()))
    return '\n'.join(diff)

def calculate_content_match_percentage(source_content, target_content):
    match_percentage = difflib.SequenceMatcher(None, source_content, target_content).ratio() * 100
    return match_percentage

if __name__ == "__main__":
    source_folder = "source/"
    target_folder = "target/"
    csv_file = "comparison_results.csv"
    log_file = "comparison_log.txt"

    # Clear log file and CSV file before running the comparison
    open(log_file, 'w', encoding='utf-8').close()
    open(csv_file, 'w', newline='', encoding='utf-8').close()

    compare_pdfs(source_folder, target_folder, csv_file, log_file)
