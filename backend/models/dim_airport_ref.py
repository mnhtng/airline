from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from backend.db.database import Base


class DimAirportRef(Base):
    """
    Model cho thông tin sân bay

    Chứa thông tin IATA codes, tên, thành phố và quốc gia của các sân bay trên thế giới

    Attributes:
        id: ID duy nhất của bản ghi
        iata_code: Mã IATA 3 ký tự của sân bay
        airport_name: Tên đầy đủ của sân bay
        city: Thành phố nơi sân bay được đặt
        country: Quốc gia nơi sân bay được đặt
        created_at: Thời gian tạo bản ghi
        updated_at: Thời gian cập nhật bản ghi
    """

    __tablename__ = "Dim_Airport_Ref"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    iata_code = Column(
        "IATACode", String(10), nullable=True, comment="3-letter IATA airport code"
    )
    airport_name = Column(
        "Airport_Name", String(200), nullable=True, comment="Full airport name"
    )
    city = Column(
        "City", String(100), nullable=True, comment="City where airport is located"
    )
    country = Column(
        "Country",
        String(100),
        nullable=True,
        comment="Country where airport is located",
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
        """Represent the DimAirportRef model as a string"""
        return f"<DimAirportRef(iata_code='{self.iata_code}', airport_name='{self.airport_name}', city='{self.city}', country='{self.country}')>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "iata_code": self.iata_code,
            "airport_name": self.airport_name,
            "city": self.city,
            "country": self.country,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
