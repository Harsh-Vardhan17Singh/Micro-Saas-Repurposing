def social_prompt(text, tone):
    return f"""
You are an Expert social strategist.

Return ONLY valid JSON.

{{
"twitter":[
"tweet1",
"tweet2",
"tweet3",
"tweet4",
"tweet5"
],
"linkedin":"linkedin post",
"summary":"summary"
}}

TONE:
{tone}

CONTENT:
{text}

TWITTER RULES
-Generate exactly 5 tweets
-Every tweet must be unique.
-Tweet 1 must be immediately grab attention,
-Tweet 2 should build curiosity,
-Tweet 3 should teach something useful.
-Tweet 4 should include an example or practical insight.
-Tweet 5 should end with a CTA.
-keep tweets concise.
-Aviod generic AI buzzwords.
-sound like real creator, not an AI.

LINKEDIN RULES

-Start with a strong hook.
-Write in short paragraphs
-Provide actionable insights.
-End with a question to encourage comments.

SUMMARY RULES
- 5-6 conside lines.
-Focus only on key ideas.

Return JSON only.
"""

def email_prompt(text , tone):
    return f"""
Return ONLY valid JSON.

{{
"subject":email subject",
"body":"email body"
}}

Tone:
{tone}

Content:
{text}

Write a professional email with:
-strong subject
-engaging introduction
-valuable body
-clear ending

Return JSON only.
"""

def instagram_prompt(text, tone):
    return f"""
Return ONLY valid JSON.
{{
"caption":"caption",
"hastags":"#tags1 #tag2 #tag3 #tag4 #tag5
}}

Tone:
{tone}

Content:
{text}

Caption Rules

-Engaging first Line
-short paragraphs
-Use emojis Naturally
-Strong CTA
-Exactly 5 relevant hashtgas

Return JSON only;
"""