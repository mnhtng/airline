from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func

from backend.db.database import Base


class SeatByACType(Base):
    """
    Model cho thông tin đăng ký máy bay và cấu hình ghế cá nhân

    Chi tiết đăng ký máy bay cá nhân và cấu hình ghế

    Attributes:
        id: ID duy nhất của bản ghi
        ac_reg_no: Số đăng ký máy bay
        brand: Nhà sản xuất máy bay
        ac_type: Loại máy bay
        seat: Số ghế thực tế của máy bay này
        created_at: Thời gian tạo bản ghi
        updated_at: Thời gian cập nhật bản ghi
    """

    __tablename__ = "seat_by_AC_type"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    ac_reg_no = Column(
        "ACRegNo",
        String(20),
        nullable=False,
        index=True,
        comment="Aircraft registration number",
    )
    brand = Column("Brand", String(50), nullable=True, comment="Aircraft manufacturer")
    ac_type = Column(
        "AC_Type", String(50), nullable=True, index=True, comment="Aircraft type"
    )
    seat = Column(
        "Seat", BigInteger, nullable=True, comment="Actual seat count for this aircraft"
    )
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
        """Represent the SeatByACType model as a string"""
        return f"<SeatByACType(ac_reg_no='{self.ac_reg_no}', ac_type='{self.ac_type}', seat={self.seat})>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "ac_reg_no": self.ac_reg_no,
            "brand": self.brand,
            "ac_type": self.ac_type,
            "seat": self.seat,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
