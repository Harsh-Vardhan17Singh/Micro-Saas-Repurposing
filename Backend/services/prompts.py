def social_prompt(text, tone, instructions):
    return f"""
You are an expert content strategist and copywriter.

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

Tweet 1
- Strong hook
- Make people stop scrolling
- Use curiosity, surprise or a bold opinion

Tweet 2
- Explain the problem

Tweet 3
- Give valuable insight

Tweet 4
- Give an actionable example or tip

Tweet 5
- End with a CTA that encourages discussion

GENERAL RULES

- Exactly 5 tweets
- No repeated ideas
- Natural writing
- No placeholders
- No markdown
- No numbering

LINKEDIN RULES

- Start with a hook
- Short readable paragraphs
- Actionable advice
- Professional tone
- End with a question

SUMMARY RULES

- 5-6 concise lines
- Focus only on important ideas

Return ONLY valid JSON.
"""


def email_prompt(text, tone, instructions):
    return f"""
Return ONLY valid JSON.

{{
  "subject":"email subject",
  "body":"email body"
}}

TONE:
{tone}

CONTENT:
{text}

Write a professional email with

- Strong subject
- Engaging introduction
- Valuable body
- Clear conclusion

Return ONLY valid JSON.
"""


def instagram_prompt(text, tone, instructions):
    return f"""
Return ONLY valid JSON.

{{
  "caption":"instagram caption",
  "hashtags":"#tag1 #tag2 #tag3 #tag4 #tag5"
}}

TONE:
{tone}

CONTENT:
{text}

Caption Rules

- Strong opening
- Short paragraphs
- Natural emojis
- Strong CTA
- Exactly 5 hashtags

Return ONLY valid JSON.
"""