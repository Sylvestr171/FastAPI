from fastapi import FastAPI, Path, Query, HTTPException, Depends, status
from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_db,Note

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

# Valpoetrpoetry 

class NoteModel(BaseModel):
    name: str
    description: str
    done: bool

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

@app.get("/notes")
async def read_notes(skip: int = 0, limit: Annotated [int, Query(le=100, ge=10)] = 10, db: Session = Depends(get_db)):
    notes = db.query(Note).offset(skip).limit(limit).all()
    return notes

@app.post("/notes")
async def create_note(note: NoteModel, db: Session = Depends(get_db)):
    new_note = Note(name=note.name, description=note.description, done=note.done)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.get("/notes/new")
async def read_new_notes():
    return {"message": "Return new notes"}


@app.get("/notes/{note_id}")
async def read_note(note_id: int = Path(description="The ID of the note to get", gt=0, le=10),
                    db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return note
