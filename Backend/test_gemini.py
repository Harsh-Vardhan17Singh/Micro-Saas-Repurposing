from dotenv import load_dotenv
import google.generativeai as genai
import os
load_dotenv()
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)
model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content(
    """
Retrun ONLY valid JSON.
{
"twitter":["tweet1,"tweet2","tweet3","tweet4","tweet5"],
"linkedin":"linkedin post",
"summary":"summary"
}
Topic : AI is Transformaing startups.
"""
)
print(response.text)