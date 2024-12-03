import argparse
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path, output_pdf1_path, output_pdf2_path):
    try:
        # Read the input PDF
        reader = PdfReader(input_pdf_path)

        # Ensure the PDF has at least two pages
        if len(reader.pages) < 2:
            raise ValueError("The PDF must have at least two pages to split.")

        # Create PDF writers for each output file
        writer1 = PdfWriter()
        writer2 = PdfWriter()

        # Add all the pages from the input PDF except the last one to the first PDF
        for page in reader.pages[:-1]:
            writer1.add_page(page)

        # Rotate the last page by 90 degrees clockwise and crop to 4x6 inches
        label_page = reader.pages[-1]
        label_page.rotate(270)  # Rotate 90 degrees clockwise
        label_page.mediabox.lower_left = (82, 260)
        label_page.mediabox.upper_right = (432+82, 288+260)  # 4 inches x 72 dpi, 6 inches x 72 dpi

        # Add the rotated and cropped second page to the second PDF
        writer2.add_page(label_page)

        # Write the output PDFs
        with open(output_pdf1_path, 'wb') as output_pdf1:
            writer1.write(output_pdf1)

        with open(output_pdf2_path, 'wb') as output_pdf2:
            writer2.write(output_pdf2)

        print(f"Successfully split the PDF.\nFirst page saved as: {output_pdf1_path}\nSecond page saved as: {output_pdf2_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a PDF into two separate PDFs with the first and second pages.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input PDF file")
    parser.add_argument("-o1", "--output1", required=True, help="Path to the output PDF file for the first page")
    parser.add_argument("-o2", "--output2", required=True, help="Path to the output PDF file for the second page")

    args = parser.parse_args()

    split_pdf(args.input, args.output1, args.output2)