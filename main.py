import os
import argparse
import sys
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from prompts import system_prompt
from call_function import available_functions, call_function
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

def call_to_model(client, prompt, previous_convo):
    messages = [types.Content(role="user", parts=[types.Part(text=prompt.user_prompt)])]
    messages.append(types.Content(role="user", parts=[types.Part(text=previous_convo)]))
    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0
            )
        )

        if len(response.candidates) > 0:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.usage_metadata == None:
            raise RuntimeError("likely failed API request")
        if prompt.verbose == True:
            print(f"User prompt: {prompt.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.function_calls != None:
            function_responses = []
            for item in response.function_calls:
                function_call_result = call_function(item, prompt.verbose)
                if len(function_call_result.parts) == 0:
                    raise Exception(f"Function {item.name} returned an empty list!")
                if function_call_result.parts[0].function_response == None:
                    raise Exception(f"Function {item.name} parts[0] returned a None result!")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception(f"Function {item.name} returned None as a response!")
                function_responses.append(function_call_result.parts[0])
                if prompt.verbose == True:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(f"Response: \n{response.text}")
            return response.text
        
        messages.append(types.Content(role="user", parts=function_responses))
    
    sys.exit("ai agent did not come to a response")

def get_user_input():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    return args

def main():
    client = api_key()
    prompt = get_user_input()
    previous_convo = get_file_content(".", "prior_convo.txt")
    response = call_to_model(client, prompt, previous_convo)
    previous_convo = previous_convo + f"\n----\nuser input: {prompt.user_prompt}\n----\nresponse: {response}"
    write_file(".", "prior_convo.txt", previous_convo)

if __name__ == "__main__":
    main()
