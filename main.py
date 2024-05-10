from typing import List
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
app = FastAPI(title="Training Good Habits")


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": str(exc)})
    )
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )

class User(BaseModel):
    id: int = Field(ge=0)
    age: int = Field(ge=0)
    name: str

fake_users = [
    User(id=1, age=15, name='Andrey'),
    User(id=2, age=14, name='Roman'),
    User(id=3, age=10, name='Svetlana'),
]


@app.get("/users", tags=["Users"], response_model=List[User])
def get_users(id: int = None, limit: int = 10, offset: int = 0):
    return [user for user in fake_users if (user.id == id if id else True)][offset:offset + limit
                                        if offset + limit < len(fake_users) else None]

@app.post("/users", tags=["Users"])
def add_user(users: List[User]):
    for user in users:
        current_user = next((u for u in fake_users if u.id == user.id), None)
        if current_user:
            raise HTTPException(status_code=400, detail=f"User with id {user.id} already exists")
        fake_users.append(user)
    return {"status": 200, "data": fake_users[-1]}

@app.put("/users", tags=["Users"])
def change_user(user: User):
    current_user = next((u for u in fake_users if u.id == user.id), None)
    if not current_user:
        raise HTTPException(status_code=404, detail=f"User with id {user.id} not found")
    current_user.name = user.name
    current_user.age = user.age
    return {"status": 200, "data": current_user}


@app.delete("/users", tags=["Users"])
def remove_user(id: int):
    current_user = next((u for u in fake_users if u.id == id), None)
    if not current_user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    fake_users.remove(current_user)
    return {"message": f"User with id {id} removed successfully"}

class Category(BaseModel):
    id: int = Field(ge=0)
    name: str
    emoji: str = Field(max_length=1)

fake_categories = [
    Category(id=1, name='economy', emoji='💰'),
    Category(id=2, name='health', emoji='❤'),
    Category(id=3, name='study', emoji='📗'),
]

@app.get("/categories", tags=["Categories"], response_model=List[Category])
def get_categories(id: int = None, limit: int = 10, offset: int = 0):
    return [category for category in fake_categories if (category.id == id if id else True)][offset:offset + limit
    if offset + limit < len(fake_categories) else None]

@app.post("/categories", tags=["Categories"])
def add_category(categories: List[Category]):
    for category in categories:
        if any(current_category.id == category.id for current_category in fake_categories):
            raise HTTPException(status_code=400, detail=f"Category with id {category.id} already exists")

    fake_categories.extend(categories)
    return {"status": 200, "data": fake_categories[-1]}


@app.put("/categories", tags=["Categories"])
def change_category(category: Category):
    current_category = next((c for c in fake_categories if c.id == category.id), None)
    if not current_category:
        raise HTTPException(status_code=404, detail=f"User with id {category.id} not found")
    current_category.id = category.id
    current_category.name = category.name
    current_category.emoji = category.emoji
    return {"status": 200, "data": current_category}



@app.delete("/categories", tags=["Categories"])
def remove_category(id: int):
    category_to_delete = next((category for category in fake_categories if category.id == id), None)
    if category_to_delete:
        fake_categories.remove(category_to_delete)
        return {"status": 200, "message": f"Category with id {id} deleted"}
    return {"status": 404, "message": f"Category with id {id} not found"}

class Habit(BaseModel):
    id: int = Field(ge=0)
    user_id: int = Field(ge=0)
    category_id: int = Field(ge=0)
    name: str

fake_habits = [
    Habit(id=1, user_id=1, category_id=3, name='Russian language'),
    Habit(id=2, user_id=2, category_id=3, name='math'),
    Habit(id=3, user_id=3, category_id=1, name='save money'),
    Habit(id=4, user_id=3, category_id=1, name='earn money'),
]

@app.get("/habits", tags=["Habits"])
def get_habits(user_id: int = None, limit: int = 10, offset: int = 0, category_id: int = None):
    filtered_habits = [habit for habit in fake_habits if (habit.user_id == user_id if user_id else True) and
                       (habit.category_id == category_id if category_id else True)]
    return filtered_habits[offset:offset + limit if offset + limit < len(fake_habits) else None]


@app.post("/habits", tags=["Habits"])
def add_habit(habits: List[Habit]):
    for habit in habits:
        if any(current_habit.id == habit.id for current_habit in fake_habits):
            raise HTTPException(status_code=400, detail=f"Habit with id {habit.id} already exists")
    fake_habits.extend(habits)
    return {"status": 200, "data": fake_habits[-1]}



@app.put("/habits", tags=["Habits"])
def change_habit(habit: Habit):
    current_habit = next((h for h in fake_habits if h.id == habit.id), None)
    if not current_habit:
        raise HTTPException(status_code=404, detail=f"Habit with id {habit.id} not found")
    current_habit.id = habit.id
    current_habit.user_id = habit.user_id
    current_habit.category_id = habit.category_id
    current_habit.name = habit.name
    return {"status": 200, "data": current_habit}

@app.delete("/habits", tags=["Habits"])
def remove_habit(id: int):
    current_habit = next((habit for habit in fake_habits if habit.id == id), None)
    if not current_habit:
        raise HTTPException(status_code=404, detail=f"Habit with id {id} not found")
    old_habit = [h for h in fake_habits if h.id == id]
    fake_habits.remove(current_habit)
    return {"status": 200, "message": f"Habit: {old_habit} was deleted"}
