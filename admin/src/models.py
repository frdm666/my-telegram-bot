from sqlalchemy import Column, BigInteger, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class AllowedUser(Base):
    __tablename__ = "allowed_users"
    user_id = Column(BigInteger, primary_key=True)
    username = Column(String(255))

engine = create_engine("postgresql://botuser:botpass@db:5432/botdb")  # Путь к БД через Docker-сеть
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)