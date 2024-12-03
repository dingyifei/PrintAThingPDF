# Label Processor - PrintAThing

This repository contains an example of using SumatraPDF and python to split and print PDFs downloaded from printathing.com for printing the shipping labels and packing sheets.

## Overview
1. **pdf_splitter.py** - Splits a PDF file into two separate PDF files.
2. **pdf_printer.py** - Prints a PDF file using a specified printer.
3. **pdf_split_print_script.py** - Combines the functionalities of the splitter and printer to split a PDF and print the resulting files using different printers.

### Dependencies
The programs rely on the following dependencies:
- `SumatraPDF` - A free, open-source PDF viewer that can be used to print PDF files from the command line.
- `PyPDF2` - A Python library for reading, writing, and splitting PDF files.
- `pywin32` - A Python library for interacting with the Windows API, used for printer management.

To install these dependencies, you can use the following command:

```sh
pip install -r requirements.txt
```

Then place the `SumatraPDF.exe` portable executable in the same directory as the scripts.

SumatraPDF Download: [SumatraPDF](https://www.sumatrapdfreader.org/free-pdf-reader.html)

## Usage

### 1. pdf_splitter.py
The `pdf_splitter.py` script is used to split an input PDF into two separate files: the first PDF containing all pages except the last one, and the second PDF containing the rotated and cropped last page.

**Usage**:
```sh
python pdf_splitter.py -i <input_pdf_path> -o1 <output_pdf1_path> -o2 <output_pdf2_path>
```
- `-i` or `--input`: Path to the input PDF file.
- `-o1` or `--output1`: Path to save the first output PDF file.
- `-o2` or `--output2`: Path to save the second output PDF file.

### 2. pdf_printer.py
The `pdf_printer.py` script allows printing a PDF file using a specified printer. It also supports listing available printers.

**Usage**:

To list all available printers:
```sh
python pdf_printer.py --list-printers
```

To print a PDF file:
```sh
python pdf_printer.py -p <printer_name> -i <input_pdf_path>
```
- `-p` or `--printer`: Name of the printer to use.
- `-i` or `--input`: Path to the PDF file to print.

### 3. pdf_split_print_script.py
The `pdf_split_print_script.py` script combines the functionalities of the `pdf_splitter.py` and `pdf_printer.py` scripts. It takes a directory of PDF files, splits each PDF into two separate files, and then sends them to two different printers for printing.

**Usage**:
```sh
python pdf_split_print_script.py -p1 <printer1_name> -p2 <printer2_name> -i <input_directory> -o <output_directory>
```
- `-p1` or `--printer1`: Name of the first printer to print the first split PDF.
- `-p2` or `--printer2`: Name of the second printer to print the second split PDF.
- `-i` or `--input`: Path to the directory containing input PDF files.
- `-o` or `--output`: Path to the directory where split PDF files will be saved.

### Example
Suppose you have a folder of PDF files that need to be split and printed by two different printers. The `pdf_split_print_script.py` allows you to easily automate this task by running the following command:

```sh
python pdf_split_print_script.py -p1 "Printer1" -p2 "Printer2" -i "input_pdfs" -o "output_pdfs"
```
This will split each PDF file in the `input_pdfs` directory and save the results in the `output_pdfs` directory, then print the first and second PDFs using `Printer1` and `Printer2` respectively.

## Notes
- **Windows Only**: The printer interaction is implemented using the `win32print` library, which is specific to Windows.
- **SumatraPDF Required**: The `pdf_printer.py` script uses SumatraPDF to send print commands. Make sure SumatraPDF is installed and accessible from the command line.

## License
This project is licensed under the MIT License. Feel free to use and modify the code as needed.

## Contact
For any questions or issues, please contact the repository owner or create an issue in the repository.