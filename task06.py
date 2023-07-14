'''Создать веб-страницу для отображения списка пользователей. Приложение
должно использовать шаблонизатор Jinja для динамического формирования HTML
страницы.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
содержать заголовок страницы, таблицу со списком пользователей и кнопку для
добавления нового пользователя.
Создайте маршрут для отображения списка пользователей (метод GET).
Реализуйте вывод списка пользователей через шаблонизатор Jinja.'''
 
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="FastAPI App")
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str

class UserMod(BaseModel):
    name: str
    email: str
    password: str

users = []
users.append(User(id=1, name='Kit', email='kit@example.com', password='abc123'))
users.append(User(id=2, name='Tom', email='tom@example.com', password='xyz123'))

@app.get("/users", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.post('/users')
async def add_task(user: UserMod):
    next_id = max(users, key=lambda x: x.id).id + 1
    next_user = User(id=next_id, title=user.name, email=user.email, password=user.password)
    users.append(next_user)
    return 'New user added'

