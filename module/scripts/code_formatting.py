"""
This module runs Pylint and Flake8 on all Python files in the specified directory
and saves the results to a file.
"""

import io
import os
import subprocess
import sys
from pylint import lint


def run_linters_on_files(directory, output_file_path):
    """
    Run Pylint and Flake8 on all Python files in the specified directory and save the results to a file.

    Args:
        directory (str): The directory containing the Python files to analyze.
        output_file_path (str): The path to the file where the linting results will be saved.

    Returns:
        None: This function writes the results directly to the specified output file.

    Raises:
        Exception: If an error occurs while running the linters or writing to the file.
    """
    try:
        with open(output_file_path, "w", encoding="utf-8-sig") as output_file_handle:
            for file in os.listdir(directory):
                if file.endswith(".py"):
                    file_path = os.path.join(directory, file)
                    print(f"Running linters on {file_path}...")

                    # Redirect stdout to avoid terminal output for Pylint
                    original_stdout = sys.stdout
                    sys.stdout = io.StringIO()  # Capture output in a string buffer

                    # Run Pylint and capture its output
                    try:
                        lint.Run([file_path], do_exit=False)
                        pylint_output_str = sys.stdout.getvalue()
                        if not pylint_output_str.strip():
                            pylint_output_str = "No issues found by Pylint."
                    except Exception as error:
                        pylint_output_str = f"Error running Pylint on {file_path}: {error}"

                    # Restore original stdout
                    sys.stdout = original_stdout

                    # Run Flake8
                    try:
                        flake8_output = subprocess.run(
                            ["flake8", file_path], capture_output=True, text=True, check=True
                        )
                        flake8_results = flake8_output.stdout
                        if not flake8_results.strip():
                            flake8_results = "No issues found by Flake8."
                    except subprocess.CalledProcessError as error:
                        flake8_results = error.output

                    output_file_handle.write(f"\n{'=' * 80}\n")
                    output_file_handle.write(f"FILE: {file_path}\n")
                    output_file_handle.write(f"{'=' * 80}\n\n")

                    output_file_handle.write("PYLINT RESULTS:\n")
                    output_file_handle.write(f"{'-' * 40}\n")
                    output_file_handle.write(pylint_output_str.strip() + "\n\n")

                    output_file_handle.write("FLAKE8 RESULTS:\n")
                    output_file_handle.write(f"{'-' * 40}\n")
                    output_file_handle.write(flake8_results.strip() + "\n\n")

                    output_file_handle.write(f"{'*' * 80}\n\n")
    except Exception as error:
        print(f"An error occurred: {error}")


SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PARENT_DIRECTORY = os.path.dirname(SCRIPT_DIRECTORY)


OUTPUT_FILE = os.path.join(SCRIPT_DIRECTORY, "lint_results.txt")
run_linters_on_files(PARENT_DIRECTORY, OUTPUT_FILE)

print(f"\nLinting results saved to {OUTPUT_FILE}")