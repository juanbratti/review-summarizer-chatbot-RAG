from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

class Subtask(BaseModel): # tipo dato subtarea
    id: int
    title: str
    completed: bool

class Task(BaseModel): # tipo de dato tarea
    id: int
    title: str
    description: str
    completed: bool = False # predeterminado es false
    priority: Optional[int] = Field(None, ge=1, le=5, description="1 <= priority <= 5")
    due_date: Optional[datetime]
    category: Optional[str]
    subtasks: List[Subtask] = []

# no tenemos bd asiq ponemos todas las tareas en una lista de python
my_tasks = []

#################### hago los endpoints ####################

## Con método GET

# para devolver lista con las tareas existentes
@app.get("/my_tasks", response_model=List[Task])
def get_all_tasks():
    return my_tasks 

# para obtener los detalles de una tarea con id task_id
@app.get("/my_tasks/{task_id}", response_model=Task)
def get_specific_task(task_id: int):
    # busco la tarea con el id dado
    if not any(task["id"] == task_id for task in my_tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        for task in my_tasks:
            if task["id"] == task_id:
                return task

## Con método POST

# para crear una nueva tarea, devuelvo la tarea que se crea
@app.post("/my_tasks", response_model=Task, status_code=201)
def create_task(task: Task):
    if any(existing_task["id"] == task.id for existing_task in my_tasks):
        raise HTTPException(status_code=400, detail="ID is already taken")
    else: 
        my_tasks.append(task.dict()) # antes de guardar a lista, transformo a dict.
    return task

## Con método PUT

# para actualizar tarea ya existente
@app.put("/my_tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    if not any(existing_task["id"] == task_id for existing_task in my_tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    else: 
        for index, task in enumerate(my_tasks):
            if task["id"] == task_id:
                my_tasks[index] = updated_task.dict()
                return updated_task

# para borrar tarea
@app.delete("/my_tasks/{task_id}", status_code=200)
def delete_task(task_id: int):
    global my_tasks
    if not any(task["id"] == task_id for task in my_tasks):
        raise HTTPException(status_code=404, detail="The task with that id doesn't exist")
    else:
        my_tasks = [task for task in my_tasks if task["id"] != task_id]
    