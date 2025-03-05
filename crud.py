from sqlalchemy.orm import Session
import models, schemas

def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()

def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(name=todo.name, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def read_todos(db: Session, completed: bool):
    if completed is None:
        return db.query(models.ToDo).all()
    else:
        return db.query(models.ToDo).filter(models.ToDo.completed == completed).all()

def read_todo(db: Session, id: int):
    return db.query(models.ToDo).filter(models.ToDo.id == id).first()

def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    db_todo = get_todo(db, todo_id)
    if db_todo:
        for key, value in todo.model_dump(exclude_unset=True).items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo