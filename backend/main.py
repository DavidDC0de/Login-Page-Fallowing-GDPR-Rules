from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"], #allow backend to talk to frontend
    allow_methods=["*"],
    allow_headers=["*"]
)

#connect SQLAlchemy to SQLite
engine = create_engine("sqlite:///./users.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db(): #starts a new db session every time is called 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#tells sql what type of data is gonna be stored in each column
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True) #unique key for every data 
    email = Column(String, unique=True) #all emails must be unique
    password_hash = Column(String) #stores the hash version of the password
    name = Column(String) 
    gdpr_consent = Column(Boolean) #stores if user agreed to the gdpr rules 
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine) #create the database table 

#Create CryptContext instance
password_context = CryptContext(schemes=["argon2"], deprecated="auto")

#password hashing function
def hash_password(password):
    return password_context.hash(password)

#verify the plain password against the hashed 
def verify_password(plain, hashed):
    return password_context.verify(plain, hashed)

class RegisterIn(BaseModel): #data coming in form the front end 
    email: EmailStr
    password: str
    gdpr_consent: bool

class RegisterOut(BaseModel): #data going back to the front end from the backend 
    message: str
    

@app.post("/register", response_model = RegisterOut)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    #check for GDPR consent
    if not payload.gdpr_consent:
        raise HTTPException(status_code=400, detail="Must accept the GDPR consent to register.")

    #check if user already exists in the db
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email provided is already registered.")

    #hash the raw password
    new_password = hash_password(payload.password)

    #create the new user
    new_user = User(
        email = payload.email,
        password_hash = new_password,
        gdpr_consent = payload.gdpr_consent
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RegisterOut(message="User registered succesfully!")