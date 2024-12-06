from fastapi import FastAPI, Depends, Form, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import models, schemas
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Configuración de Jinja2 para manejar las plantillas
templates = Jinja2Templates(directory="templates")

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para eliminar un usuario (usando DELETE)
@app.delete("/users/{user_id}/delete", response_class=HTMLResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    # Redirigir a la página principal después de eliminar
    return RedirectResponse(url="/", status_code=303)

# Lista de usuarios obtenidos de la base de datos
@app.get("/users/", response_class=HTMLResponse)
def get_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return templates.TemplateResponse("form.html", {"request": request, "users": users})

# Crear un nuevo usuario
@app.post("/users/", response_class=HTMLResponse)
def create_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    age: int = Form(...),
    db: Session = Depends(get_db),
):
    # Verificar si el correo ya está en uso
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        users = db.query(models.User).all()  # Obtengo la lista de usuarios
        return templates.TemplateResponse(
            "form.html",
            {
                "request": request,
                "error": "El correo electrónico ya está en uso, por favor usa otro.",
                "users": users,  # Paso la lista de usuarios
            },
        )
    
    if age < 0:
        users = db.query(models.User).all()  # Obtengo la lista de usuarios
        return templates.TemplateResponse(
            "form.html",
            {"request": request, "error": "Age cannot be negative.", "users": users},
        )
    if not name.replace(" ", "").isalpha():
        users = db.query(models.User).all()  # Obtengo la lista de usuarios
        return templates.TemplateResponse(
            "form.html",
            {"request": request, "error": "El nombre solo acepta valores de texto.", "users": users},
        )
    
    # Crear el nuevo usuario
    user = models.User(name=name, email=email, age=age)
    db.add(user)
    db.commit()
    db.refresh(user)
    users = db.query(models.User).all()  # Obtengo la lista de usuarios
    return templates.TemplateResponse(
        "form.html",
        {
            "request": request,
            "message": "Usuario creado exitosamente!",
            "users": users,  # Paso la lista de usuarios
        },
    )

# Ruta principal para cargar el formulario
@app.get("/", response_class=HTMLResponse)
def read_form(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return templates.TemplateResponse("form.html", {"request": request, "users": users})





