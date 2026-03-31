from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY=os.getenv("OPENROUTER_API_KEY")

def generate_content(text):
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

                 STRICT RULES:
                 - DO NOT add any extra text
                 - DO NOT add "Here is My output"
                 - Follow EXACT format below

                FORMAT:

                 TWITTER:
                 <Only twitter threads>

                 LINKEDIN:
                 <Only Linkedin post>

                 SUMMARY:
                 <only summary>

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
            twitter = text.split("TWITTER:")[1].split("LINKEDIN:")[0].strip()
            linkedin = text.split("LINKEDIN:")[1].split("SUMMARY:")[0].strip()
            summary = text.split("SUMMARY:")[1].strip()


            return {
            "twitter": twitter,
            "linkedin":linkedin,
            "summary":summary
            }
        except Exception as e:
            return {
                "error":"Parsing Failed",
                "raw":text
            }
    
    
    reply = data["choices"][0]["message"]["content"]

    parsed = parse_response(reply)

    return parsed


