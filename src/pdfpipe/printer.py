"""Printer interface for pdfpipe using SumatraPDF."""

import os
import subprocess
import sys
from pathlib import Path


class PrinterError(Exception):
    """Raised when printing fails."""


def list_printers() -> list[str]:
    """
    List available printers on the system.

    Returns:
        List of printer names

    Raises:
        PrinterError: If printer enumeration fails
    """
    try:
        import win32print
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        )
        return [printer[2] for printer in printers]
    except ImportError:
        raise PrinterError("win32print not available. Printing only works on Windows.")


def find_sumatra_pdf() -> Path | None:
    """
    Find SumatraPDF executable.

    Searches in:
    1. Current directory
    2. Script directory
    3. PATH

    Returns:
        Path to SumatraPDF.exe or None if not found
    """
    # Check current directory
    cwd_path = Path.cwd() / "SumatraPDF.exe"
    if cwd_path.exists():
        return cwd_path

    # Check script directory (for installed package)
    script_dir = Path(__file__).parent.parent.parent
    script_path = script_dir / "SumatraPDF.exe"
    if script_path.exists():
        return script_path

    # Check PATH
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    for dir_path in path_dirs:
        exe_path = Path(dir_path) / "SumatraPDF.exe"
        if exe_path.exists():
            return exe_path

    return None


def print_pdf(
    pdf_path: Path,
    printer: str,
    copies: int = 1,
    extra_args: list[str] | None = None,
    sumatra_path: Path | None = None,
    dry_run: bool = False,
) -> bool:
    """
    Print a PDF file using SumatraPDF.

    Args:
        pdf_path: Path to the PDF file
        printer: Name of the printer to use
        copies: Number of copies to print
        extra_args: Additional SumatraPDF command-line arguments
        sumatra_path: Path to SumatraPDF.exe (auto-detected if None)
        dry_run: If True, only show what would be done

    Returns:
        True if printing succeeded, False otherwise

    Raises:
        PrinterError: If SumatraPDF is not found or printing fails
    """
    if not pdf_path.exists():
        raise PrinterError(f"PDF file not found: {pdf_path}")

    if sumatra_path is None:
        sumatra_path = find_sumatra_pdf()

    if sumatra_path is None:
        raise PrinterError(
            "SumatraPDF.exe not found. Please place it in the current directory "
            "or add it to PATH."
        )

    # Build command
    cmd = [str(sumatra_path)]

    # Add print settings
    if copies > 1:
        cmd.extend(["-print-settings", f"{copies}x"])

    # Add extra args
    if extra_args:
        cmd.extend(extra_args)

    # Add printer and file
    cmd.extend(["-print-to", printer, str(pdf_path)])

    if dry_run:
        print(f"[dry-run] Would execute: {' '.join(cmd)}")
        return True

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Print failed: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        raise PrinterError(f"SumatraPDF not found at: {sumatra_path}")
