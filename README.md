# pdfpipe

A configurable PDF processing pipeline for splitting, transforming, and printing PDFs. Originally designed for PrintAThing.com shipping labels, but flexible enough for any PDF batch processing workflow.

## Features

- **YAML Configuration**: Define processing pipelines in simple config files
- **Page Selection**: Select pages by index, range, or pattern (`first`, `last`, `odd`, `even`)
- **Transformations**: Rotate, crop, and resize pages with precise control
- **Multi-Output**: Split one PDF into multiple outputs with different settings
- **Batch Processing**: Process single files or entire directories
- **Printing**: Send outputs to different printers with custom settings
- **Dry Run**: Preview what will happen before processing

## Installation

```sh
# Clone and install in development mode
git clone https://github.com/your-repo/pdfpipe.git
cd pdfpipe
pip install -e .

# Place SumatraPDF.exe in the project directory (required for printing)
```

Download SumatraPDF: [sumatrapdfreader.org](https://www.sumatrapdfreader.org/free-pdf-reader.html)

## Quick Start

```sh
# List available printers
pdfp --list-printers

# Process PDFs with a config file
pdfp -c configs/label_packing.yaml -i ./input -o ./output

# Process a single file
pdfp -c configs/label_packing.yaml -i document.pdf

# Dry run (see what would happen)
pdfp -c configs/label_packing.yaml -i ./input --dry-run

# Validate a config file
pdfp -c configs/label_packing.yaml --validate
```

## Configuration

Create a YAML config file to define your processing pipeline:

```yaml
version: 1

settings:
  on_error: continue  # or "stop"
  cleanup_source: false
  cleanup_output_after_print: false

outputs:
  packing_sheet:
    pages: "1--1"  # all pages except last
    output_dir: ./output
    filename_suffix: "_packing"
    print:
      enabled: true
      printer: "Canon G3060 series"

  label:
    pages: "last"
    transforms:
      - rotate: 270
      - crop:
          lower_left: [82, 260]
          upper_right: [514, 548]
    output_dir: ./output
    filename_suffix: "_label"
    print:
      enabled: true
      printer: "Label Printer"
```

### Page Selection Syntax

| Syntax | Meaning |
|--------|---------|
| `[1, 2, 3]` | Exact pages 1, 2, 3 |
| `"1-3"` | Pages 1 through 3 |
| `"3-"` | Page 3 to end |
| `"-2"` | Last 2 pages |
| `"1--1"` | Page 1 to second-to-last |
| `"first"` | First page only |
| `"last"` | Last page only |
| `"odd"` | All odd-numbered pages |
| `"even"` | All even-numbered pages |
| `"all"` | All pages |

### Transforms

```yaml
transforms:
  # Rotate by degrees
  - rotate: 270  # 0, 90, 180, 270

  # Or rotate to orientation
  - rotate: landscape  # landscape, portrait

  # Crop to coordinates (in points, 72 per inch)
  - crop:
      lower_left: [0, 0]
      upper_right: [288, 432]

  # Resize with units
  - size:
      width: 100mm   # supports: mm, in, pt, cm
      height: 150mm
      fit: contain   # contain, cover, stretch
```

## Example Configs

See the `configs/` directory for ready-to-use examples:

- `label_packing.yaml` - Split PDFs into packing sheet + shipping label
- `six_page.yaml` - Process 6-page PDFs (remove pages 1-2, rotate pages 4-5)

## Requirements

- Python 3.10+
- Windows (for printing functionality)
- SumatraPDF (for printing)

## License

MIT License
