import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.caller import available_functions, call_function

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run main.py PROMPT")
        sys.exit(1)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key = api_key)
    model_name = 'gemini-2.0-flash-001'
    user_prompt = sys.argv[1]

    verbose = "--verbose" in sys.argv


    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optinal arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    messages = [
        types.Content(role = "user", parts=[types.Part(text=user_prompt)]),
    ]
    
    response = client.models.generate_content(
        model= model_name,
        contents=messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt,
        )
    )
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print()
    if not response.function_calls:
        print(f"Response:\n{response.text}")
    
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")


if __name__ == "__main__":
    main()
