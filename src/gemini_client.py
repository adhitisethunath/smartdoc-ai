"""
gemini_client.py
----------------
Everything related to talking to Google's Gemini API lives here.
If you ever switch to a different LLM (OpenAI, Claude, etc.), this is the
ONLY file you'd need to rewrite — that's the benefit of modular design.
"""

import json
import os
import re
import google.generativeai as genai

from src.prompts import build_summary_prompt


class GeminiAPIError(Exception):
    """Raised when the Gemini API call fails for any reason
    (bad key, network issue, quota exceeded, etc.)."""
    pass


class GeminiResponseParseError(Exception):
    """Raised when Gemini's reply isn't valid JSON we can use."""
    pass


def configure_gemini(api_key: str) -> None:
    """
    Sets up the Gemini SDK with our API key.
    Called once when the app starts.
    """
    if not api_key:
        raise GeminiAPIError(
            "No Gemini API key found. Add GEMINI_API_KEY to your .env file "
            "or Streamlit secrets."
        )
    genai.configure(api_key=api_key)


def _clean_json_response(raw_text: str) -> str:
    """
    LLMs sometimes wrap JSON in ```json ... ``` code fences even when told
    not to. This strips those fences so json.loads() doesn't choke on them.
    """
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    return cleaned


def generate_document_insights(document_text: str, model_name: str = "gemini-2.5-flash") -> dict:
    """
    Sends the document text to Gemini using our prompt template and
    returns a parsed Python dictionary with:
        summary, key_points, keywords, action_items, flashcards, faqs

    Raises GeminiAPIError or GeminiResponseParseError on failure —
    the UI layer (app.py) decides how to display these to the user.
    """
    prompt = build_summary_prompt(document_text)

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,   # lower temperature = more focused, less "creative"/random
                max_output_tokens=4096,
            ),
        )
    except Exception as e:
        # Any network/API/quota error gets wrapped into our own clear exception.
        raise GeminiAPIError(f"Gemini API request failed: {e}")

    if not response or not response.text:
        raise GeminiAPIError("Gemini returned an empty response. Try again.")

    cleaned_text = _clean_json_response(response.text)

    try:
        result = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        raise GeminiResponseParseError(
            f"Could not parse Gemini's response as JSON: {e}"
        )

    # Defensive defaults — guarantees every key exists even if the model
    # forgets one, so app.py never crashes on a missing dictionary key.
    result.setdefault("summary", "")
    result.setdefault("key_points", [])
    result.setdefault("keywords", [])
    result.setdefault("action_items", [])
    result.setdefault("flashcards", [])
    result.setdefault("faqs", [])

    return result