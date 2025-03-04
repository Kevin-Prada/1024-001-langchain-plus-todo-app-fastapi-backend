from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import schemas
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

@router.post("", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    todo = crud.create_todo(db, todo)
    return todo

@router.get("", response_model=List[schemas.ToDoResponse])
def get_todos(completed: bool = None, db: Session = Depends(get_db)):
    todos = crud.read_todos(db, completed)
    return todos

@router.get("/{id}")
def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo

@router.put("/{id}")
def update_todo(id: int, todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    todo = crud.update_todo(db, id, todo)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_todo(id: int, db: Session = Depends(get_db)):
    res = crud.delete_todo(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="to do not found")
    
    
# LANGCHAIN
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