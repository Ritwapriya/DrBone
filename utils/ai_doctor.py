import google.generativeai as genai
import re
from config.settings import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

def clean_text(text):
    return re.sub(r"\*+", "", text.strip())

def generate_zone_report(entry):
    """Generate doctor-style AI interpretation using Gemini."""
    prompt = f"""
    You are an orthopedic AI doctor. Write a structured, short, and professional report
    for this fracture zone using emojis and concise text.

    Zone: {entry['Zone']}
    Uncertainty: {entry['Uncertainty (%)']}%
    Shift (px): {entry['Shift (px)']}
    Shift (mm): {entry['Shift (mm)']}
    Shape Difference: {entry['Shape Diff']}

    Format strictly as:
    🦴 Fracture Zone 1

    Severity: (1 line)
    Findings: (1 line)
    Advice: (1 line)
    Nutrition Tip: (1 line)
    General Tip: (1 line)

    Tone: Professional but friendly, with relevant emojis.
    """
    response = gemini_model.generate_content(prompt)
    return clean_text(response.text.strip())
