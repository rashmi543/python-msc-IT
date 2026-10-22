
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from database import engine, Base, get_db
from models import User, Task

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="change-this-to-a-long-random-secret",
    same_site="lax",
    https_only=False
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


# Get currently logged-in user
def current_user(request: Request, db: Session):
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    return db.query(User).filter(
        User.id == user_id
    ).first()


# Get task only if it belongs to the logged-in user
def get_owned_task(task_id: int, user: User, db: Session):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.created_by == user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# Home page
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    tasks = db.query(Task).filter(
        Task.created_by == user.id
    ).order_by(Task.id.desc()).all()

    pending_tasks = [
        task for task in tasks
        if not task.is_completed
    ]

    completed_tasks = [
        task for task in tasks
        if task.is_completed
    ]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "user": user,
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks,
            "theme": request.cookies.get("theme", "light")
        }
    )


# Login page
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)

    if user:
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
            "error": None
        }
    )


# Login user
@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    username = username.strip()

    user = db.query(User).filter(
        User.username == username
    ).first()

    if user and check_password_hash(
        user.password_hash, password
    ):
        request.session.clear()
        request.session["user_id"] = user.id

        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
            "error": "Invalid username or password"
        },
        status_code=401
    )


# Register user
@app.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    username = username.strip()

    if not username or not password:
        raise HTTPException(
            status_code=400,
            detail="Username and password are required"
        )

    existing_user = db.query(User).filter(
        User.username == username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    user = User(
        username=username,
        password_hash=generate_password_hash(password)
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    return RedirectResponse("/login", status_code=303)


# Add task
@app.post("/add")
def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    db: Session = Depends(get_db)
):
    user = current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    title = title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    if priority not in ["High", "Medium", "Low"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid priority"
        )

    task = Task(
        title=title,
        description=description.strip(),
        priority=priority,
        is_completed=False,
        created_by=user.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return RedirectResponse("/", status_code=303)


# Mark task completed or pending
@app.get("/toggle/{task_id}")
def toggle_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    task = get_owned_task(task_id, user, db)

    task.is_completed = not task.is_completed

    db.commit()

    return RedirectResponse("/", status_code=303)


# Edit task page
@app.get("/edit/{task_id}", response_class=HTMLResponse)
def edit_page(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    task = get_owned_task(task_id, user, db)

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={
            "request": request,
            "user": user,
            "task": task
        }
    )


# Update task
@app.post("/update/{task_id}")
def update_task(
    task_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    db: Session = Depends(get_db)
):
    user = current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    title = title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    if priority not in ["High", "Medium", "Low"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid priority"
        )

    task = get_owned_task(task_id, user, db)

    task.title = title
    task.description = description.strip()
    task.priority = priority

    db.commit()

    return RedirectResponse("/", status_code=303)


# Delete task
@app.post("/delete/{task_id}")
def delete_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    task = get_owned_task(task_id, user, db)

    db.delete(task)
    db.commit()

    return RedirectResponse("/", status_code=303)


# Change theme using cookie
@app.get("/set-theme/{theme}")
def set_theme(theme: str, request: Request):
    if theme not in ["light", "dark"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid theme"
        )

    if not request.session.get("user_id"):
        return RedirectResponse("/login", status_code=303)

    response = RedirectResponse("/", status_code=303)

    response.set_cookie(
        key="theme",
        value=theme,
        httponly=True,
        samesite="lax"
    )

    return response


# Logout
@app.get("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse("/login", status_code=303)
