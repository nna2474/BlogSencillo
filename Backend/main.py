from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
import uuid
from bson import ObjectId

app = FastAPI()

# Habilitar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory="media"), name="media")

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://admin:pass@mongo:27017")
client = MongoClient(MONGO_URL)
db = client.blog_db
posts_collection = db.posts
users_collection = db.users

SECRET_KEY = "LNv6m2mw8EkujV9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Post(BaseModel):
    title: str
    content: str

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Hashear/verificar contraseñas
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        db_user = users_collection.find_one({"username": username})

        if not db_user:
            raise HTTPException(status_code=401, detail="Usuario no válido")
        
        return db_user
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/me")
def read_users_me(user=Depends(get_current_user)):
    return {"usuario": user["username"]}

@app.post("/register")
def register(user: User):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Usuario ya registrado")
    
    hashed = get_password_hash(user.password)
    users_collection.insert_one({
        "username": user.username,
        "hashed_password": hashed
    })

    return {"msg": "Usuario creado exitosamente"}

@app.post("/login", response_model=Token)
def login(user: User):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(days=1))
    return {"access_token": token, "token_type": "bearer"}

@app.get("/posts")
def get_posts():
    posts = list(posts_collection.find())
    result = []
    for p in posts:
        p["_id"] = str(p["_id"])  # Convertir ObjectId a string
        result.append(p)

    return result

@app.get("/posts/{post_id}")
def get_post(post_id: str):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    post["_id"] = str(post["_id"])  # Convertir ObjectId a string
    return post

@app.post("/posts")
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),
    user=Depends(get_current_user)
):
    image_url = None

    if image:
        ext = os.path.splitext(image.filename)[1]
        image_name = f"{uuid.uuid4()}{ext}"
        image_path = os.path.join("media", image_name)

        with open(image_path, "wb") as f:
            f.write(image.file.read())

        image_url = f"http://localhost:8000/media/{image_name}"

    new_post = {
        "title": title,
        "content": content,
        "image_url": image_url,
        "author": user["username"],
        "created_at": datetime.now().isoformat()
    }
    result = posts_collection.insert_one(new_post)
    new_post["_id"] = str(result.inserted_id)
    return new_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: str, user=Depends(get_current_user)):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    if post["author"] != user["username"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este post")
    posts_collection.delete_one({"_id": ObjectId(post_id)})
    return {"msg": "Post eliminado"}
