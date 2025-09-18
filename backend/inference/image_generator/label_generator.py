#!/usr/bin/env python3
"""
Simple Folder to Excel - Just filenames in 'name' column
"""

import os
import pandas as pd

def folder_to_excel(folder_path: str, output_file: str = "filenames.xlsx") -> str:
    """
    Read all filenames from a folder and save to Excel with 'name' column

    Args:
        folder_path: Path to folder to scan
        output_file: Output Excel filename

    Returns:
        Path to created Excel file
    """
    filenames = []

    for item in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, item)):
            filenames.append(item)

    df = pd.DataFrame({'name': sorted(filenames)})
    df.to_excel(output_file, index=False)

    return output_file

def main():
    # Example usage
    folder_to_excel("./dataset/", "filenames.xlsx")

if __name__ == "__main__":
    main()
