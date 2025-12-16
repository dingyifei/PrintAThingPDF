# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Windows-only PDF processing tools for PrintAThing.com shipping labels. Splits multi-page PDFs, rotates/crops label pages, and prints to different printers via SumatraPDF.

## Setup

```sh
# Uses conda environment
conda activate PrintAThingPDF

# Install dependencies
pip install -r requirements.txt

# Place SumatraPDF.exe portable executable in the repository root
```

**Dependencies**: PyPDF2, pywin32, SumatraPDF (portable exe)

## Commands

List available printers:
```sh
python pdf_printer.py --list-printers
```

Split and print PDFs to two printers (packing sheets + labels):
```sh
python print_labels_and_packing_sheets.py -p1 "<printer1>" -p2 "<printer2>" -i ./input -o ./output
```

Process 6-page PDFs (removes pages 1-2, rotates pages 4-5, sends to single printer):
```sh
python pure_print_labels_and_packing_sheets.py -i ./input -o ./output -p "<printer>"
```

Split a single PDF into two files:
```sh
python pdf_splitter.py -i <input.pdf> -o1 <packing_sheet.pdf> -o2 <label.pdf>
```

## Architecture

- **pdf_splitter.py** - Core PDF splitting: separates pages, rotates last page 270°, crops to 4x6" label size. Exports `split_pdf()` function.
- **pdf_printer.py** - Printer interface using win32print for enumeration, SumatraPDF subprocess for printing. Exports `list_printers()` and `print_pdf()` functions.
- **print_labels_and_packing_sheets.py** - Batch processor: splits PDFs in input dir into `_1.pdf` (packing) and `_2.pdf` (label), sends to two different printers.
- **pure_print_labels_and_packing_sheets.py** - Alternative processor for 6-page PDFs: removes pages 1-2, rotates pages 4-5 by 270°, outputs as `processed_*.pdf`.

All scripts use argparse for CLI. The batch scripts import from `pdf_splitter` and `pdf_printer` modules.

## Key Constants

Label cropping coordinates in `pdf_splitter.py:24-25`:
```python
mediabox.lower_left = (82, 260)
mediabox.upper_right = (514, 548)  # 4x6 inches at 72 DPI (432x288 points)
```