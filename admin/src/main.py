from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from .crud import get_users, create_user, update_user, delete_user
from .models import SessionLocal
from .schemas import UserCreate, UserUpdate
from passlib.context import CryptContext

app = FastAPI(title="Admin Panel for Bot Users")
templates = Jinja2Templates(directory="templates")  # Путь относительно /code/ в контейнере

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
ADMIN_PASSWORD = pwd_context.hash("adminpass")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, password: str = Form(...)):
    if pwd_context.verify(password, ADMIN_PASSWORD):
        response = RedirectResponse(url="/users", status_code=303)  # Явный GET-редирект
        response.set_cookie(key="admin_session", value="true")
        return response
    raise HTTPException(status_code=401, detail="Invalid password")

@app.get("/users", response_class=HTMLResponse)
async def list_users(request: Request, db: Session = Depends(get_db)):
    if not request.cookies.get("admin_session"):
        raise HTTPException(status_code=401, detail="Not authenticated")
    users = get_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})  # /code/templates/users.html

@app.post("/users")
async def add_user(user_id: int = Form(...), username: str = Form(...), db: Session = Depends(get_db)):
    create_user(db, user_id, username)
    return RedirectResponse(url="/users", status_code=303)

@app.post("/users/{user_id}")
async def edit_user(user_id: int, username: str = Form(...), db: Session = Depends(get_db)):
    updated = update_user(db, user_id, username)
    if not updated:
        raise HTTPException(status_code=404)
    return RedirectResponse(url="/users", status_code=303)

@app.post("/delete/{user_id}")
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    deleted = delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404)
    return RedirectResponse(url="/users", status_code=303)

 

if __name__ == "__main__":
    import uvicorn
    print(pwd_context.hash("adminpass"))
    uvicorn.run(app, host="0.0.0.0", port=8080)