from fastapi import FastAPI
import time
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./records.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Model for a record
class Record(Base):
    """
    Represents a record in the database.

    Attributes:
        id (int): The primary key for the record.
        name (str): The name of the record.
    """
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Create the table
Base.metadata.create_all(bind=engine)

@app.post("/write")
def write():
    """
    Inserts 10,000 records into the database.

    Measures the time taken to add the records to the SQLite database and returns it.

    Returns:
        dict: A message containing the time taken to write records.
    """
    start_time = time.time()  # Start timing the operation

    # Get a session for interacting with the database
    db = SessionLocal()

    try:
        # Add 10,000 records to the database
        for i in range(10000):
            record = Record(name=f"Record {i + 1}")
            db.add(record)

        db.commit()  # Commit the transaction
    finally:
        db.close()  # Ensure the session is closed

    end_time = time.time()  # End timing the operation

    # Return the time taken for the operation
    return {"message": f"FastAPI write of 10,000 records took {end_time - start_time:.2f} seconds"}
