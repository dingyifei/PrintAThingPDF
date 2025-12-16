import argparse
import os
from PyPDF2 import PdfReader, PdfWriter
from pdf_printer import print_pdf


def process_pdf(input_pdf_path, output_pdf_path):
    """
    Process a 6-page PDF by:
    1. Removing pages 1 and 2
    2. Rotating pages 4 and 5 by 90 degrees clockwise
    """
    try:
        # Read the input PDF
        reader = PdfReader(input_pdf_path)

        # Ensure the PDF has exactly 6 pages
        if len(reader.pages) != 6:
            raise ValueError(f"The PDF must have exactly 6 pages. Found {len(reader.pages)} pages.")

        # Create a new PDF writer
        writer = PdfWriter()

        # Add pages 3, 4, 5, 6 (0-indexed: 2, 3, 4, 5) from the original PDF
        pages_to_keep = [2, 3, 4, 5]  # Original pages 3, 4, 5, 6

        for i, page_idx in enumerate(pages_to_keep):
            page = reader.pages[page_idx]

            # Check if this is page 4 or 5 in the original PDF (pages 2, 3 in our new PDF)
            if page_idx == 3 or page_idx == 4:  # Original pages 4 and 5
                # Rotate 90 degrees clockwise (270 degrees counterclockwise)
                page.rotate(270)

            writer.add_page(page)

        # Write the processed PDF
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)

        print(f"Successfully processed PDF. Output saved as: {output_pdf_path}")
        return True

    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Batch process 6-page PDFs by removing pages 1-2, rotating pages 4-5, and printing the results.")
    parser.add_argument("-i", "--input", required=True,
                        help="Input directory containing PDF files (each must be 6 pages)")
    parser.add_argument("-o", "--output", required=True, help="Output directory to save processed PDF files")
    parser.add_argument("-p", "--printer", required=True, help="Name of the printer to use")

    args = parser.parse_args()

    input_directory = args.input
    output_directory = args.output

    # Check if input directory exists
    if not os.path.exists(input_directory):
        print(f"Error: Input directory '{input_directory}' does not exist.")
        return

    if not os.path.isdir(input_directory):
        print(f"Error: '{input_directory}' is not a directory.")
        return

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: {output_directory}")

    # Process all PDF files in the input directory
    pdf_files = [f for f in os.listdir(input_directory) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print(f"No PDF files found in directory: {input_directory}")
        return

    print(f"Found {len(pdf_files)} PDF file(s) to process.")

    processed_count = 0
    for file_name in pdf_files:
        input_pdf_path = os.path.join(input_directory, file_name)
        output_pdf_path = os.path.join(output_directory, f"processed_{file_name}")

        print(f"\nProcessing: {file_name}")

        # Process the PDF
        if process_pdf(input_pdf_path, output_pdf_path):
            # Print the processed PDF
            print(f"Sending processed PDF to printer: {args.printer}")
            print_pdf(args.printer, output_pdf_path)
            processed_count += 1
        else:
            print(f"Failed to process: {file_name}")

    print(f"\nBatch processing complete. Successfully processed {processed_count} out of {len(pdf_files)} PDF files.")


if __name__ == "__main__":
    main()