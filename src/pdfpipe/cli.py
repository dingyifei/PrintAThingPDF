"""Command-line interface for pdfpipe."""

import argparse
import sys
from pathlib import Path

from pdfpipe import __version__


def list_printers() -> list[str]:
    """List available printers on the system."""
    try:
        import win32print
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        )
        return [printer[2] for printer in printers]
    except ImportError:
        print("Error: win32print not available. Printer listing only works on Windows.", file=sys.stderr)
        return []


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="pdfp",
        description="Configurable PDF processing pipeline for splitting, transforming, and printing PDFs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdfp -c config.yaml -i ./input -o ./output    Process PDFs with config
  pdfp -c config.yaml -i document.pdf           Process a single file
  pdfp -c config.yaml --validate                Validate config only
  pdfp -c config.yaml -i ./input --dry-run      Show what would happen
  pdfp --list-printers                          List available printers
""",
    )

    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "-c", "--config",
        type=Path,
        help="Path to YAML configuration file",
    )

    parser.add_argument(
        "-i", "--input",
        type=Path,
        help="Input PDF file or directory containing PDFs",
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output directory (overrides config)",
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate configuration file and exit",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually doing it",
    )

    parser.add_argument(
        "--list-printers",
        action="store_true",
        help="List available printers and exit",
    )

    return parser


def main(args: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed = parser.parse_args(args)

    # Handle --list-printers
    if parsed.list_printers:
        printers = list_printers()
        if not printers:
            print("No printers found.")
            return 1
        print("Available printers:")
        for i, printer in enumerate(printers, 1):
            print(f"  {i}. {printer}")
        return 0

    # Require config for other operations
    if not parsed.config:
        parser.print_help()
        return 1

    # Handle --validate
    if parsed.validate:
        from pdfpipe.config import load_config, ConfigError
        try:
            config = load_config(parsed.config)
            print(f"Configuration is valid: {parsed.config}")
            print(f"  Outputs defined: {', '.join(config.outputs.keys())}")
            return 0
        except ConfigError as e:
            print(f"Configuration error: {e}", file=sys.stderr)
            return 1
        except FileNotFoundError:
            print(f"Configuration file not found: {parsed.config}", file=sys.stderr)
            return 1

    # Handle processing
    if not parsed.input:
        print("Error: --input is required for processing", file=sys.stderr)
        return 1

    from pdfpipe.config import load_config, ConfigError
    from pdfpipe.processor import process

    try:
        config = load_config(parsed.config)

        # Override output directory if specified
        output_dir = parsed.output

        process(
            config=config,
            input_path=parsed.input,
            output_dir=output_dir,
            dry_run=parsed.dry_run,
        )
        return 0
    except ConfigError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"File not found: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())