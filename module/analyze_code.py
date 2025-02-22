"""
This module will help me imporve the style and coding of the module
reminder to self:
- write docstring to each file and each function
- in docstring explain how, in # explain only why
"""
import os
from pylint import epylint as lint
import subprocess

def run_linters_on_files(directory, output_file_path):
    """
    Run Pylint and Flake8 on all Python files in the specified directory and save the results to a file.

    Args:
        directory (str): The directory containing the Python files to analyze.
        output_file_path (str): The path to the file where the linting results will be saved.
    """
    with open(output_file_path, "w", encoding="utf-8") as output_file_handle:
        for file in os.listdir(directory):
            if file.endswith(".py"):
                file_path = os.path.join(directory, file)
                print(f"Running linters on {file_path}...")
                
                # Run Pylint
                pylint_stdout, _ = lint.py_run(file_path, return_std=True)
                pylint_output = pylint_stdout.getvalue()
                
                # Run Flake8
                try:
                    flake8_output = subprocess.run(["flake8", file_path], capture_output=True, text=True, check=True)
                    flake8_results = flake8_output.stdout
                except subprocess.CalledProcessError as e:
                    flake8_results = e.output
                
                # Write output to file with a separator
                output_file_handle.write(f"{'='*40}\n")
                output_file_handle.write(f"Results for: {file_path}\n")
                output_file_handle.write(f"{'='*40}\n\n")
                
                output_file_handle.write("Pylint Results:\n")
                output_file_handle.write(f"{'-'*20}\n")
                output_file_handle.write(pylint_output + "\n\n")
                
                output_file_handle.write("Flake8 Results:\n")
                output_file_handle.write(f"{'-'*20}\n")
                output_file_handle.write(flake8_results + "\n\n")

# Run linters on all Python files in the current directory
CURRENT_DIRECTORY = os.getcwd()
OUTPUT_FILE = "lint_results.txt"
run_linters_on_files(CURRENT_DIRECTORY, OUTPUT_FILE)

print(f"\nLinting results saved to {OUTPUT_FILE}")
