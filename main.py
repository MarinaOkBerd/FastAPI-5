import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()


class Task(BaseModel):
    title: str
    description: str
    completed: bool = False


db: Dict[int, Task] = {}


def get_next_task_id() -> int:
    return max(db, default=0) + 1


@app.get("/tasks/")
def get_tasks():
    return db.values()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="task not found")
    return db[task_id]


@app.post("/tasks/")
def create_task(task: Task):
    task_id = get_next_task_id()
    db[task_id] = task
    return {"task_id": task_id}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="task not found")
    db[task_id] = task
    return {"task_id": task_id}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="task not found")
    del db[task_id]
    return {"message": "task deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)