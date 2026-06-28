"""
prompts.py
----------
All prompt-engineering lives here, separate from the API-calling logic.

Why separate prompts into their own file?
In real AI products, prompts are treated like important "config" — they
get tuned, versioned, and tested. Keeping them in one place makes it easy
to improve them later without touching your API or UI code.
"""

# We ask Gemini to return STRICT JSON. This is a key prompt-engineering
# technique: instead of parsing freeform paragraphs (unreliable), we force
# a predictable structure we can parse straight into Python dictionaries.
SUMMARY_PROMPT_TEMPLATE = """You are an expert document analyst. Read the document text below
and analyze it carefully. Then respond with ONLY a valid JSON object — no markdown
formatting, no ```json fences, no extra commentary before or after.

The JSON object must have EXACTLY this structure:

{{
  "summary": "A concise 4-6 sentence summary capturing the document's core meaning.",
  "key_points": ["point 1", "point 2", "point 3", "... 5 to 8 total"],
  "keywords": ["keyword1", "keyword2", "... 6 to 10 total"],
  "action_items": ["action 1", "action 2", "... only if the document implies tasks, decisions, or next steps; otherwise an empty list"],
  "flashcards": [
    {{"question": "A question testing understanding of a key concept", "answer": "The answer"}}
  ],
  "faqs": [
    {{"question": "A question a reader might naturally ask about this document", "answer": "The answer"}}
  ]
}}

Rules:
- Base everything STRICTLY on the document content. Do not invent facts.
- If the document has no actionable tasks, return an empty list for "action_items".
- Generate exactly 4 flashcards and 4 FAQs.
- Keep language simple and clear, suitable for someone skimming quickly.
- Output raw JSON only. Nothing else.

DOCUMENT TEXT:
\"\"\"
{document_text}
\"\"\"
"""


def build_summary_prompt(document_text: str) -> str:
    """
    Inserts the extracted PDF text into our prompt template.
    Using .format() keeps the template readable and reusable.
    """
    return SUMMARY_PROMPT_TEMPLATE.format(document_text=document_text)