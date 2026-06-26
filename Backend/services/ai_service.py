from dotenv import load_dotenv
from services.prompts import (
    social_prompt,
    email_prompt,
    instagram_prompt
)
import os
import google.generativeai as genai
import json


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_content(text, tone, content_format):
    if content_format == "social":
        prompt = social_prompt(text,tone)
    elif content_format == "email":
        prompt = email_prompt(text,tone)
    elif content_format == "instagram":
        prompt = instagram_prompt(text,tone)
    else:
        return {
            "error":"Unsupported format"
        }

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type":"application/json"
            }
            )

        reply = response.text.strip()
        reply = (
            reply.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        parsed = json.loads(reply)

        # Validation for social format
        if content_format == "social":
            if "twitter" not in parsed:
                return {
                    "error": "Missing twitter array"
                }

            if not isinstance(parsed["twitter"], list):
                return {
                    "error": "Twitter field is not a list"
                }

            if len(parsed["twitter"]) != 5:
                return {
                    "error": "AI did not generate exactly 5 tweets",
                    "raw": parsed
                }

        return parsed

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by model",
            "raw": reply
        }

    except Exception as e:
        return {
            "error": str(e)
        }