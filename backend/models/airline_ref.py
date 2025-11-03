from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from backend.db.database import Base


class AirlineRef(Base):
    """
    Model cho thông tin hãng hàng không

    Ánh xạ các hãng hàng không với quốc gia và tên đầy đủ

    Attributes:
        id: ID duy nhất của bản ghi
        carrier: Mã hãng 2 ký tự (VD: SF, DT)
        airline_nation: Quốc gia của hãng hàng không
        airlines_name: Tên đầy đủ của hãng hàng không
        created_at: Thời gian tạo bản ghi
        updated_at: Thời gian cập nhật bản ghi
    """

    __tablename__ = "Airline_Ref"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    carrier = Column(
        "CARRIER", String(50), nullable=True, comment="2-letter airline code"
    )
    airline_nation = Column(
        "Airline_Nation", String(255), nullable=True, comment="Country of airline"
    )
    airlines_name = Column(
        "Airlines_Name", String(255), nullable=True, comment="Full airline name"
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
        """Represent the AirlineRef model as a string"""
        return f"<AirlineRef(carrier='{self.carrier}', airline_nation='{self.airline_nation}', airlines_name='{self.airlines_name}')>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "carrier": self.carrier,
            "airline_nation": self.airline_nation,
            "airlines_name": self.airlines_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
