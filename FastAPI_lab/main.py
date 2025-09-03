from fastapi import FastAPI, Path, Query
from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl

app = FastAPI()



class User(BaseModel):
    name: str
    email: EmailStr
    website: HttpUrl
    age: Optional[int] = Field(None, ge=13, le=90)
    friends: Optional[int] = 0

user = User(name="John", email="john@example.com", website="https://john.com", age=25, friends=10)
print(user)
# Output: User(name='John', email='john@example.com', website='https://john.com', age=25, friends=10)

# Validation error (age is below the minimum)
user = User(name="Jane", email="jane@example.com", website="https://jane.com", age=15)
print(user)
# Output: pydantic.error_wrappers.ValidationError: 1 validation error for User
# age
#   ensure this value is greater than or equal to 13 (type=value_error.number.not_ge; limit_value=13)

# Validation error (website is not a valid URL)
user = User(name="Bob", email="bob@example.com", website="invalid url", age=20)
print(user)
# Output: pydantic.error_wrappers.ValidationError: 1 validation error for User
# website
#   invalid or missing URL scheme (type=value_error.url.scheme)



class Note(BaseModel):
    name: str
    description: str
    done: bool

@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/notes")
async def read_notes(skip: int = 0, limit: Annotated [int, Query(le=100, ge=10)] = 10):
    return {"message": f"Return all notes: skip: {skip}, limit: {limit}"}

@app.post("/notes")
async def create_note(note: Note):
    return {"name": note.name, "description": note.description, "status": note.done}


@app.get("/notes/new")
async def read_new_notes():
    return {"message": "Return new notes"}


@app.get("/notes/{note_id}")
async def read_note(note_id: int = Path(description="The ID of the note to get", gt=0, le=10)):
    return {"note": note_id}

