"""
utils.py
--------
Small, reusable helper functions that don't belong specifically to
PDF extraction or Gemini logic — things like formatting the final
summary for download.
"""

from datetime import datetime


def format_summary_as_text(filename: str, insights: dict) -> str:
    """
    Converts the structured insights dictionary into a clean, readable
    plain-text report that the user can download (e.g. summary.txt).
    """
    lines = []
    lines.append(f"SmartDoc AI — Document Summary Report")
    lines.append(f"Source file: {filename}")
    lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 60)

    lines.append("\nSUMMARY\n" + "-" * 30)
    lines.append(insights.get("summary", "N/A"))

    lines.append("\nKEY POINTS\n" + "-" * 30)
    for point in insights.get("key_points", []):
        lines.append(f"• {point}")

    lines.append("\nKEYWORDS\n" + "-" * 30)
    lines.append(", ".join(insights.get("keywords", [])))

    action_items = insights.get("action_items", [])
    if action_items:
        lines.append("\nACTION ITEMS\n" + "-" * 30)
        for item in action_items:
            lines.append(f"☐ {item}")

    flashcards = insights.get("flashcards", [])
    if flashcards:
        lines.append("\nFLASHCARDS\n" + "-" * 30)
        for i, card in enumerate(flashcards, start=1):
            lines.append(f"Q{i}: {card.get('question', '')}")
            lines.append(f"A{i}: {card.get('answer', '')}\n")

    faqs = insights.get("faqs", [])
    if faqs:
        lines.append("\nFAQs\n" + "-" * 30)
        for i, faq in enumerate(faqs, start=1):
            lines.append(f"Q{i}: {faq.get('question', '')}")
            lines.append(f"A{i}: {faq.get('answer', '')}\n")

    return "\n".join(lines)


def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Rough estimate of reading time in minutes — a nice little detail
    that makes the UI feel more polished/professional.
    """
    word_count = len(text.split())
    minutes = max(1, round(word_count / words_per_minute))
    return minutes