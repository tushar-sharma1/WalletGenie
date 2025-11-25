from sqlalchemy import create_engine, Column, Integer, String, Float, Date, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import SQL_CONNECTION
import os

# Cloud Run connects to Cloud SQL via Unix socket
# Format for SQL_CONNECTION: project:region:instance or postgresql://user:pass@/dbname?host=/cloudsql/instance
DATABASE_URL = "sqlite:///./test.db"
engine = None

if os.getenv("SQL_CONNECTION") and ":" in os.getenv("SQL_CONNECTION"):
    # Cloud SQL via Unix socket (used in Cloud Run)
    instance_connection_name = os.getenv("SQL_CONNECTION")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "password")
    db_name = os.getenv("DB_NAME", "walletgenie")
    
    # Cloud Run provides access via Unix socket
    unix_socket_path = f"/cloudsql/{instance_connection_name}"
    
    DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}?host={unix_socket_path}"
    print(f"Connecting to Cloud SQL via Unix socket: {unix_socket_path}")
    engine = create_engine(DATABASE_URL)
else:
    # Local SQLite
    print("Using local SQLite")
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, default="user_1") # Hackathon: single user or hardcoded
    date = Column(String) # Keeping as string for simplicity in hackathon, or Date if parsed correctly
    description = Column(String)
    amount = Column(Float)
    type = Column(String)
    source = Column(String)
    category = Column(String)
    merchant_normalized = Column(String, nullable=True)

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, default="user_1")
    target_amount = Column(Float)
    months = Column(Integer)
    created_at = Column(String) # Timestamp as string

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
