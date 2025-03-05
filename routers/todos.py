from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import schemas
import models
import crud
from database import SessionLocal
import google.generativeai as genai

router = APIRouter(
    prefix="/todos"
)

# Configurar la API de Gemini
genai.configure(api_key="AIzaSyDJrVuMpsP2aicUn0Oc_g5gDaezR5Z4MIo")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)

@router.get("", response_model=List[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

@router.get("/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.put("/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/{todo_id}", response_model=schemas.Todo)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.post("/write-poem/{todo_id}", response_model=schemas.PoemResponse)
def write_poem(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Usar Gemini para generar un poema basado en la tarea
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Escribe un poema corto y creativo sobre la siguiente tarea: '{todo.name}'. El poema debe ser de 4 a 6 líneas."
    
    try:
        response = model.generate_content(prompt)
        poem = response.text
        return {"poem": poem}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating poem: {str(e)}")