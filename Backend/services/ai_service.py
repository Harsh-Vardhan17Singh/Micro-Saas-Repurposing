import requests

API_KEY = "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"

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

                 Return output in this format:

                 TWITTER:
                 <content>

                 LINKEDIN:
                 <content>

                 SUMMARY:
                 <content>

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
    
    reply = data["choices"][0]["message"]["content"]

    def parse_response(text):
        twitter_part = reply.split("LINKEDIN:")[0]
        linkedin_part = reply.split("LINKEDIN:")[1].split("SUMMARY:")[0]
        summary_part = reply.split("SUMMARY:")[1]

        return {
            "Twitter": twitter_part,
            "Linkedin":linkedin_part,
            "Summary":summary_part
        }

    return reply


