def calculate_bmr(
    age: int,
    gender: str,
    height_cm: float,
    weight_kg: float
):

    gender = gender.lower()

    if gender in ["male", "m"]:
        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            + 5
        )

    elif gender in ["female", "f"]:
        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            - 161
        )

    else:
        raise ValueError("Gender must be male or female")

    return round(bmr, 2)


def calculate_tdee(bmr: float, activity_level: str):

    activity_factors = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderate": 1.55,
        "highly active": 1.725,
        "extremely active": 1.9
    }

    activity_level = activity_level.lower()

    if activity_level not in activity_factors:
        raise ValueError("Invalid activity level")

    return round(
        bmr * activity_factors[activity_level],
        2
    )


def calculate_calorie_target(
    tdee: float,
    goal: str
):



    if goal == "Weight Loss":
        target = tdee - 400

    elif goal == "Maintenance":
        target = tdee

    elif goal == "Weight Gain":
        target = tdee + 400

    else:
        raise ValueError(
            "Goal must be Weight Loss, Maintenance or Weight Gain"
        )

    return round(target, 2)


def calculate_bmi(
    height_cm: float,
    weight_kg: float
):

    height_m = height_cm / 100

    bmi = weight_kg / (height_m ** 2)

    return round(bmi, 2)


def calculate_protein_target(
    weight_kg: float,
    goal: str,
    age: int
):
    if age < 18:
        base = 1.0
    else:
        base = 0.8
        
    if goal == "Weight Loss":
        multiplier = max(1.2, base + 0.4)
    elif goal == "Weight Gain":
        multiplier = max(1.6, base + 0.8)
    else:
        multiplier = base
        
    return round(weight_kg * multiplier, 1)