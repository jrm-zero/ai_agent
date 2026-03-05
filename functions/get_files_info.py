import os

def get_files_info(working_directory, directory="."):
    if os.path.isdir(working_directory) == False: # type: ignore
        return f'Error: "{working_directory}" is not a directory'
    
    abs_working_directory = os.path.abspath(working_directory) # type: ignore
    target_directory = os.path.normpath(os.path.join(abs_working_directory, directory)) # type: ignore
    if os.path.commonpath([target_directory, abs_working_directory]) == abs_working_directory: # type: ignore
        contents = os.listdir(target_directory) # type: ignore
        content_description = []
        for item in contents:
            item_path = os.path.join(target_directory, item)
            try:
                content_description.append(
                    f"- {item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}" # type: ignore
                )
            except Exception as e:
                return f"Error: {e}"
        return "\n".join(content_description)
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'