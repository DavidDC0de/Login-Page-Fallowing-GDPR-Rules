app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], #allow backend to talk to frontend
    allow_methods=["*"],
    allow_headers=["*"]
)

#connect SQLAlchemy to SQLite
engine = create_engine("sqlite:///./users.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#tells sql what type of data is gonna be stored in each column
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True) #unique key for every data 
    email = Column(String, unique=True) #all emails must be unique
    password_hash = Column(String) #stores the hash version of the password
    name = Column(String) 
    gdpr_consent = Column(Boolean) #stores if user agreed to the gdpr rules 
    created_at = Column(DateTime, default=datetime.utcnow)


