
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

API_KEY=os.getenv("OPENROUTER_API_KEY")

def generate_content(text,tone,format):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
       "Authorization": f"Bearer {API_KEY}",
       "Content-Type": "application/json"
    }
    data = {
        "max_tokens":500,
        "temperature":0.7,
        "model":"nvidia/nemotron-3-ultra:free",
        "messages":[
            {
                "role":"user",
                "content":f"""
                You are a Strict API.
                Return ONLY valid JSON.

                If format == "social":
                {{
                "twitter":["Tweet 1 wioth hook",
                "Tweet 2 with insight",
                "Tweet 3 with value",
                "Tweet 4 with Example",
                "Tweet 5 with CTA"],
                "linkedin":"A paragraph Linkedin post (120-140 word)",
                "summary":"A clean 5-6 lines summary"
                }}

                RULES FOR TWITTER:
                - MUST generate exactly 5 tweets
                - Each tweet must be different
                - Each tweet should be 1-2 sentences
                - No palceholder
                - No "tweet1" text
                - No repeated content 
                - First tweet should have a strong hook
                - last tweet should call to action 

                ---------------------------

                If format == "email":
                {{
                "subject":"email subject",
                "body":"6-7 lines summary"
                }}

                ---------------------------
                If format == "instagram":
                {{
                "caption":"engaging caption",
                "hashtags":"#tag1 #tag2 #tag3 #tag4 #tag5"
                }}

                RULES:
                -No extra text
                -NO explanation
                -No heading like TWITTER
                -output must be valid JSON only
                -Follow selected format strictly

                -----------------------------
               

                FORMAT: {format}


                CONTENT:
                {text}"""
            }
        ]
    }


    response = requests.post(
       url,
       headers=headers,
       json=data,
       timeout=20
       )
    if response.status_code != 200:
       return{"error":"API request failed","raw":response.text}

    data = response.json()

    # extract reply
    print("AI Response received")

    if "choices" not in data:
        return f"API Error:{data}"
    
     
    reply = data["choices"][0]["message"]["content"]

    #clean markdown json blocks
    reply = reply.replace("```json","").replace("```","").strip()

    try:
       parsed = json.loads(reply)
       return parsed
    except Exception:
       return{
          "error":"Invalid JSON from AI",
          "raw":reply
       }
       
       



  


