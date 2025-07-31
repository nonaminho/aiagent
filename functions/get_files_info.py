import os
from google.genai import types
from functions.config import MAX_CHARS


def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
 
    try:
        files_info = []
        dir = os.listdir(target_dir)
        for file in dir:
            filepath = os.path.join(target_dir, file)
            size = 0
            size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)
            files_info.append(f"- {file}: file_size={size}, is_dir={is_dir}")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

