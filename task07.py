'''Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс Task с полями id, title, description и status.
Создайте список tasks для хранения задач.
Создайте функцию get_tasks для получения списка всех задач (метод GET).
Создайте функцию get_task для получения информации о задаче по её ID
(метод GET).
Создайте функцию create_task для добавления новой задачи (метод POST).
Создайте функцию update_task для обновления информации о задаче по её ID
(метод PUT).
Создайте функцию delete_task для удаления задачи по её ID (метод DELETE).'''

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI(title="FastAPI App")

class Status(Enum):
    TODO = 1
    INPROGRESS = 2
    DONE = 3

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str

class TaskMod(BaseModel):
    title: str
    description: str
    status: str

tasks = []
tasks.append(Task(id=1, title='sleep', description='sleep well', status=Status.TODO.name))

@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task_by_id(task_id: int):
    is_task = [task for task in tasks if task.id == task_id]
    if is_task:
        return is_task[0]
    raise HTTPException(status_code=404, detail='No task with such id')

@app.post('/tasks')
async def add_task(task: TaskMod):
    next_id = max(tasks, key=lambda x: x.id).id + 1
    next_task = Task(id=next_id, title=task.title, description=task.description, status=task.status)
    tasks.append(next_task)
    return 'New task added'

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: TaskMod):
    is_task = [task for task in tasks if task.id == task_id]
    if not is_task:
        raise HTTPException(status_code=404, detail='No task with such id')
    is_task[0].title = task.title
    is_task[0].description = task.description
    is_task[0].status = task.status
    return is_task[0]

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    is_task = [task for task in tasks if task.id == task_id]
    if not is_task:
        raise HTTPException(status_code=404, detail='No task with such id')
    tasks.pop(task_id - 1)