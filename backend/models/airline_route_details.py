from sqlalchemy import Column, BigInteger, String, DateTime, Float
from sqlalchemy.sql import func

from backend.db.database import Base


class AirlineRouteDetails(Base):
    """
    Model cho thông tin chi tiết tuyến bay và sector

    Chứa dữ liệu tuyến bay bao gồm khoảng cách, quốc gia và phân loại domestic/international

    Attributes:
        index: ID duy nhất của bản ghi
        sector: Mã sector tuyến bay (VD: SGNHAN)
        distance_mile_gds: Khoảng cách tính bằng dặm từ GDS
        distance_km_gds: Khoảng cách tính bằng km từ GDS
        sector_2: Định dạng sector thay thế
        route: Mô tả tuyến bay
        country_1: Quốc gia điểm khởi hành
        country_2: Quốc gia điểm đến
        country: Quốc gia chính để phân loại tuyến bay
        dom_int: Domestic (DOM) hoặc International (INT)
        area: Khu vực/vùng địa lý
        inserted_time: Thời gian chèn bản ghi
        created_at: Thời gian tạo bản ghi
        updated_at: Thời gian cập nhật bản ghi
    """

    __tablename__ = "Airline_Route_Details"

    index = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    sector = Column(
        "Sector",
        String(20),
        nullable=False,
        index=True,
        comment="Route sector code (e.g., SGNHAN)",
    )
    distance_mile_gds = Column(
        "Distance mile GDS",
        BigInteger,
        nullable=True,
        comment="Distance in miles from GDS",
    )
    distance_km_gds = Column(
        "Distance km GDS",
        Float,
        nullable=True,
        comment="Distance in kilometers from GDS",
    )
    sector_2 = Column(
        "Sector_2", String(20), nullable=True, comment="Alternative sector format"
    )
    route = Column(
        "Route", String(100), nullable=True, index=True, comment="Route description"
    )
    country_1 = Column(
        "Country 1", String(100), nullable=True, comment="Origin country"
    )
    country_2 = Column(
        "Country 2", String(100), nullable=True, comment="Destination country"
    )
    country = Column(
        "Country",
        String(100),
        nullable=True,
        index=True,
        comment="Primary country for route classification",
    )
    dom_int = Column(
        "DOM/INT",
        String(10),
        nullable=True,
        comment="Domestic (DOM) or International (INT)",
    )
    area = Column("Area", String(100), nullable=True, comment="Geographic area/region")
    inserted_time = Column(
        DateTime, default=func.getdate(), nullable=False, comment="Thời gian chèn"
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
        """Represent the AirlineRouteDetails model as a string"""
        return f"<AirlineRouteDetails(sector='{self.sector}', route='{self.route}', country='{self.country}', dom_int='{self.dom_int}')>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "index": self.index,
            "sector": self.sector,
            "distance_mile_gds": self.distance_mile_gds,
            "distance_km_gds": self.distance_km_gds,
            "sector_2": self.sector_2,
            "route": self.route,
            "country_1": self.country_1,
            "country_2": self.country_2,
            "country": self.country,
            "dom_int": self.dom_int,
            "area": self.area,
            "inserted_time": self.inserted_time,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
