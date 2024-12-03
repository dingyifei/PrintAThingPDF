import win32print
import subprocess
import os
import argparse

def list_printers():
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    printer_names = [printer[2] for printer in printers]
    return printer_names

def print_pdf(printer_name, pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' does not exist.")
        return

    # Command to print using SumatraPDF, assuming it's installed
    command = f'"SumatraPDF.exe" -print-to "{printer_name}" "{pdf_path}"'
    try:
        subprocess.run(command, check=True, shell=True)
        print("Print job sent successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while printing: {e}")

def main():
    parser = argparse.ArgumentParser(description="Print PDF files using available printers.")
    parser.add_argument("--list-printers", action="store_true", help="List all available printers")
    parser.add_argument("-p", "--printer", type=str, help="Specify the printer name to use")
    parser.add_argument("-i", "--input", type=str, help="Specify the path to the PDF file to print")

    args = parser.parse_args()

    if args.list_printers:
        printers = list_printers()
        if not printers:
            print("No printers found.")
            return

        print("Available Printers:")
        for i, printer in enumerate(printers):
            print(f"{i + 1}. {printer}")
        return

    if args.printer and args.input:
        print_pdf(args.printer, args.input)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
