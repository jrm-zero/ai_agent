import os

def write_file(working_directory, file_path, content):
    if os.path.isdir(working_directory) == False: # type: ignore
        return f'Error: "{working_directory}" is not a directory'
    
    abs_working_directory = os.path.abspath(working_directory) # type: ignore
    target_file = os.path.normpath(os.path.join(abs_working_directory, file_path)) # type: ignore

    if os.path.isdir(target_file) == True:
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    

    if os.path.commonpath([target_file, abs_working_directory]) == abs_working_directory: # type: ignore
        try:
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            with open(target_file, "w") as f:
                f.write(content)
            return f'Succesfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Error: {e}"
    else:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'