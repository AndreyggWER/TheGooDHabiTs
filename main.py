from fastapi import FastAPI, HTTPException

app = FastAPI(title="Training Good Habits")


fake_users = [
    {"id": 1, "age": 15, "name": "Andrey"},
    {"id": 2, "age": 14, "name": "Roman"},
    {"id": 3, "age": 10, "name": "Svetlana"},
]

fake_categories = [
    {"id": 1, "name": "economy", "emoji": "❤"},
    {"id": 2, "name": "health", "emoji": "💰"},
    {"id": 3, "name": "study", "emoji": "📗"},
]

fake_habits = [
    {"id": 1, "user_id": 1, "category_id": 3, "name": "Russian language"},
    {"id": 2, "user_id": 2, "category_id": 3, "name": "math"},
    {"id": 3, "user_id": 3, "category_id": 1, "name": "save money"},
    {"id": 4, "user_id": 3, "category_id": 1, "name": "earn money"},
]


@app.get("/users", tags=["Users"])
def get_users(id: int = None, limit: int = 10, offset: int = 0):
    return [user for user in fake_users if (user.get("id") == id if id else True)][offset:offset + limit
                                        if offset + limit < len(fake_users) else None]

@app.post("/users", tags=["Users"])
def add_user(id: int, name: str, age: int):
    current_user = next((u for u in fake_users if u["id"] == id), None)
    if current_user:
        return {"status": 400, "message": f"User with id {id} already exists"}
    fake_users.append({"id": id, "name": name, "age": age})
    return {"status": 200, "data": fake_users[-1]}

@app.put("/users", tags=["Users"])
def change_user(id: int, name: str = None, age: int = None):
    current_user = next((u for u in fake_users if u["id"] == id), None)
    if not current_user:
        return {"status": 404, "message": f"User with id {id} not found"}
    current_user.update({"name": name or current_user["name"], "age": age or current_user["age"]})
    return {"status": 200, "data": current_user}

@app.delete("/users", tags=["Users"])
async def remove_user(id: int):
    current_user = next((u for u in fake_users if u["id"] == id), None)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    fake_users.remove(current_user)
    return {"message": "User removed successfully"}

##################

@app.get("/categories", tags=["Categories"])
def get_categories(id: int = None, limit: int = 10, offset: int = 0):
    return [category for category in fake_categories
    if (category["id"] == id if id else True)][offset:offset + limit
    if offset + limit < len(fake_categories) else None]

@app.post("/categories", tags=["Categories"])
def add_category(id: int, name: str, emoji: str):
    current_category = next((c for c in fake_categories if c["id"] == id), None)
    if current_category:
        return {"status": 400, "message": f"Category with id {id} already exists"}
    fake_categories.append({"id": id, "name": name, "emoji": emoji})
    return {"status": 200, "data": fake_categories[-1]}

@app.put("/categories", tags=["Categories"])
def change_category(id: int, name: str, emoji: str):
    current_category = next((c for c in fake_categories if c["id"] == id), None)
    if not current_category:
        return {"status": 404, "message": f"Category with id {id} not found"}
    current_category.update({"name": name or current_category["name"], "emoji": emoji or current_category["emoji"]})
    return {"status": 200, "data": current_category}

@app.delete("/categories", tags=["Categories"])
def remove_category(id: int):
    category_to_delete = next((category for category in fake_categories if category["id"] == id), None)
    if category_to_delete:
        fake_categories.remove(category_to_delete)
        return {"status": 200, "message": f"Category with id {id} deleted"}
    return {"status": 404, "message": f"Category with id {id} not found"}

##################

@app.get("/habits", tags=["Habits"])
def get_habits(user_id: int = None, limit: int = 10, offset: int = 0, category_id: int = None):
    filtered_habits = [habit for habit in fake_habits if (habit["user_id"] == user_id if user_id else True) and
                       (habit["category_id"] == category_id if category_id else True)]
    return filtered_habits[offset:offset + limit if offset + limit < len(fake_habits) else None]


@app.post("/habits", tags=["Habits"])
def add_habit(id: int, user_id: int = "", category_id: int = "", name: str = ""):
    current_habit = next((h for h in fake_habits if h["id"] == id), None)
    if current_habit:
        return {"status": 400, "message": f"Habit with id {id} already exists"}
    fake_habits.append({"id": id,"user_id": user_id, "category_id": category_id, "name": name})
    return {"status": 200, "data": fake_habits[-1]}

@app.put("/habits", tags=["Habits"])
def change_habit(id: int, user_id: int = "", category_id: int = "", name: str = ""):
    current_habit = next((h for h in fake_habits if h["id"] == id), None)
    if not current_habit:
        return {"status": 400, "message": f"Habit with id {id} not found"}
    current_habit.update({"id": id or current_habit["id"],
                        "user_id": user_id or current_habit["user_id"],
                        "category_id": category_id or current_habit["category_id"],
                        "name": name or current_habit["name"]})
    return {"status": 200, "data": current_habit}


@app.delete("/habits", tags=["Habits"])
def remove_habit(id: int):
    current_habit = next((habit for habit in fake_habits if habit["id"] == id), None)
    if not current_habit:
        return {"status": 404, "message": f"Habit with id {id} not found"}
    old_habit = [h for h in fake_habits if h.get("id") == id]
    fake_habits.remove(current_habit)
    return {"status": 200, "message": f"Habit: {old_habit} was deleted"}
