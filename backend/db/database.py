from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from backend.core.config import settings


engine = create_engine(settings.DATABASE_URL)  # Tạo engine kết nối CSDL

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # Tạo session để tương tác với CSDL

Base = declarative_base()  # Lớp cha mẹ (superclass) của tất cả các entity models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(
        bind=engine
    )  # Tạo tất cả các bảng trong CSDL nếu chưa tồn tại
