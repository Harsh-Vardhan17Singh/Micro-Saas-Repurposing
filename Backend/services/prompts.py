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
Tweet 1:
- Stop the user from scrolling.
- Start with a surprising fact, bold statement, question, or contrarian opinion.
- Avoid starting with "AI is..." unless it's necessary.

Tweet 2:
- Explain the problem.

Tweet 3:
- Provide a useful insight.

Tweet 4:
- Give a real-world example or actionable tip.

Tweet 5:
- End with a clear CTA that invites replies or discussion.

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