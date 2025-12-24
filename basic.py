from fastapi import FastAPI
from fastapi.responses import HTMLResponse 
app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"message": "Hello, World!"}

@app.get("/user/{user_id}")

def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User{user_id}"}

#POST Request (Send data to create something)
@app.post("/user/")
def create_user(name: str, age: int, city: str, country: str, email: str, phone: str):
    return {"Thankyou": f"User {name} from {city}, {country} created successfully!"}

#PUT Request (Update existing data)
@app.put("/user/{user_id}")
def update_user(user_id: int, name: str = None, age: int = None):
    updated_info = {"user_id": user_id}
    if name:
        updated_info["name"] = name
    if age:
        updated_info["age"] = age
    return {"Updated User Info": updated_info}

#DELETE Request (Remove data)
@app.delete("/user/{user_id}")  
def delete_user(user_id: int):
    return {"message": f"User with ID {user_id} has been deleted."}    
sss
sss
sss
sss
s
s