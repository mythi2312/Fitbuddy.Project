# FitBuddy – AI Fitness Plan Generator

## About the Project

FitBuddy is an AI-powered fitness web application developed as a college project.

It creates personalized 7-day workout plans based on the user's fitness details, fitness goal, and workout intensity.

The application uses FastAPI for the backend, SQLite for database storage, Jinja2 for web pages, and Google Gemini AI for generating and updating workout plans.

## Main Features

- User fitness details input
- Personalized 7-day AI workout plan
- Fitness goal and workout intensity
- Nutrition and recovery tips
- User feedback
- AI-based workout plan update
- SQLite database storage
- Admin page to view users
- Delete user records
- Responsive fitness-themed interface
- Gym-themed background

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Jinja2
- HTML5
- CSS3
- Google Gemini AI
- Uvicorn
- python-dotenv

## Project Structure

```text
FitBuddy/
├── README.md
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py
    ├── database.py
    ├── routes.py
    ├── schemas.py
    ├── gemini_generator.py
    ├── gemini_flash_generator.py
    ├── nutrition.py
    ├── updated_plan.py
    │
    ├── templates/
    │   ├── index.html
    │   ├── result.html
    │   └── all_users.html
    │
    └── static/
        └── images/
            └── gym-background.jpg
