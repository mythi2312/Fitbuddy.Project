import os
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

model = genai.GenerativeModel(
    os.getenv(
        "GEMINI_FLASH_MODEL",
        "gemini-2.5-flash"
    )
)


def generate_nutrition_tip_with_flash(goal):

    prompt = f"""
Give one simple nutrition or recovery tip
for a person whose fitness goal is:

{goal}

Make it practical, friendly and easy to understand.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"Error: {e}"
