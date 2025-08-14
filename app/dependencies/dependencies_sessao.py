from sqlalchemy.orm import sessionmaker
from app.database import engine

SessionLocal = sessionmaker(bind=engine)

def pegar_sessao():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

