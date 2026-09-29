from app.gemini_generator import model


def update_workout_plan(original_plan, user_feedback):

    prompt = f"""
You are a professional fitness trainer.

Original workout plan:

{original_plan}

User feedback:

{user_feedback}

Update the workout plan according to the feedback.

Keep the 7-day structure.
Make the changes clear and practical.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"Error updating plan: {e}"
