
conda activate PrintAThingPDF
python .\print_labels_and_packing_sheets.py -p1 "Canon G3060 series (Copy 1)" -p2 "BY-480_BTH" -i .\input -o .\output
rm .\input\*f.pdf