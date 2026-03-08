import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
    
        if file_path.endswith('.py') == False:
            return f'Error: "{file_path}" is not a Python file'
        
        abs_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))
        if os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if os.path.commonpath([target_file, abs_working_directory]) == abs_working_directory:
            command = ["python", target_file]
            if args != None:
                command.extend(args)
            comp_process_data = subprocess.run(command, timeout=30, text=True, capture_output=True)

            output_string = ""
            if comp_process_data.returncode != 0:
                output_string += f'Process exited with code {comp_process_data.returncode}'

            if len(comp_process_data.stdout) == 0 and len(comp_process_data.stderr) == 0:
                output_string += "\nNo output produced"
            else:
                output_string += f'STDOUT: {comp_process_data.stdout}\nSTDERR: {comp_process_data.stderr}\n'
            
            return output_string 
        else:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: executing Python file: {e}'