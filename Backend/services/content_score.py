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

    # --------------------------
    # Readability
    # --------------------------

    words = text.split()

    avg_sentence = len(words) / max(
        1,
        len(re.split(r"[.!?]", text))
    )

    readability = 100

    if avg_sentence > 25:
        readability -= 20

    if avg_sentence > 35:
        readability -= 20

    score["readability"] = max(readability, 60)

    # --------------------------
    # CTA
    # --------------------------

    cta = 50

    lower = text.lower()

    for word in CTA_WORDS:
        if word in lower:
            cta += 8

    score["cta"] = min(cta, 100)

    # --------------------------
    # Engagement
    # --------------------------

    engagement = 70

    emojis = len(re.findall(r"[😀-🙏]", text))

    engagement += min(emojis * 2, 10)

    if "?" in text:
        engagement += 10

    if "story" in lower:
        engagement += 5

    score["engagement"] = min(engagement, 100)

    # --------------------------
    # Overall
    # --------------------------

    overall = (
        score["hook"]
        + score["readability"]
        + score["cta"]
        + score["engagement"]
    ) // 4

    score["overall"] = overall


