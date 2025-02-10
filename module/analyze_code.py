"""
Module to run pylint on all Python files in a directory and save the results to a file.
"""

import os
from pylint import epylint as lint

def run_pylint_on_files(directory, output_file_path):
    """
    Run pylint on all Python files in the specified directory and save the results to a file.

    Args:
        directory (str): The directory containing the Python files to analyze.
        output_file_path (str): The path to the file where the pylint results will be saved.
    """
    with open(output_file_path, "w", encoding="utf-8") as output_file_handle:
        for file in os.listdir(directory):
            if file.endswith(".py"):
                file_path = os.path.join(directory, file)
                print(f"Running pylint on {file_path}...")
                
                # Run pylint
                pylint_stdout, _ = lint.py_run(file_path, return_std=True)
                output = pylint_stdout.getvalue()
                
                # Write output to file with a separator
                output_file_handle.write(f"{'='*40}\n")
                output_file_handle.write(f"Results for: {file_path}\n")
                output_file_handle.write(f"{'='*40}\n\n")
                output_file_handle.write(output + "\n\n")

# Run pylint on all Python files in the current directory
CURRENT_DIRECTORY = os.getcwd()
OUTPUT_FILE = "pylint_results.txt"
run_pylint_on_files(CURRENT_DIRECTORY, OUTPUT_FILE)

print(f"\nPylint results saved to {OUTPUT_FILE}")