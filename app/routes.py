import os

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import (
    SessionLocal,
    User,
    WorkoutPlan,
    delete_user,
    get_original_plan,
    get_user,
    save_plan,
    save_user,
    update_plan
)

from app.gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from app.gemini_generator import (
    generate_workout_gemini
)

from app.nutrition import get_fallback_tip

from app.updated_plan import (
    update_workout_plan
)


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

templates = Jinja2Templates(
    directory=os.path.join(
        BASE_DIR,
        "templates"
    )
)

router = APIRouter()


def get_tip(goal):

    tip = generate_nutrition_tip_with_flash(goal)

    if tip.startswith("Error"):
        return get_fallback_tip(goal)

    return tip


@router.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request,
        "index.html",
        {}
    )


@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout_page(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    save_user(
        user_id,
        username,
        age,
        weight,
        goal,
        intensity
    )

    plan = generate_workout_gemini({
        "goal": goal,
        "intensity": intensity
    })

    save_plan(user_id, plan)

    nutrition_tip = get_tip(goal)

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": plan,
            "nutrition_tip": nutrition_tip,
            "message": None
        }
    )


@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):

    user = get_user(user_id)
    original = get_original_plan(user_id)

    if not user or not original:
        raise HTTPException(
            status_code=404,
            detail="Plan not found."
        )

    updated = update_workout_plan(
        original,
        feedback
    )

    update_plan(
        user_id,
        updated
    )

    nutrition_tip = get_tip(user.goal)

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "username": user.name,
            "user_id": user.id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": updated,
            "nutrition_tip": nutrition_tip,
            "message":
                "Your plan was updated successfully!"
        }
    )


@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(request: Request):

    db = SessionLocal()

    users = db.query(User).all()

    user_data = []

    for user in users:

        plan = db.query(
            WorkoutPlan
        ).filter(
            WorkoutPlan.user_id == user.id
        ).first()

        user_data.append({
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "original_plan":
                plan.original_plan if plan else "N/A",
            "updated_plan":
                plan.updated_plan
                if plan and plan.updated_plan
                else "Not updated"
        })

    db.close()

    return templates.TemplateResponse(
        request,
        "all_users.html",
        {
            "users": user_data
        }
    )


@router.post(
    "/delete-user/{user_id}"
)
def delete_user_route(user_id: int):

    delete_user(user_id)

    return RedirectResponse(
        url="/view-all-users",
        status_code=303
    )


@router.post(
    "/generate-workout/gemini"
)
def generate_gemini_workout(request_data: dict):

    result = generate_workout_gemini(
        request_data
    )

    return {
        "model": "gemini-pro",
        "workout_plan": result
    }


@router.get("/nutrition-tip")
def nutrition_tip(goal: str):

    return {
        "goal": goal,
        "nutrition_tip":
            generate_nutrition_tip_with_flash(goal)
    }
