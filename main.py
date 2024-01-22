import glob
import logging
import os
import random
from multiprocessing import freeze_support
from urllib import response

import PySimpleGUI as sg
import nltk
import numpy as np
import pandas as pd
import paramiko
import pdfplumber
import requests


column_names = ["SourceFileName", "TargetFileName", "SourceFileSize",
                "TargetFileSize", "SourcePageCount", "TargetPageCount","Status","Comments"]

overview = pd.DataFrame(columns=column_names)

overview.columns = column_names

loggers = None

def log_file_console():
    # logger_name = inspect.stack()[1][3]
    # logger = logging.getLogger(logger_name)
    # logger.setLevel(logging.INFO)
    # fh = logging.FileHandler("automation.log", mode='w')
    # sh = logging.StreamHandler(sys.stdout)
    # formater = logging.Formatter("%(asctime)s [%(levelname)s] : %(message)s")
    # fh.setFormatter(formater)
    # logger.addHandler(fh)
    # logger.addHandler(sh)
    # # logger.basicConfig(level=,
    # #                     format="%(asctime)s [%(levelname)s] %(message)s",
    # #                     handlers=[
    # #                         logging.FileHandler("logs.log"),
    # #                         logging.StreamHandler(sys.stdout)
    # #                     ])
    # return logger
        import multiprocessing, logging
        logger = multiprocessing.get_logger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter( \
            '[%(asctime)s| %(levelname)s| %(processName)s] %(message)s')
        handler = logging.FileHandler('./automation.log')
        handler.setFormatter(formatter)

        # this bit will make sure you won't have
        # duplicated messages in the output
        if not len(logger.handlers):
            logger.addHandler(handler)
        return logger





if(loggers == None):
    loggers = log_file_console()

def create_logger(self):
        import multiprocessing, logging
        logger = multiprocessing.get_logger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter( \
            '[%(asctime)s| %(levelname)s| %(processName)s] %(message)s')
        handler = logging.FileHandler('logs/your_file_name.log')
        handler.setFormatter(formatter)

        # this bit will make sure you won't have
        # duplicated messages in the output
        if not len(logger.handlers):
            logger.addHandler(handler)
        return logger


    # Function to compare PDFs and highlight differing words in red
def compare_and_highlight(source_path, target_path,source_filename,target_filename):
            nltk.download('punkt')
            # source_path, target_path = t
            processed_files = 0
            identical_count =0
            non_identical_count = 0

            # source_path, target_path, output_path,processed_files,identical_count,non_identical_count,source_filename,target_filename = t
            # processed_files = 0
            # identical_count =0
            # non_identical_count = 0

            text1 = extract_text(source_path)
            text2 = extract_text(target_path)
            # lines_file1 = text1.readlines()
            # lines_file2 = text2.readlines()

            # text1.splitlines()
            # text2.splitlines()

            # file1write = open("text1.txt", 'w' , encoding='utf-8')
            # file1write.write(text1.strip())
            # file1write.close()

            # file2write = open("text2.txt", 'w' ,encoding='utf-8')
            # file2write.write(text2.strip())
            # file2write.close()
            # mismatched_lines = compare_lines_in_files(text1.splitlines(), text2.splitlines())
            # print(pdf_path1 + " :: " + pdf_path2)

            # processed_files += 1

            if os.path.isfile(source_path):
                source_size = os.path.getsize(source_path)
                source_page_count = get_page_count(source_path)

                if os.path.isfile(target_path):
                    target_size = os.path.getsize(target_path)
                    target_page_count = get_page_count(target_path)

                    logger.info(
                        f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},{convert_bytes_to_human_readable(target_size)},{source_page_count},{target_page_count},")
                    # log.write(
                    #     f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},{convert_bytes_to_human_readable(target_size)},{source_page_count},{target_page_count},")

                    mismatched_lines = compare_lines_in_files(text1.splitlines(), text2.splitlines())

                    # if source_size == target_size and source_page_count == target_page_count:
                    # if source_page_count == target_page_count:
                    # identical_count += 1
                    # Input PDF file paths
                    pdf_path1 = source_filename
                    pdf_path2 = target_filename

                    # Output PDF file path with differing words highlighted in red
                    output_path = 'out.pdf'

                        # data = [('bla', 1, 3, 7), ('spam', 12, 4, 8), ('eggs', 17, 1, 3)]
                        # data = [(source_path, target_path, output_path)]
                        # mismatched_lines = p.map(SampleDriver.compare_and_highlight, data)
                        # print(mismatched_lines)

                        # mismatched_lines = compare_lines_in_files(text1.splitlines(), text2.splitlines())
                        # if mismatched_lines:
                        #     non_identical_count += 1
                        #     # print("Differences between the files:")
                        #     logger.info("Differences between the files.\n")
                        #     # log.write("Differences between the files.\n")
                        #     for line in mismatched_lines:
                        #         print(line)
                        #
                        # else:
                        #     identical_count += 1
                        #     # print("No differences found between the files.")
                        #     logger.info("No differences found between the files.\n")
                        #     # log.write("No differences found between the files.\n")

            #         else:
            #             non_identical_count += 1
            #             # print("Non Identical")
            #             logger.info("Non Identical,")
            #             # log.write("Non Identical,")
            #
            #             if source_size != target_size:
            #                 # print("File size does not match.\n")
            #                 logger.info("File size does not match.\n")
            #                 # log.write("File size does not match.\n")
            #
            #             elif source_page_count != target_page_count:
            #                 # print("Page count does not match.\n")
            #                 logger.info("Page count does not match.\n")
            #                 # log.write("Page count does not match.\n")
            #
            #     else:
            #         non_identical_count += 1
            #         logger.info(
            #             f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},,-,-,-,Target file not found.\n")
            #         # log.write(
            #         #     f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},,-,-,-,Target file not found.\n")
            #         # print("Target file not found.\n");
            #
            # else:
            #     # print("Source file not found.\n");
            #     logger.info(f"{source_filename},{target_filename},,-,-,-,-,Source file not found.\n")
            #     # log.write(f"{source_filename},{target_filename},,-,-,-,-,Source file not found.\n")
            #     logger.info("\n")
            #     # log.write("\n")

            # print(" Compared ...")
            time.sleep(0.01)

            return mismatched_lines


