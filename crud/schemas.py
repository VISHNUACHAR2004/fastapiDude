from pydantic import BaseModel

# ---------- INPUT MODEL ----------
class UserCreate(BaseModel):
    name: str
    age: int

# ---------- OUTPUT MODEL ----------
class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True
