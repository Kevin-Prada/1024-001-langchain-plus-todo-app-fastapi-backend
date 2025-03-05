import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_d5jVEZOqr4nw@ep-plain-mode-a8tq1tu6-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

user = os.environ['DATABASE_USER']
password = os.environ['DATABASE_PASSWORD']
host = os.environ['DATABASE_HOST']
port = os.environ['DATABASE_PORT']
db_name = os.environ['DATABASE_NAME']

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()