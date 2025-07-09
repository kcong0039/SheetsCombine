import os
import pandas as pd
from pathlib import Path

def read_csv_with_fallback(filepath):
    """Try reading a CSV with multiple encodings."""
    encodings_to_try = ['utf-8', 'gbk', 'iso-8859-1']
    for enc in encodings_to_try:
        try:
            return pd.read_csv(filepath, encoding=enc)
        except Exception:
            continue
    raise ValueError(f"Could not read file with any known encoding: {filepath}")

def combine_csvs_to_excel(input_folders, output_file_path):
    """Combine all CSVs from multiple folders into one Excel file with separate tabs."""
    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        for folder in input_folders:
            if not os.path.isdir(folder):
                print(f"⚠️ Skipped invalid folder: {folder}")
                continue

            folder_name = os.path.basename(os.path.normpath(folder))
            for filename in os.listdir(folder):
                if filename.lower().endswith('.csv'):
                    filepath = os.path.join(folder, filename)
                    sheet_base = f"{folder_name}_{os.path.splitext(filename)[0]}"
                    sheet_name = sheet_base[:31]  # Excel sheet names max out at 31 characters

                    try:
                        df = read_csv_with_fallback(filepath)
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        print(f"✅ Added {filepath} to sheet '{sheet_name}'")
                    except Exception as e:
                        print(f"❌ Failed to read {filepath}: {e}")

    print(f"\n🎉 All readable CSVs combined into: {output_file_path}")

def main():
    folder_input = input("Enter folder paths (comma-separated): ").strip()
    input_folders = [folder.strip() for folder in folder_input.split(',') if folder.strip()]

    if not input_folders:
        print("❌ No valid folders provided.")
        return

    downloads_folder = str(Path.home() / "Downloads")
    output_file_path = os.path.join(downloads_folder, input("What would you like your output file to be called?: ex: combined.xlsx: "))

    combine_csvs_to_excel(input_folders, output_file_path)