def get_page_count(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return len(pdf.pages)


def convert_bytes_to_human_readable(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            break
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} {unit}"

import multiprocessing

import shutil, os

def compare_pdfs(data):
    try:
        row = data[1]
        source_folder = "source/"
        target_folder = "target/"

        local = "./target/"

        # source_folder, target_folder = t
        csv_file = "file_list.csv"
        log_file = "Results.txt"
        processed_files = 0
        identical_count = 0
        non_identical_count = 0

        source_filename = str(row.Source_FileName)
        target_filename = str(row.Target_FileName)

        try:
            environmentDF = pd.read_csv("TestData.csv")
            RunControlllist = environmentDF[environmentDF['RunControll'] == 'Yes']
            environmentlist = RunControlllist['ENVIRONMENT'].values
            Runlist = RunControlllist['RunControll'].values
            Execution_Modelist = RunControlllist['Execution_Mode'].values
            SOURCE_PATHllist = RunControlllist['SOURCE_PATH'].values
            TARGET_PATHlist = RunControlllist['TARGET_PATH'].values

            environment = environmentlist[0]
            RunControll = Runlist[0]
            Execution_Mode = Execution_Modelist[0]
            SOURCE_PATH = SOURCE_PATHllist[0]
            TARGET_PATH = TARGET_PATHlist[0]

            if (Execution_Mode == 'Remote'):

                # environmentDataDF = pd.read_csv("TestData.csv", sheet_name='ENV_Details')
                environmentData = RunControlllist.loc[RunControlllist['ENVIRONMENT'] == environment]
                IP_ADDRESS = (environmentData['IP'].values)[0]
                PORT_NUMBER = (environmentData['PORT'].values)[0]
                USERNAME = (environmentData['USERNAME'].values)[0]
                PASSWORD = (environmentData['PASSWORD'].values)[0]
                loggers.info('ENVIRONMENT: ' + environment)

                loggers.info("########### Creating Connection ##########")
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(IP_ADDRESS, int(PORT_NUMBER), username=USERNAME, password=PASSWORD)
                SFTP_client = client.open_sftp()
                # print("Remote System Connected Successfully....")
                loggers.info("Remote System Connected Successfully....")
                # targetfileDF = read_remoteFile_csv(SFTP_client, TARGET_PATH,TargetFileName)

                remotepath = TARGET_PATH + "/" + target_filename + ".pdf";
                # remotepath = TARGET_PATH + "/79466729_Black.pdf";
                # remote_file = SFTP_client.open(remotepath)
                # remote_file = "/home/pin/PDF_Bills/79418536_MobileServices.csv"
                # targetfileDF = pd.read_csv(remote_file, dtype=str, on_bad_lines='skip')
                # print(targetfileDF)

                # targetTempStrPath = "./target/temp/" + target_filename + "_temp" + str(random_number) + ".pdf"

                random_number = random.randint(1, 1000)
                SFTP_client.get(remotepath,               "./target/temp/" + target_filename + "_temp" + str(random_number)+".pdf");
                target_path = os.path.join("./target/temp/",f"{target_filename+ "_temp" + str(random_number)}.pdf")

                SFTP_client.close()

            elif (Execution_Mode == "Local"):
                # targetfileDF = pd.read_csv("Dumps\\TARGET\\" + target_filename + ".csv", dtype=str, on_bad_lines='skip')
                # print(targetfileDF)
                target_path = os.path.join(local, f"{target_filename}.pdf")

        except Exception as e:
            print("Unable to connect remote ip " + IP_ADDRESS)
            print(e)
            loggers.error(e)
            overview_DF = pd.DataFrame(
                [[source_filename, target_filename, "0.00 B", "0.00 B",
                  0,
                  0,"Not Matching", e]])

        if SOURCE_PATH == "":
            source_path = os.path.join(local, f"{source_filename}.pdf")
        else:
            source_path = os.path.join(SOURCE_PATH, f"{source_filename}.pdf")

        # data.append((source_path, target_path,"output.txt",processed_files,identical_count,non_identical_count,source_filename,target_filename))

        # mismatched_lines = p.map(SampleDriver.compare_and_highlight, data)
        # mismatched_lines = SampleDriver.compare_and_highlight(source_path,target_path,source_filename,target_filename)
        # for val in mismatched_lines:
        #             print(val)

        processed_files += 1

        try:
            if os.path.isfile(source_path):
                source_size = os.path.getsize(source_path)
                source_page_count = get_page_count(source_path)

                if os.path.isfile(target_path):
                    target_size = os.path.getsize(target_path)
                    target_page_count = get_page_count(target_path)

                    loggers.info(
                        f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},{convert_bytes_to_human_readable(target_size)},{source_page_count},{target_page_count},")
                    # log.write(
                    #     f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},{convert_bytes_to_human_readable(target_size)},{source_page_count},{target_page_count},")

                    if source_page_count == target_page_count:
                        # identical_count += 1

                        # Input PDF file paths
                        pdf_path1 = source_filename
                        pdf_path2 = target_filename

                        # Output PDF file path with differing words highlighted in red
                        output_path = 'out.pdf'

                        # process = multiprocessing.Process(target=SampleDriver.compare_and_highlight, args=(source_path, target_path, output_path))
                        # result = process.map(target=SampleDriver.compare_and_highlight, args = (source_path, target_path, output_path))
                        # mismatched_lines =  compare_pdfs(source_folder, target_folder, csv_file, log_file)
                        # print(result)

                        # numbers = [1, 5, 9]
                        # pool = multiprocessing.Pool(processes=1)
                        # print(pool.map(SampleDriver.compare_and_highlight,[[source_path, target_path, output_path]]))

                        # data = [('bla', 1, 3, 7), ('spam', 12, 4, 8), ('eggs', 17, 1, 3)]
                        # data = [(source_path, target_path, output_path)]
                        # mismatched_lines = p.map(SampleDriver.compare_and_highlight, data)
                        # print(mismatched_lines)

                        mismatched_lines = compare_and_highlight(source_path, target_path, source_filename,
                                                                 target_filename)
                        # if variable.value:
                        if mismatched_lines:
                            non_identical_count += 1
                            print("Differences between the files:")
                            # loggers.info("Differences between the files.\n")
                            overview_DF = pd.DataFrame(
                                [[source_filename, target_filename, convert_bytes_to_human_readable(source_size),
                                  convert_bytes_to_human_readable(target_size), source_page_count, target_page_count,
                                  "Not Matching","Differences between the files"]])

                            # log.write("Differences between the files.\n")
                            # for line in mismatched_lines:
                            #     print(line)

                        else:
                            identical_count += 1
                            print("No differences found between the files.")
                            loggers.info("No differences found between the files.\n")
                            # log.write("No differences found between the files.\n")
                            overview_DF = pd.DataFrame(
                                [[source_filename, target_filename, convert_bytes_to_human_readable(source_size),
                                  convert_bytes_to_human_readable(target_size), source_page_count, target_page_count,
                                  "Matching","No differences found between the files"]])
                            # ''79342579_LA	79342579_LA.1	2.46 MB	2.46 MB.1	172	172.1	No differences found between the files.""


                    else:
                        non_identical_count += 1
                        # print("Non Identical")
                        loggers.info("Non Identical,")
                        # log.write("Non Identical,")

                        if source_size != target_size:
                            # print("File size does not match.\n")
                            loggers.info("File size does not match.\n")
                            # log.write("File size does not match.\n")
                            overview_DF = pd.DataFrame(
                                [[source_filename, target_filename, convert_bytes_to_human_readable(source_size),
                                  convert_bytes_to_human_readable(target_size), source_page_count,
                                  target_page_count,"Not Matching", "File size does not match."]])

                        elif source_page_count != target_page_count:
                            # print("Page count does not match.\n")
                            loggers.info("Page count does not match.\n")
                            # log.write("Page count does not match.\n")
                            overview_DF = pd.DataFrame(
                                [[source_filename, target_filename, convert_bytes_to_human_readable(source_size),
                                  convert_bytes_to_human_readable(target_size), source_page_count,
                                  target_page_count,"Not Matching", "Page count does not match."]])

                        loggers.info("\n")
                        # log.write("\n")

                else:
                    non_identical_count += 1
                    loggers.info(
                        f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},,-,-,-,Target file not found.\n")
                    # log.write(
                    #     f"{source_filename},{target_filename},{convert_bytes_to_human_readable(source_size)},,-,-,-,Target file not found.\n")
                    # print("Target file not found.\n");
                    overview_DF = pd.DataFrame(
                        [[source_filename, target_filename, convert_bytes_to_human_readable(source_size), "0.00 B",
                          source_page_count,
                          "0","Not Matching", "Target file not found."]])
                    # continue

            else:
                non_identical_count += 1
                # print("Source file not found.\n");
                loggers.info(f"{source_filename},{target_filename},,-,-,-,-,Source file not found.\n")
                # log.write(f"{source_filename},{target_filename},,-,-,-,-,Source file not found.\n")
                # continue
                if os.path.isfile(target_path):
                    target_size = os.path.getsize(target_path)
                    target_page_count = get_page_count(target_path)
                else:
                    target_size = 0
                    target_page_count = 0

                overview_DF = pd.DataFrame(
                    [[source_filename, target_filename, "0.00 B", convert_bytes_to_human_readable(target_size), "0",
                      target_page_count, "Not Matching","Source file not found."]])

            if (Execution_Mode == 'Remote'):
                if os.path.exists(target_path):
                    os.remove(target_path)
                    # print(target_path +" file delete...")
                else:
                    print(target_path+ " file does not exist")

        except:
            print("getting error while reading target file......")
            overview_DF = pd.DataFrame(
                [[source_filename, target_filename, convert_bytes_to_human_readable(source_size), "0.00 B",
                  source_page_count,
                  "0","Not Matching","Target file not found."]])


    except:
        print("issue in file comparison method..")
        logger.info("\n issue in file comparison method..")
        if (Execution_Mode == 'Remote'):
            SFTP_client.close()
        overview_DF = pd.DataFrame(
                [[source_filename, target_filename, "0.00 B", "0.00 B",
                  "0",
                  "0", "Not Matching","Source file not found."]])

    # end_time = time.time()
    # print("\nComparison summary:")
    # print(f"Processed {processed_files} files.")
    # print(f"Identical: {identical_count} files.")
    # print(f"Non Identical: {non_identical_count} files.")
    # print(f"Script end time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")

    return overview_DF

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

def compare_lines_in_files(file1_path,file2_path):

    try:
        # with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
        #     lines_file1 = file1.readlines()
        #     lines_file2 = file2.readlines()

        mismatched_lines = []
        mainloopbreakFlag = False

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

def create_logger():
    import multiprocessing, logging
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(\
        '[%(asctime)s| %(levelname)s| %(processName)s] %(message)s')
    handler = logging.FileHandler('./automation123.log')
    handler.setFormatter(formatter)

    # this bit will make sure you won't have
    # duplicated messages in the output
    if not len(logger.handlers):
        logger.addHandler(handler)
    return logger


logger = None

log_file_path = './' # Wherever your log files live
log_name = 'my_log'

def listener_configurer(log_name, log_file_path):
    """ Configures and returns a log file based on
    the given name

    Arguments:
        log_name (str): String of the log name to use
        log_file_path (str): String of the log file path

    Returns:
        logger: configured logging object
    """
    logger = logging.getLogger(log_name)

    fh = logging.FileHandler(
        os.path.join(log_file_path, f'{log_name}.log'), encoding='utf-8')
    fmtr = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmtr)
    logger.setLevel(logging.INFO)
    current_fh_names = [fh.__dict__.get(
        'baseFilename', '') for fh in logger.handlers]
    if not fh.__dict__['baseFilename'] in current_fh_names: # This prevents multiple logs to the same file
        logger.addHandler(fh)

    return logger

if(logger == None):
    logger = log_file_console()


def ClearLogs():
        if os.path.isdir('./'):
            filelist = glob.glob("./*.log")
            for f in filelist:
                open(f, 'w+')

import multiprocessing as mp
import requests
def getTargetDF(loggers,TargetFileName):

    try:
        environmentDF = pd.read_csv("TestData.csv")
        RunControlllist = environmentDF[environmentDF['RunControll'] == 'Yes']
        environmentlist = RunControlllist['ENVIRONMENT'].values
        Runlist = RunControlllist['RunControll'].values
        Execution_Modelist = RunControlllist['Execution_Mode'].values
        SOURCE_PATHllist =  RunControlllist['SOURCE_PATH'].values
        TARGET_PATHlist = RunControlllist['TARGET_PATH'].values
        local = "//DUMPS//REMOTE_TARGET//"

        environment = environmentlist[0]
        RunControll = Runlist[0]
        Execution_Mode = Execution_Modelist[0]
        SOURCE_PATH = SOURCE_PATHllist[0]
        TARGET_PATH = TARGET_PATHlist[0]

        if(Execution_Mode == 'Remote'):
            # environmentDataDF = pd.read_csv("TestData.csv", sheet_name='ENV_Details')
            environmentData = environmentDF.loc[environmentDF['ENVIRONMENT'] == environment]
            IP_ADDRESS = (environmentData['IP'].values)[0]
            PORT_NUMBER = (environmentData['PORT'].values)[0]
            USERNAME = (environmentData['USERNAME'].values)[0]
            PASSWORD = (environmentData['PASSWORD'].values)[0]
            loggers.info('ENVIRONMENT: ' + environment)

            loggers.info("########### Creating Connection ##########")
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(IP_ADDRESS, int(PORT_NUMBER), username=USERNAME, password=PASSWORD)
            SFTP_client = client.open_sftp()
            print("Remote System Connected Successfully....")
            loggers.info("Remote System Connected Successfully....")
            # targetfileDF = read_remoteFile_csv(SFTP_client, TARGET_PATH,TargetFileName)
            remotepath = TARGET_PATH+TargetFileName+".csv";
            emote_file = SFTP_client.open(remotepath)
            # targetfileDF = pd.read_csv(emote_file, dtype=str, on_bad_lines='skip')
            # print(df)
            with open('/tmp/metadata.pdf', 'wb') as f:
                f.write(response.content)
                for line in f:
                    print(line)

            # SFTP_client.close()

        elif(Execution_Mode == "Local"):
            targetfileDF = pd.read_csv("Dumps\\TARGET\\" + TargetFileName + ".csv", dtype=str, on_bad_lines='skip')
            # print(targetfileDF)

        return targetfileDF

    except Exception as e:
        # print("Unable to connect remote ip "+IP_ADDRESS)
        print(e)
        loggers.error(e)


