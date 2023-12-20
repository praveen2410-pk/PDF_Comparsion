# PDF Comparison Utility

## Overview

This Python script facilitates the comparison of PDF files between a local source folder and a remote server. The script logs results, highlighting identical and non-identical files based on size and page count. It employs `pdfplumber` for PDF handling and `paramiko` for SSH connections.

## Features

- Compares PDF files in a source folder with corresponding files on a remote server.
- Logs results, indicating identical and non-identical files along with specific differences.
- Provides error handling for issues like missing source files or connection problems with the target server.

## Usage

1. Set the source folder, target server details, CSV file listing file pairs, and log file paths in the script.
2. Run the script (`compare_pdfs.py`) to perform PDF comparisons.
3. Review the generated log file (`comparison_log.txt`) for detailed results.

## Getting Started

### Prerequisites

- Install required libraries:

  ```bash
  pip install pdfplumber paramiko
