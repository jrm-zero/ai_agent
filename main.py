import os
import argparse
from dotenv import load_dotenv
from google import genai

def api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("Gemini API key not found")
    client = genai.Client(api_key=api_key)
    return client

def call_to_model(client, prompt):
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt
    )
    if response.usage_metadata == None:
        raise RuntimeError("likely failed API request")
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: \n{response.text}")

def get_user_input():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    return args.user_prompt

def main():
    client = api_key()
    prompt = get_user_input()
    call_to_model(client, prompt)

if __name__ == "__main__":
    main()
