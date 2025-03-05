from typing import Optional, List
from pydantic import BaseModel

# Esquema base para Todo
class TodoBase(BaseModel):
    name: str
    completed: bool = False

# Esquema para crear un Todo
class TodoCreate(TodoBase):
    pass

# Esquema para actualizar un Todo
class TodoUpdate(BaseModel):
    name: Optional[str] = None
    completed: Optional[bool] = None

# Esquema para respuesta de Todo
class Todo(TodoBase):
    id: int

    class Config:
        from_attributes = True  # Antes era orm_mode = True en Pydantic v1

# Esquema para respuesta de poema
class PoemResponse(BaseModel):
    poem: str