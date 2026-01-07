from google import genai
from dotenv import load_dotenv
from google.genai import types
from models import GeminiOutput, GeminiInput

load_dotenv()
SYSTEM_INSTRUCTION = "You are part of a script that is responsible for generating better youtube title, description, tags from title and description already provided to you. The youtube channel name is UNSULLIED FOODS GUJARATI"

def ai_video_response(input_data: GeminiInput)-> GeminiOutput:
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
        system_instruction="You are a cat. Your name is Neko.",
        temperature= 1.2,
        response_mime_type="application/json",
        response_json_schema= GeminiOutput.model_json_schema()
        ),
        contents=f"{input_data}",
    )
    output = GeminiOutput.model_validate_json(response.text)

    return output


if __name__ == "__main__":
    # print(ai_video_response(input_data=GeminiInput(**{"title": "pizza recipe", "description": "neopolitan pizza", "videoid": "xyz123"})).__dict__)
    foo =GeminiInput(**{"title": "pizza recipe", "description": "neopolitan pizza", "videoid": "xyz123"})
    print(foo.title) #pizza