import re 

CTA_WORDS = [
    "comment",
    "share",
    "follow",
    "reply",
    "save",
    "subscribe",
    "try",
    "learn more",
    "join"
]

def calculate_content_score(result):

    score = {
        "overall": 0,
        "hook": 0,
        "readability": 0,
        "engagement": 0,
        "cta": 0,
        "feedback": []
    }

    text = ""

    if "twitter" in result:
        text += " ".join(result["twitter"]) + " "

    if "linkedin" in result:
        text += result["linkedin"] + " "

    if "summary" in result:
        text += result["summary"]

    text = text.strip()

    # --------------------------
    # Hook Score
    # --------------------------

    hook = 60

    if text.startswith(("Why", "How", "What", "Imagine")):
        hook += 20

    if "?" in text[:120]:
        hook += 10

    if "!" in text[:120]:
        hook += 10

    score["hook"] = min(hook, 100)
