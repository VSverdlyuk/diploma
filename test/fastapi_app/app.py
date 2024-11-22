# fastapi_app/app.py
from fastapi import FastAPI
import time
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Настройка базы данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./records.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Модель для записи
class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Создание таблицы
Base.metadata.create_all(bind=engine)

@app.post("/write")
def write():
    start_time = time.time()
    
    # Получаем сессию для работы с базой данных
    db = SessionLocal()
    
    # Добавляем 100 записей в базу данных
    for i in range(10000):
        record = Record(name=f"Record {i + 1}")
        db.add(record)
    
    db.commit()  # Подтверждаем транзакцию
    db.close()   # Закрываем сессию
    
    end_time = time.time()
    return {"message": f"FastAPI write of 100 records took {end_time - start_time} seconds"}

