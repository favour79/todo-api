from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import repository

app = FastAPI()

@app.get("/", summary="API info")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}

@app.get("/tasks", summary="List all tasks")
def get_tasks():
    return repository.get_all_tasks()

@app.get("/tasks/{task_id}", summary="Get one task by id")
def get_task(task_id: int):
    task = repository.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

class TaskCreate(BaseModel):
    title: str

@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")
    return repository.create_task(task.title)

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

@app.put("/tasks/{task_id}", summary="Update a task's title and/or done status")
def update_task(task_id: int, update: TaskUpdate):
    if update.title is not None and not update.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    updated = repository.update_task(task_id, title=update.title, done=update.done)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return updated

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    deleted = repository.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")