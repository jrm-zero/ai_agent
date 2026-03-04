import os
from dotenv import load_dotenv
from google import genai

def api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("Gemini API key not found")
    client = genai.Client(api_key=api_key)
    return client

def call_to_model(client):
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents='Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
    )
    print(response.text)

def main():
    client = api_key()
    call_to_model(client)

if __name__ == "__main__":
    main()
