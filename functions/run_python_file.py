import os
from google.genai import types
from functions.config import MAX_CHARS
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        command = ["python", file_path] + args
        result = subprocess.run(
            args=command,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text= True
            )
        output=[]
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "/n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run especified python file in directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="he file path, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            )
        },
    ),
)
