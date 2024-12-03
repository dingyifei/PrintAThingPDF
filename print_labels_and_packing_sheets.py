import argparse
import os
from pdf_splitter import split_pdf
from pdf_printer import print_pdf

def main():
    parser = argparse.ArgumentParser(description="Split a PDF and print with different printers.")
    parser.add_argument("-p1", "--printer1", required=True, help="Name of the first printer")
    parser.add_argument("-p2", "--printer2", required=True, help="Name of the second printer")
    parser.add_argument("-i", "--input", required=True, help="Input directory containing PDF files")
    parser.add_argument("-o", "--output", required=True, help="Output directory to save split PDF files")
    args = parser.parse_args()

    input_directory = args.input
    output_directory = args.output

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file_name in os.listdir(input_directory):
        if file_name.lower().endswith(".pdf"):
            input_pdf_path = os.path.join(input_directory, file_name)
            output_pdf1_path = os.path.join(output_directory, f"{os.path.splitext(file_name)[0]}_1.pdf")
            output_pdf2_path = os.path.join(output_directory, f"{os.path.splitext(file_name)[0]}_2.pdf")

            # Split the PDF
            split_pdf(input_pdf_path, output_pdf1_path, output_pdf2_path)

            # Print the split PDFs
            print_pdf(args.printer1, output_pdf1_path)
            print_pdf(args.printer2, output_pdf2_path)

if __name__ == "__main__":
    main()