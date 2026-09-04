from fastapi import APIRouter, HTTPException

from backend.schemas import UserProfile
from backend.services.calorie_service import (
    calculate_bmr,
    calculate_tdee,
    calculate_calorie_target,
    calculate_bmi,
    calculate_protein_target
)

router = APIRouter(
    prefix="/api/calorie",
    tags=["Calorie Calculator"]
)


@router.post("/calculate")
def calculate_calories(user: UserProfile):

    try:

        bmr = calculate_bmr(
            user.age,
            user.gender,
            user.height_cm,
            user.weight_kg
        )

        tdee = calculate_tdee(
            bmr,
            user.activity_level
        )

        calorie_target = calculate_calorie_target(
            tdee,
            user.goal
        )

        bmi = calculate_bmi(
            user.height_cm,
            user.weight_kg
        )

        protein_target = calculate_protein_target(
            user.weight_kg,
            user.goal,
            user.age
        )

        return {
            "bmr": bmr,
            "tdee": tdee,
            "bmi": bmi,
            "daily_calorie_target": calorie_target,
            "daily_protein_target": protein_target,
            "goal": user.goal
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )