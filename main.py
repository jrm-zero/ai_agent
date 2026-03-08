import os
import argparse
from prompts import system_prompt
from call_function import available_functions
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types # type: ignore

def api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("Gemini API key not found")
    client = genai.Client(api_key=api_key)
    return client

def call_to_model(client, prompt):
    messages = [types.Content(role="user", parts=[types.Part(text=prompt.user_prompt)])]
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0
        )
    )
    if response.usage_metadata == None:
        raise RuntimeError("likely failed API request")
    if prompt.verbose == True:
        print(f"User prompt: {prompt.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
    if response.function_calls != None:
        for item in response.function_calls:
            print(f"Calling function: {item.name}({item.args})")
    else:
        print(f"Response: \n{response.text}")

def get_user_input():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    return args

def main():
    client = api_key()
    prompt = get_user_input()
    call_to_model(client, prompt)

if __name__ == "__main__":
    main()
