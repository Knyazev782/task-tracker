from uuid import uuid4

from fastapi import FastAPI, status, HTTPException
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
        return {"message": f"Любимые книги: {favorites}"}
    return {"message": "Пока нет ни одной книги"}


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskUpdate) -> Task:
    """
    Обновить существующую задачу
    task_id получаем из url
    payload получаем из тела запроса
    """
    for task in tasks:
        if task.id == task_id:
            if payload.title is not None:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> None:
    """Удалить задачу"""
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")



class Category(BaseModel):
    id: str
    name: str


class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

categories: list[Category] = []
@app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate):
    new_category = Category(id=str(uuid4()), name=category_data.name)
    categories.append(new_category)
    return new_category

@app.get("/categories", response_model=list[Category])
def get_categories():
    return categories

@app.patch("/categories/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
def update_category(category_id: str, payload: CategoryUpdate):
    for category in categories:
        if category.id == category_id:
            if payload.name is not None:
                category.name = payload.name
            return category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Такой категории нет")

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="категория не найдена")