if __name__ == "__main__":
    freeze_support()
    ClearLogs()
    logger.info("########### Execution Started ##########")
    start_time = time.time()
    print(f"Script end time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    logger.info(f"Script end time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    source_folder = "source/"
    target_folder = "target/"
    csv_file = "file_list.csv"
    log_file = "Results.txt"
    start_time = time.time()

    filename = "./Overview.csv"
    # opening the file with w+ mode truncates the file
    f = open(filename, "w+")
    f.close()

    DriverSheetDF = pd.read_csv("file_list.csv")
    # DriverSheetDF = DriverSheetDF[DriverSheetDF['RUN_CONTROL'] == 'YES']
    DriverSheetDF.fillna("NULL", inplace=True)
    logger.info('')
    logger.info('')
    print("Total Files Selected For Recon: " + str(DriverSheetDF.shape[0]))
    logger.info("Total Files Selected For Recon: " + str(DriverSheetDF.shape[0]))
    logger.info('')
    logger.info('')

    filelist = glob.glob(os.path.join(".\\target\\temp\\", "*.pdf"))
    for f in filelist:
        if os.path.exists(".\\target/temp\\"):
            os.remove(f)
        else:
            print("The file does not exist")

    num_workers = mp.cpu_count()
    print("num_workers : " + str(num_workers - 2))
    # pool = multiprocessing.Pool(num_workers - 2)  # Create a multiprocessing Pool
    pool = multiprocessing.Pool(1)
    result = list((pool.map(compare_pdfs,DriverSheetDF.iterrows())))

    # listener = multiprocessing.Process(target=compare_pdfs,
    #                                    args=(DriverSheetDF.iterrows()))
    # Send DB connections in the multiprocess pool
    # result = list((pool.map(partial(ProcessingFiles,sorceDBconn=DbSourceConnection), DriverSheetDF.iterrows())))

    pool.close()
    pool.join()

    # compare_pdfs(source_folder, target_folder, csv_file, log_file)
    overview = pd.concat(result)
    overview.index = np.arange(1, len(overview) + 1)
    overview.to_csv("./Overview.csv", index=False)
    # Load data from a CSV file into a Pandas DataFrame:
    dataFrame = pd.read_csv("./Overview.csv")

    # rename column names from the CSV file
    dataFrame.columns.values[0] = "SourceFileName"
    dataFrame.columns.values[1] = "TargetFileName"
    dataFrame.columns.values[2] = "SourceFileSize"
    dataFrame.columns.values[3] = "TargetFileSize"
    dataFrame.columns.values[4] = "SourcePageCount"
    dataFrame.columns.values[5] = "TargetPageCount"
    dataFrame.columns.values[6] = "Status"
    dataFrame.columns.values[7] = "Comments"

    # print("\nDisplaying updated column names : \n", res)

    dataFrame.to_csv("./Overview.csv", index=False)

    OverviewDF_Matching_Count = (dataFrame.loc[dataFrame['Status'] == "Matching"]).shape[0]
    OverviewDF_Not_Matching_Count = (dataFrame.loc[dataFrame['Status'] != "Matching"]).shape[0]
    # write html to file
    # text_file = open("./Overview.html", "w")
    # PassPercentage = round((int(OverviewDF_Matching_Count) / (int(OverviewDF_Matching_Count) + int(OverviewDF_Not_Matching_Count))) * 100,2)
    # html_text = Utilities.html_syntax(OverviewDF_Matching_Count, OverviewDF_Not_Matching_Count, PassPercentage,
    #                                   overview_html)
    # text = text_file.read();
    # print(text)

    end_time = time.time()
    print("\nComparison summary:")
    print(f"Processed {str(OverviewDF_Matching_Count+OverviewDF_Not_Matching_Count)} files.")
    print(f"Identical: {str(OverviewDF_Matching_Count)} files.")
    print(f"Non Identical: {str(OverviewDF_Not_Matching_Count)} files.")

    logger.info("\n")
    logger.info("\nComparison summary:")
    logger.info(f"Processed {str(OverviewDF_Matching_Count+OverviewDF_Not_Matching_Count)} files.")
    logger.info(f"Identical: {str(OverviewDF_Matching_Count)} files.")
    logger.info(f"Non Identical: {str(OverviewDF_Not_Matching_Count)} files.")
    logger.info(f"Script end time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    logger.info("\n")
    end_time = time.time()
    # end_time = time.time()
    TimeTaken = convert(end_time - start_time)

    logger.info("\n")

    logger.info("\n")
    logger.info('Time Taken For Execution:' + str(TimeTaken))

    logger.info("##################### Execution Completed in " + str(TimeTaken) + " ################")
    sg.Popup('Execution completed in ' + str(TimeTaken))
