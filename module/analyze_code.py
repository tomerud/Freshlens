import os
from pylint import epylint as lint

def run_pylint_on_files(directory):
    for file in os.listdir(directory):
        if file.endswith('.py'): 
            file_path = os.path.join(directory, file)
            print(f"Running pylint on {file_path}")
            pylint_stdout, pylint_stderr = lint.py_run(file_path, return_std=True)
            print(pylint_stdout.getvalue()) 

# Get the current working directory
current_directory = os.getcwd()
run_pylint_on_files(current_directory)
