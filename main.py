from fastapi import FastAPI

app = FastAPI(
    title="Training Good Habits"
)

fake_users = [
    {"id": 1, "age": 15, "name": "Andrey"},
    {"id": 2, "age": 14, "name": "Roman"},
    {"id": 3, "age": 10, "name": "Svetlana"},
]

fake_categories = [
    {"id": 1, "name_habit": "economy", "emoji": "❤"},
    {"id": 2, "name_habit": "health", "emoji": "💰"},
    {"id": 3, "name_habit": "study", "emoji": "📗"},
]

fake_habits = [
    {"id": 1, "user_id": 1, "category_id": 3, "name": "Russian language"},
    {"id": 2, "user_id": 2, "category_id": 3, "name": "math"},
    {"id": 3, "user_id": 3, "category_id": 1, "name": "save money"},
    {"id": 4, "user_id": 3, "category_id": 1, "name": "earn money"},
]


@app.get("/users", tags=["Users"])
def get_users(user_id: int = None, limit: int = 10, offset: int = 0):
    if user_id is not None:
        return [user for user in fake_users if user.get("id") == user_id]
    if user_id is None:
        return fake_users[offset:][:limit]


@app.post("/users", tags=["Users"])
def change_users_data(user_id: int, new_name: str = None, new_age: int = None):
    current_user = next((user for user in fake_users if user["id"] == user_id), None)
    if current_user:
        if new_name is not None:
            current_user["name"] = new_name
        if new_age is not None:
            current_user["age"] = new_age
        return {"status": 200, "data": current_user}
    return {"status": 404, "message": f"User with id {user_id} not found"}


@app.delete("/users", tags=["Users"])
def remove_users(user_id: int):
    user_to_delete = next((user for user in fake_users if user["id"] == user_id), None)
    if user_to_delete:
        fake_users.remove(user_to_delete)
        return {"status": 200, "message": f"User with id {user_id} deleted"}
    return {"status": 404, "message": f"User with id {user_id} not found"}


@app.get("/category", tags=["Categories"])
def get_categories(category_id: int = None, limit: int = 10, offset: int = 0):
    if category_id is not None:
        return [category for category in fake_categories if category["id"] == category_id]
    return fake_categories[offset:offset+limit]


@app.post("/category", tags=["Categories"])
def add_or_change_categories(category_id: int, command: str = "add", name_habit: str = "", emoji: str = ""):
    if command == "add":
        fake_categories.append({"id": category_id, "name_habit": name_habit, "emoji": emoji})
        return {"status": 200, "data": [category for category in fake_categories if category["id"] == category_id]}
    elif command == "change":
        current_category = next((category for category in fake_categories if category["id"] == category_id), None)
        if current_category:
            current_category["name_habit"] = name_habit
            current_category["emoji"] = emoji
            return {"status": 200, "data": current_category}
        return {"status": 404, "message": f"Category with id {category_id} not found"}
    return {"status": 400, "message": f"Invalid command: {command}"}


@app.delete("/category", tags=["Categories"])
def remove_categories(category_id: int):
    category_to_delete = next((category for category in fake_categories if category["id"] == category_id), None)
    if category_to_delete:
        fake_categories.remove(category_to_delete)
        return {"status": 200, "message": f"Category with id {category_id} deleted"}
    return {"status": 404, "message": f"Category with id {category_id} not found"}


@app.get("/habits", tags=["Habits"])
def get_habits(user_id: int = None, limit: int = 10, offset: int = 0, category_id: int = None):
    filtered_habits = [habit for habit in fake_habits if (habit["user_id"] == user_id if user_id else True) and
                       (habit["category_id"] == category_id if category_id else True)]
    return filtered_habits[offset:offset+limit]


@app.post("/habits", tags=["Habits"])
def habits_data(user_id: int, command: str = "add", new_user: int = "", new_category: int = "", new_name: str = ""):
    if command == "add":
        fake_habits.append({"id": user_id, "user_id": new_user, "category_id": new_category, "name": new_name})
        return {"status": 200, "data": [habit for habit in fake_habits if habit["id"] == user_id]}
    elif command == "change":
        current_habit = next((habit for habit in fake_habits if habit["id"] == user_id), None)
        if current_habit:
            current_habit["name"] = new_name
            current_habit["category_id"] = new_category
            return {"status": 200, "data": current_habit}
        return {"status": 404, "message": f"Habit with id {user_id} not found"}
    return {"status": 400, "message": f"Invalid command: {command}"}


@app.delete("/habits", tags=["Habits"])
def remove_habits(user_id: int):
    current_habit = next((habit for habit in fake_habits if habit["id"] == user_id), None)
    if current_habit:
        old_habit = [category for category in fake_categories if category.get("id") == user_id]
        fake_habits.remove(current_habit)
        return {"status": 200, "message": f"Category: {old_habit} was deleted"}
    return {"status": 404, "message": f"Habit with id {user_id} not found"}
