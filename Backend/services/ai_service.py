
from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY=os.getenv("OPENROUTER_API_KEY")

def generate_content(text,tone):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
       "Authorization": f"Bearer {API_KEY}",
       "Content-Type": "application/json"
    }
    data = {
        "model":"meta-llama/llama-3-8b-instruct",
        "messages":[
            {
                "role":"user",
                "content": f"""Convert this podcast transcript into:
                 1. Twitter thread (5 tweets)
                 2. LinkedIn post
                 3. Short Summary

                 Tone:{tone}

                 STRICT RULES:
                 -Adapt writing style based on tone:
                   - professional → formal, clean
                   - casual → friendly, conversational
                   - viral → catchy, engaging, hook-based
                 - DO NOT add any extra text
                 - DO NOT add "Here is My output"
                 - Follow EXACT format below

                FORMAT:

                 TWITTER:
                 (tweet 1)
                 (tweet 2)
                 (tweet 3)
                 (tweet 4)
                 (tweet 5)

                 LINKEDIN:
                 (single paragraph)

                 SUMMARY:
                 (5-6 lines)

                 IMPORTANT:
                    - DO NOT use ** or markdown
                    - DO NOT write "TWITTER THREAD"
                    - DO NOT change headings
                    - headings must be EXACTLY: TWITTER:, LINKEDIN:, SUMMARY:

                 Transcript : 
                 {text}
                """
            }
        ]
    }

    response = requests.post(url,headers=headers,json=data)

    data = response.json()

    # extract reply
    print(data)

    if "choices" not in data:
        return f"API Error:{data}"
    
    def parse_response(text):
     try:
        clean = text.replace("**", "").strip()

        # Split by headings instead of regex
        parts = clean.split("LINKEDIN:")
        
        if len(parts) < 2:
            return {"error": "Format mismatch", "raw": text}

        twitter_part = parts[0].replace("TWITTER:", "").strip()

        remaining = parts[1].split("SUMMARY:")
        
        if len(remaining) < 2:
            return {"error": "Format mismatch", "raw": text}

        linkedin_part = remaining[0].strip()
        summary_part = remaining[1].strip()

        return {
            "twitter": twitter_part,
            "linkedin": linkedin_part,
            "summary": summary_part
        }

     except Exception:
        return {
            "error": "Parsing Failed",
            "raw": text
        }
     
    reply = data["choices"][0]["message"]["content"]

    parsed = parse_response(reply)

    return parsed


  


