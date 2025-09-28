from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func

from backend.db.database import Base


class TempActypeImport(Base):
    """
    Model cho Temporary Aircraft Type Import - Cho bulk importing aircraft data

    Được sử dụng khi import dữ liệu aircraft type và cấu hình ghế

    Attributes:
        actype: Mã loại máy bay
        seat: Sức chứa ghế
        created_at: Thời gian tạo bản ghi
    """

    __tablename__ = "TempActypeImport"

    actype = Column(
        "Actype", String(255), primary_key=True, comment="Aircraft type code"
    )
    seat = Column("Seat", Integer, nullable=True, comment="Seat capacity")
    created_at = Column(
        DateTime, default=func.sysdatetime(), nullable=False, comment="Thời gian tạo"
    )

    def __repr__(self):
        """Represent the TempActypeImport model as a string"""
        return f"<TempActypeImport(actype='{self.actype}', seat={self.seat})>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "actype": self.actype,
            "seat": self.seat,
            "created_at": self.created_at,
        }
