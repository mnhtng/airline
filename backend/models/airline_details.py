from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func

from backend.db.database import Base


class AirlineDetails(Base):
    """
    Model cho thông tin các hãng hàng không

    Chứa mã hãng, tên và thông tin liên quan của các hãng hàng không

    Attributes:
        index: ID duy nhất của bản ghi
        carrier: Mã hãng 2 ký tự (VD: VN, VJ)
        qg: Mã quốc gia của hãng hàng không
        airlines_name: Tên đầy đủ của hãng hàng không
        created_at: Thời gian tạo bản ghi
        updated_at: Thời gian cập nhật bản ghi
    """

    __tablename__ = "Airline_Details"

    index = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    carrier = Column(
        "CARRIER",
        String(10),
        nullable=False,
        index=True,
        comment="2-letter airline code (e.g., VN, VJ)",
    )
    qg = Column("QG", String(10), nullable=True, comment="Country code for airline")
    airlines_name = Column(
        "Airlines name", String(255), nullable=True, comment="Full airline name"
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
        """Represent the AirlineDetails model as a string"""
        return f"<AirlineDetails(carrier='{self.carrier}', airlines_name='{self.airlines_name}')>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "index": self.index,
            "carrier": self.carrier,
            "qg": self.qg,
            "airlines_name": self.airlines_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
