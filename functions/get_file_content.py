import os
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and prints a set number of characters from a specified file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path for file to be read, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    if os.path.isdir(working_directory) == False: # type: ignore
        return f'Error: "{working_directory}" is not a directory'
    
    abs_working_directory = os.path.abspath(working_directory) # type: ignore
    target_file = os.path.normpath(os.path.join(abs_working_directory, file_path)) # type: ignore
    if os.path.isfile(target_file) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if os.path.commonpath([target_file, abs_working_directory]) == abs_working_directory: # type: ignore
        MAX_CHARS = 10000
        try:
            with open(target_file, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
        except Exception as e:
            return f"Error: {e}"
    else:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'