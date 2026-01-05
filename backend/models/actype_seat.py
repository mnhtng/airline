from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func

from backend.db.database import Base


class ActypeSeat(Base):
    """
    Model cho cấu hình ghế theo loại máy bay

    Ánh xạ các loại máy bay với sức chứa ghế tiêu chuẩn

    Attributes:
        index: ID duy nhất của bản ghi
        actype: Mã loại máy bay (VD: A320, B777)
        seat: Sức chứa ghế tiêu chuẩn
        created_at: Thời gian tạo bản ghi
        updated_at: Thời gian cập nhật bản ghi
    """

    __tablename__ = "actype_seat"
    __table_args__ = {"implicit_returning": False}

    index = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    actype = Column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
        comment="Aircraft type code (e.g., A320, B777)",
    )
    seat = Column(BigInteger, nullable=False, comment="Standard seat capacity")
    created_at = Column(
        DateTime, default=func.sysdatetime(), nullable=False, comment="Thời gian tạo"
    )
    updated_at = Column(
        DateTime,
        default=func.sysdatetime(),
        onupdate=func.sysdatetime(),
        nullable=False,
        comment="Thời gian cập nhật",
    )

    def __repr__(self):
        """Represent the ActypeSeat model as a string"""
        return f"<ActypeSeat(actype='{self.actype}', seat={self.seat})>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "index": self.index,
            "actype": self.actype,
            "seat": self.seat,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
