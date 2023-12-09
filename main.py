import os
import pdfplumber
import csv

def compare_pdfs(source_folder, target_folder, csv_file, log_file):
    # Read filenames from the CSV
    with open(csv_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        filenames = [row[0] for row in reader]

    with open(log_file, 'w') as log:
        for filename in filenames:
            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(target_folder, filename)

            if os.path.isfile(source_path) and os.path.isfile(target_path):
                source_text = extract_text_from_pdf(source_path)
                target_text = extract_text_from_pdf(target_path)

                if source_text == target_text:
                    log.write(f"File {filename} is identical.\n")
                else:
                    log.write(f"File {filename} is different:\n")
                    log.write(f"Reason: Text content does not match.\n\n")


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

if __name__ == "__main__":
    source_folder = "source/"
    target_folder = "target/"
    csv_file = "file_list.csv"
    log_file = "comparison_log.txt"

    compare_pdfs(source_folder, target_folder, csv_file, log_file)
