"""
app.py
------
The main entry point of SmartDoc AI. This file is ONLY responsible for the
user interface (UI) and wiring the pieces together — it does not contain
PDF-parsing logic or prompt logic itself. Those live in src/.

Run with:  streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv

from src.pdf_extractor import (
    extract_text_from_pdf,
    truncate_text,
    EmptyPDFError,
    CorruptPDFError,
    PDFTooLargeError,
)
from src.gemini_client import (
    configure_gemini,
    generate_document_insights,
    GeminiAPIError,
    GeminiResponseParseError,
)
from src.utils import format_summary_as_text, estimate_reading_time


# ----------------------------------------------------------------------
# 1. PAGE CONFIG — must be the first Streamlit command in the script
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="SmartDoc AI — Document Summarizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ----------------------------------------------------------------------
# 2. LOAD API KEY
#    Locally: comes from a .env file (via python-dotenv).
#    On Streamlit Cloud: comes from st.secrets (set in the dashboard).
# ----------------------------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")


# ----------------------------------------------------------------------
# 3. SIDEBAR — branding, instructions, and settings
# ----------------------------------------------------------------------
with st.sidebar:
    st.title("📄 SmartDoc AI")
    st.caption("AI-powered PDF summarizer")

    st.markdown("---")
    st.subheader("How it works")
    st.markdown(
        """
        1. Upload a PDF (report, article, notes, etc.)
        2. Click **Analyze Document**
        3. Get a summary, key points, keywords,
           action items, flashcards & FAQs
        4. Download your results
        """
    )

    st.markdown("---")
    with st.expander("⚙️ Advanced options"):
        show_flashcards = st.checkbox("Generate flashcards", value=True)
        show_faqs = st.checkbox("Generate FAQs", value=True)

    st.markdown("---")
    st.caption("Built with Streamlit + Google Gemini API")
    st.caption("🔗 [View source on GitHub](https://github.com/your-username/smartdoc-ai)")


# ----------------------------------------------------------------------
# 4. MAIN HEADER
# ----------------------------------------------------------------------
st.title("📄 SmartDoc AI — Smart Document Summarizer")
st.markdown(
    "Upload any text-based PDF and instantly get a clean summary, "
    "key points, keywords, and action items — powered by Google Gemini."
)
st.markdown("---")


# ----------------------------------------------------------------------
# 5. CHECK API KEY EARLY — fail loudly and clearly, not with a crash
# ----------------------------------------------------------------------
if not GEMINI_API_KEY:
    st.error(
        "⚠️ No Gemini API key found.\n\n"
        "If running locally: create a `.env` file with `GEMINI_API_KEY=your_key`.\n\n"
        "If deployed: add `GEMINI_API_KEY` under your app's **Secrets** in "
        "Streamlit Community Cloud."
    )
    st.stop()  # halts execution here so the rest of the app doesn't run


# ----------------------------------------------------------------------
# 6. FILE UPLOAD
# ----------------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload a PDF file",
    type=["pdf"],
    help="Maximum file size: 25 MB. Scanned/image-only PDFs are not supported.",
)

analyze_clicked = st.button("🔍 Analyze Document", type="primary", disabled=uploaded_file is None)


# ----------------------------------------------------------------------
# 7. MAIN PROCESSING LOGIC
# ----------------------------------------------------------------------
if analyze_clicked and uploaded_file is not None:

    file_bytes = uploaded_file.read()

    # --- Step A: Extract text from the PDF, with full error handling ---
    with st.spinner("📖 Reading your PDF..."):
        try:
            raw_text, num_pages = extract_text_from_pdf(file_bytes)
        except EmptyPDFError as e:
            st.error(f"❌ {e}")
            st.stop()
        except CorruptPDFError as e:
            st.error(f"❌ {e}")
            st.stop()
        except PDFTooLargeError as e:
            st.error(f"❌ {e}")
            st.stop()
        except Exception as e:
            st.error(f"❌ An unexpected error occurred while reading the PDF: {e}")
            st.stop()

    text_for_model = truncate_text(raw_text)
    reading_time = estimate_reading_time(raw_text)

    st.success(f"✅ Extracted text from {num_pages} page(s) — approx. {reading_time} min read.")

    # --- Step B: Send to Gemini, with full error handling ---
    with st.spinner("🤖 Analyzing with Gemini AI... this may take a few seconds"):
        try:
            configure_gemini(GEMINI_API_KEY)
            insights = generate_document_insights(text_for_model)
        except GeminiAPIError as e:
            st.error(
                f"❌ Could not reach Gemini API: {e}\n\n"
                "This is usually caused by an invalid API key, no internet "
                "connection, or exceeding your free quota."
            )
            st.stop()
        except GeminiResponseParseError as e:
            st.error(f"❌ {e} — please try again.")
            st.stop()
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
            st.stop()

    # Store results in session_state so they persist across reruns
    # (e.g. when the user clicks the download button afterwards).
    st.session_state["insights"] = insights
    st.session_state["filename"] = uploaded_file.name


# ----------------------------------------------------------------------
# 8. DISPLAY RESULTS (only if we have them in session_state)
# ----------------------------------------------------------------------
if "insights" in st.session_state:
    insights = st.session_state["insights"]
    filename = st.session_state["filename"]

    st.markdown("## 📋 Results")

    tab_summary, tab_keypoints, tab_keywords, tab_actions, tab_extra = st.tabs(
        ["📝 Summary", "🔑 Key Points", "🏷️ Keywords", "✅ Action Items", "🎓 Flashcards & FAQs"]
    )

    with tab_summary:
        st.subheader("Summary")
        st.write(insights.get("summary", "No summary available."))

    with tab_keypoints:
        st.subheader("Key Points")
        for point in insights.get("key_points", []):
            st.markdown(f"- {point}")

    with tab_keywords:
        st.subheader("Keywords")
        keywords = insights.get("keywords", [])
        if keywords:
            # Render keywords as little "chips" using columns
            cols = st.columns(4)
            for i, kw in enumerate(keywords):
                with cols[i % 4]:
                    st.markdown(
                        f"<span style='background-color:#e8f0fe;color:#1a73e8;"
                        f"padding:4px 10px;border-radius:12px;font-size:13px;"
                        f"display:inline-block;margin:3px 0;'>{kw}</span>",
                        unsafe_allow_html=True,
                    )

    with tab_actions:
        st.subheader("Action Items")
        action_items = insights.get("action_items", [])
        if action_items:
            for item in action_items:
                st.checkbox(item, key=f"action_{hash(item)}")
        else:
            st.info("No specific action items were found in this document.")

    with tab_extra:
        flashcards = insights.get("flashcards", [])
        faqs = insights.get("faqs", [])

        if flashcards:
            st.subheader("🎓 Flashcards")
            for i, card in enumerate(flashcards, start=1):
                with st.expander(f"Q{i}: {card.get('question', '')}"):
                    st.write(card.get("answer", ""))

        if faqs:
            st.subheader("❓ FAQs")
            for i, faq in enumerate(faqs, start=1):
                with st.expander(f"{faq.get('question', '')}"):
                    st.write(faq.get("answer", ""))

    # --- Download button ---
    st.markdown("---")
    report_text = format_summary_as_text(filename, insights)
    st.download_button(
        label="⬇️ Download Summary as TXT",
        data=report_text,
        file_name=f"summary_{filename.replace('.pdf', '')}.txt",
        mime="text/plain",
    )

else:
    st.info("👆 Upload a PDF and click **Analyze Document** to get started.")