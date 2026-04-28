
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
                You are a strict API.You only returns structured output.
                FORMAT:{format}
                TONE:{tone}

                IMPORTANT RULES:
                -output Must Follow format EXACTLY 
                -Do not add extra text
                -Do not use markdown(**)
                -follow EXACT structure
                -NO additional section
                -Clean output only
                -if Wrong Format -> Response is   Invalid

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
                If mode == improve:
                Rewrite content to be:
                - more engaging 
                - stronger hook
                - shorter sentences
                - more viral


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

          twitter_raw = parts[0].replace("TWITTER:","").strip()

          twitter_part = [t.strip() for t in twitter_raw.split("\n")
                          if t.strip() and not t.lower().startwith("tweet")
                          ]

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
       try:
        clean = reply.replace("**","").strip()
        subject = clean.split("SUBJECT:")[1].split("BODY:")[0].strip()
        body = clean.split("BODY:")[1].strip()
        return{
           "subject":subject,
           "body":body
        }
       except:
          return {
             "error":"Email parsing Failed",
             "raw":reply
          }
    
    if format == "instagram":
       #spliting caption + hashtags
      try:
          clean = reply.replace("**","").strip()

          caption = clean.split("CAPTION:")[1].split("HASHTAGS:")[0].strip()
          hashtags  = clean.split("HASHTAGS:")[1].strip()

          return{
          "CAPTION":caption,
          "HASHTAGS":hashtags
       }
      except:
         return {
            "error":"Instagram parsing Failed",
            "raw":reply
         }

      

    parsed = parse_response(reply)

    return parsed


  


