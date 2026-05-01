
from dotenv import load_dotenv
import os
import requests
import re

load_dotenv()

API_KEY=os.getenv("OPENROUTER_API_KEY")

def generate_content(text,tone,format):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
       "Authorization": f"Bearer {API_KEY}",
       "Content-Type": "application/json"
    }
    data = {
        "max_token":500,
        "temperature":0.7,
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
                -do not include words like FORMAT, TONE , CONTENT
                -Do not includes numbers like(1),(2)
                -Each Tweet Must be a Clean sentence 
                -Do not add extra text
                -Do not use markdown(**)
                -follow EXACT structure
                -NO additional section
                -Clean output only
                

                -----------------------------

                If format = "social":
                
                Return EXACTLY:

                TWITTER:
                Line 1:<Tweet 1>
                Line 2:<Tweet 2>
                Line 3:<tweet 3>
                Line 4:<Tweet 4>
                Line 5:<Tweet 5>

                LINKEDIN:
                (single Paragraph)

                SUMMARY:
                (5-6 lines)

                IMPORTANT - 
                1.ONLY THESE 3 SECTION
                2.DO NOT INCLUDE EMAIL AND INSTAGRAM
                3.DO NOT INCLUDE WORDS LIKE HOOK,FORMAT,INCLUDE,CONTENT
                4.EACH TWEET MUST BE OF ONE LINE
                5.EXACTLY 5 TWEETS

                ----------------------------

                If Format = "email":

                Return EXACTLY:
                
                EMAIL:
                SUBJECT:<subject line>

                BODY:<email content>
                (BODY SHOULD BE 6-7 LINES)
                
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
    
    def parse_response(text):
        try:
          clean = text.replace("**", "").replace("\r","").strip()

        # Split main section 
          parts = clean.split("LINKEDIN:")
        
          if len(parts) < 2:
             return {
                "error":"Format Mismatch",
                "raw":text
             }
   # ----------------TWITTER----------------------
          twitter_raw = parts[0].replace("TWITTER:","").strip()

          lines = twitter_raw.split("\n")

          clean_lines = []
          for line in lines:
             l = line.strip()

             if not l:
                continue
             
            #  remove garbage lines
             if any(x in l.lower() for x in [
                "format","tone","content","email","instagram","best hook"
             ]):
                continue
             l = re.sub(r"^(line\s*\d+[:\-]|\d+[\.\)]\s*)", "", l, flags=re.IGNORECASE)

             clean_lines.append(l)
          twitter_part = clean_lines[:5] 

             
#  -----------------LINKEDIN + SUMMARY ------------
          remaining = parts[1].split("SUMMARY:")
        
          if len(remaining) < 2:
             return {
                "error": "Format mismatch", 
                "raw": text}

          linkedin_part = remaining[0].strip()
          summary_part = remaining[1].strip()

         #  CLEAN SUMMARY (IMPORTANT)
          summary_part = summary_part.split("EMAIL:")[0]
          summary_part = summary_part.split("INSTAGRAM:")[0]
          summary_part = summary_part.strip()

          if len(twitter_part) < 3:
             return{
                "error":"low quality output",
                "raw":text

             }

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
    if "TWITTER:" not in reply and format == "social":
       return {
          "error":"AI format mismatch",
          "raw":reply
       }

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
          hashtags = clean.split("HASHTAGS:")[1].strip()
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


  


