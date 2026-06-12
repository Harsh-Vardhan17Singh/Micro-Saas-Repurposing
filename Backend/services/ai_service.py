from dotenv import load_dotenv
import os
import google.generativeai as genai
import json

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_content(text, tone, content_format):
    prompt = f"""
You are a Strict API.

Return ONLY valid JSON.

If format == "social":
{{
  "twitter": [
    "tweet1",
    "tweet2",
    "tweet3",
    "tweet4",
    "tweet5"
  ],
  "linkedin": "linkedin post",
  "summary": "summary"
}}

RULES FOR TWITTER:
- Generate exactly 5 tweets
- All tweets must be different
- First tweet must be a hook
- Last tweet must contain a CTA
- No placeholders
- No repeated content

---------------------------

If format == "email":
{{
  "subject": "email subject",
  "body": "email body"
}}

---------------------------

If format == "instagram":
{{
  "caption": "instagram caption",
  "hashtags": "#tag1 #tag2 #tag3 #tag4 #tag5"
}}

RULES:
- Return valid JSON only
- No markdown
- No explanation
- No headings
- Follow selected format exactly

FORMAT:
{content_format}

TONE:
{tone}

CONTENT:
{text}
"""

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