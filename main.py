# main.py
import os
import shutil
import uuid
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import datetime
from sqlalchemy.orm import Session
from jose import JWTError, jwt

# Import all our local modules
import models, schemas, crud, security
from database import SessionLocal, engine
from config import settings

# Create database tables on startup
models.Base.metadata.create_all(bind=engine)

# Create the upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")
# Make current year available to all templates (avoids relying on a missing Jinja2 date filter)
templates.env.globals['current_year'] = datetime.datetime.now().year

# --- Database Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Authentication Dependency ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Try to get token from cookie first (for web requests)
    token = None
    if request.cookies.get("access_token"):
        token = request.cookies.get("access_token").replace("Bearer ", "")

    # If no cookie token, try Authorization header (for API requests)
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# --- API Endpoints ---

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# --- User & Auth Routes ---

@app.post("/create-user/", response_model=schemas.UserRegisterResponse)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user. Generates username and key automatically.
    """
    db_user_email = crud.get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user, key = crud.create_user(db=db, user=user)
    return schemas.UserRegisterResponse(username=new_user.username, email=new_user.email, key=key)

@app.post("/login")
def login_for_access_token(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Web login with username and password - redirects to dashboard on success.
    """
    user = crud.get_user_by_username(db, username=username)

    if not user or not user.is_active or not security.verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Incorrect username or password"
        })

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Create response with redirect to dashboard
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return response

@app.post("/token", response_model=schemas.Token)
def api_login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    API login with username and password - returns JSON token.
    """
    user = crud.get_user_by_username(db, username=form_data.username)

    if not user or not user.is_active or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    """
    A protected route to check if you are logged in.
    """
    return current_user

# --- File Transfer Routes ---

@app.post("/upload/")
def upload_file(
    request: Request,
    file: UploadFile = File(...),
    recipient_username: str = Form(None),
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Upload a file. Requires user to be authenticated.
    Optionally specify recipient_username to send to another user.
    """
    recipient_id = None
    if recipient_username:
        recipient = crud.get_user_by_username(db, username=recipient_username)
        if not recipient:
            raise HTTPException(status_code=404, detail="Recipient not found")
        recipient_id = recipient.id

    # Generate a secure, unique filename for storage
    file_extension = os.path.splitext(file.filename)[1]
    saved_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, saved_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
    finally:
        file.file.close()

    # Create the file metadata record in the database
    crud.create_file_record(
        db=db,
        filename=file.filename,
        saved_filename=saved_filename,
        owner_id=current_user.id,
        recipient_id=recipient_id,
        uploaded_at=datetime.datetime.utcnow()
    )

    # Return JSON response for AJAX requests
    if request.headers.get("accept") == "application/json":
        return {
            "message": "File uploaded successfully",
            "original_filename": file.filename,
            "saved_filename": saved_filename
        }

    # For form submissions, redirect back to dashboard
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/download/{saved_filename}")
def download_file(
    saved_filename: str,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Download a file. Requires user to be authenticated.
    Allows if user is owner or recipient.
    """
    db_file = crud.get_file_by_saved_name(db, saved_filename)

    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    # --- THIS IS THE CRITICAL SECURITY CHECK ---
    if db_file.owner_id != current_user.id and db_file.recipient_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to download this file")

    file_path = os.path.join(settings.UPLOAD_DIR, db_file.saved_filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    # Return the file with its original name
    return FileResponse(file_path, filename=db_file.filename)

# --- New Routes ---

@app.get("/received-files/", response_model=list[schemas.FileInfo])
def get_received_files(current_user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Get list of files sent to the current user.
    """
    return crud.get_files_by_recipient(db, current_user.id)

# --- Web UI Routes ---

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
def register_form(request: Request, email: str = Form(...), db: Session = Depends(get_db)):
    try:
        user_data = schemas.UserCreate(email=email)
        response = create_user_endpoint(user_data, db)
        return templates.TemplateResponse("register.html", {"request": request, "username": response.username, "key": response.key})
    except HTTPException as e:
        return templates.TemplateResponse("register.html", {"request": request, "error": e.detail})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request, current_user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    owned_files = db.query(models.File).filter(models.File.owner_id == current_user.id).order_by(models.File.uploaded_at.desc()).all()
    received_files = crud.get_files_by_recipient(db, current_user.id)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "current_user": current_user,
        "owned_files": owned_files,
        "received_files": received_files
    })

@app.get("/received", response_class=HTMLResponse)
def received_page(request: Request, current_user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    received_files = crud.get_files_by_recipient(db, current_user.id)
    return templates.TemplateResponse("received.html", {"request": request, "current_user": current_user, "received_files": received_files})

# --- Admin Routes ---

def get_current_admin_user(current_user: models.User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard_page(request: Request, current_user: models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    files = crud.get_all_files(db)
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "current_user": current_user, "users": users, "files": files})

@app.get("/admin/users/", response_model=list[schemas.User])
def get_all_users_admin(current_user: models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@app.get("/admin/files/", response_model=list[schemas.FileInfo])
def get_all_files_admin(current_user: models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    return crud.get_all_files(db)

@app.delete("/admin/users/{user_id}")
def delete_user_admin(user_id: int, current_user: models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    if crud.delete_user(db, user_id):
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/admin/files/{file_id}")
def delete_file_admin(file_id: int, current_user: models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    if crud.delete_file(db, file_id):
        return {"message": "File deleted"}
    raise HTTPException(status_code=404, detail="File not found")

# --- Logout Route ---
@app.get("/logout")
def logout(request: Request):
    """
    Logout by clearing the access token cookie and redirecting to home.
    """
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response
