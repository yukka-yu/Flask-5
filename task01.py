'''Создать API для управления списком задач. Приложение должно иметь
возможность создавать, обновлять, удалять и получать список задач.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс Task с полями id, title, description и status.
Создайте список tasks для хранения задач.
Создайте маршрут для получения списка задач (метод GET).
Создайте маршрут для создания новой задачи (метод POST).
Создайте маршрут для обновления задачи (метод PUT).
Создайте маршрут для удаления задачи (метод DELETE).
Реализуйте валидацию данных запроса и ответа.'''

from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="FastAPI App")

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: bool

class TaskMod(BaseModel):
    title: str
    description: Optional[str]
    status: bool

tasks = []
tasks.append(Task(id=1, title='sleep', description='sleep well', status='False'))

@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task_by_id(task_id: int):
    task = [task for task in tasks if task.id == task_id]
    if task:
        return task[0]
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


