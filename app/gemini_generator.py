import os
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

model = genai.GenerativeModel("gemini-3-flash-preview")


def generate_workout_gemini(user_input):

    prompt = f"""
You are a professional fitness trainer.

Create a personalized 7-day workout plan.

Goal: {user_input['goal']}
Intensity: {user_input['intensity']}

For each day include:

Day 1 to Day 7

Warm-up:
Main Workout:
Sets and Reps:
Cooldown:
Recovery Tip:

Make the plan simple, safe and easy to understand.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error: {e}"
