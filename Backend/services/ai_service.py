
from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY=os.getenv("OPENROUTER_API_KEY")

def generate_content(text,tone,format):
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
                "content":f"""
                You are an AI content repurposer.
                FORMAT:{format}
                TONE:{tone}

                RULES:
                -Do not add extra text
                -Do not use markdown(**)
                -follow EXACT structure
                -Clean output only

                -----------------------------

                If format = "social":
                
                Return EXACTLY:

                TWITTER:
                (tweet 1)
                (tweet 2)
                (tweet 3)
                (tweet 4)
                (tweet 5)

                LINKEDIN:
                (single Paragraph)

                SUMMARY:
                (5-6 lines)

                ----------------------------

                If Format = "email":

                Return EXACTLY:
                
                EMAIL:
                Subject:<subject line>

                Body:<email content>
                
                ----------------------------

                If format = "instagram":
                Return EXACTLY :

                CAPTION:
                <engaging Caption>

                HASHTAGS:
                #tag1  #tag2  #tag3  #tag4  #tag5

                -----------------------------
                CONTENT:
                {text}"""
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

#  ADDING FORMAT FOR EMAIL AND  INSTAGRAM TAGS

    if format == "email":
       return{"email":reply}
    
    if format == "instagram":
       #spliting caption + hashtags
       parts = reply.split("HASHTAGS:")
       caption = parts[0].replace("CAPTION:","").strip()
       hashtags = parts[1].split()  if len(parts) > 1 else ""

       return{
          "caption":caption,
          "hashtags":hashtags
       }
      

    parsed = parse_response(reply)

    return parsed


  


