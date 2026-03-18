from uuid import uuid4

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get('/')
def get_book():
    return {"message": "Hello, world!"}


class Task(BaseModel):
    """Модель задачи"""
    id: str
    title: str
    completed: bool = False


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


tasks: list[Task] = []


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    """Получить список задач"""
    return tasks


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    """Создать новую задачу"""
    task = Task(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(task)
    return task


class BookInput(BaseModel):
    book: str
    favorite: bool = False


books: list[BookInput] = []


@app.post("/books")
def add_book(added_book: BookInput):
    books.append(added_book)
    return {"status": "ok"}


@app.get("/favorite_book")
def get_favorite_book():
    favorites = [b.book for b in books if b.favorite]
    if favorites:
        return {"message": f"Любимая книга: {favorites}"}
    return {"message": "Пока нет ни одной книги"}
