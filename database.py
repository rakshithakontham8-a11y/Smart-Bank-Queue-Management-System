from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database
engine = create_engine("sqlite:///bank_queue.db")

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    token = Column(Integer, unique=True)
    name = Column(String)
    phone = Column(String)
    service = Column(String)
    priority = Column(String)
    time = Column(String)
    date = Column(String)
    status = Column(String, default="Waiting")


# Create table
Base.metadata.create_all(engine)


# Add date column to old database if it doesn't exist
with engine.connect() as conn:
    try:
        conn.execute(
            text("ALTER TABLE customers ADD COLUMN date VARCHAR")
        )
        conn.commit()
    except:
        pass


SessionLocal = sessionmaker(bind=engine)