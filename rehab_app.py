from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define models
class Exercise(BaseModel):
    name: str
    category: str
    description: str
    progression: str

class PlanRequest(BaseModel):
    name: str
    age: int
    injury: str
    fitness_level: str
    goals: List[str]

class PlanResponse(BaseModel):
    name: str
    injury: str
    plan: List[str]

# Exercise library
exercise_library = [
    Exercise(
        name="Calf Raise",
        category="Strength",
        description="Stand on the balls of your feet and lift your heels off the ground. Hold briefly and lower back down.",
        progression="Progress to single-leg calf raises or weighted calf raises."
    ),
    Exercise(
        name="Hip Bridge",
        category="Strength",
        description="Lie on your back with knees bent and feet flat on the floor. Lift your hips until your body forms a straight line.",
        progression="Add a resistance band or progress to single-leg bridges."
    ),
    Exercise(
        name="Seated Heel Raises",
        category="Strength",
        description="While seated, raise your heels off the ground and lower back down.",
        progression="Increase resistance by holding a dumbbell on your thighs."
    ),
    Exercise(
        name="Isometric Wall Sit",
        category="Isometric Strength",
        description="Lean against a wall with knees bent at 90 degrees and hold the position.",
        progression="Hold for longer durations or add resistance by holding a weight."
    ),
    Exercise(
        name="Side-lying Hip Abduction",
        category="Strength",
        description="Lie on your side with legs straight. Lift the top leg upward and lower slowly.",
        progression="Add a resistance band around your thighs for extra difficulty."
    ),
    Exercise(
        name="Single-leg Deadlift",
        category="Strength and Balance",
        description="Balance on one leg, hinge at the hips, and lower your torso until parallel to the ground. Return to standing.",
        progression="Hold a dumbbell in the opposite hand to the standing leg for increased difficulty."
    ),
    Exercise(
        name="Step-up to Knee Drive",
        category="Strength and Power",
        description="Step onto a box with one leg and drive the opposite knee upward. Step back down and repeat.",
        progression="Add weight by holding dumbbells or increase the height of the box."
    ),
    Exercise(
        name="Skipping with Low Impact",
        category="Plyometric",
        description="Perform skipping in place with a focus on soft landings and quick rebounds.",
        progression="Increase speed or duration of skipping sessions."
    ),
    Exercise(
        name="Split Squat with Isometric Hold",
        category="Strength and Stability",
        description="Get into a split squat position and hold the bottom position for a few seconds before returning to standing.",
        progression="Add a resistance band or weights to increase difficulty."
    ),
    Exercise(
        name="Glute Bridge March",
        category="Strength and Coordination",
        description="Lie on your back, lift hips into a bridge, and alternate lifting one leg off the ground.",
        progression="Add a resistance band or hold weights on your hips."
    ),
    Exercise(
        name="Incline Plyometric Push-Up",
        category="Power",
        description="Perform a push-up on an elevated surface and push explosively upward to lift hands slightly off the surface.",
        progression="Reduce incline or transition to floor push-ups."
    ),
    Exercise(
        name="Tibialis Raise",
        category="Strength",
        description="Stand with your back against a wall, heels slightly forward, and raise toes upward toward the shin.",
        progression="Add resistance by holding a weight plate on your toes."
    )
]

# Add the generate-plan endpoint
@app.post("/generate-plan/", response_model=PlanResponse)
def generate_plan(request: PlanRequest):
    # Initialize an empty plan
    plan = []

    # Include exercises based on injury
    if request.injury.lower() == "achilles tendinopathy":
        plan.extend([
            f"{exercise.name}: {exercise.description}" for exercise in exercise_library
            if "calf" in exercise.name.lower() or "heel" in exercise.name.lower()
        ])
        if "Return to running" in request.goals:
            plan.append("Gradual running progression starting with walk/run intervals")

    elif request.injury.lower() == "hip pain":
        plan.extend([
            f"{exercise.name}: {exercise.description}" for exercise in exercise_library
            if "hip" in exercise.name.lower()
        ])

    else:
        plan.extend([
            f"{exercise.name}: {exercise.description}" for exercise in exercise_library
        ])

    # Return the plan
    return PlanResponse(
        name=request.name,
        injury=request.injury,
        plan=plan
    )
