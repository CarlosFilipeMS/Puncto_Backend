# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Tirar de hardcode a SENHA
DATABASE_URL = "postgresql://postgres.fqyiydpzvsiqbnguhern:fXwpSkDBGIAMa04@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

# Cria engine
engine = create_engine(DATABASE_URL)

# Cria a session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os models
Base = declarative_base()
