from sqlalchemy import Column, BigInteger, String, DateTime, Float, Time
from sqlalchemy.sql import func

from backend.db.database import Base


class Route(Base):
    """
    Model cho thông tin chi tiết tuyến bay bao gồm thời gian bay và khoảng cách

    Cơ sở dữ liệu tuyến bay hoàn chỉnh với các chi tiết vận hành

    Attributes:
        index: ID duy nhất của bản ghi
        route: Mã tuyến bay
        ac: Loại máy bay cho tuyến bay
        route_id: Định danh tuyến bay duy nhất
        fh_theo_gio: Thời gian bay (định dạng time)
        flight_hour: Thời gian bay (số thập phân)
        taxi: Thời gian taxi tính bằng giờ
        block_hour: Tổng thời gian block
        distance_km: Khoảng cách tính bằng kilomet
        loai: Loại tuyến bay tiếng Việt
        type: Loại tuyến bay tiếng Anh
        country: Phân loại quốc gia
        created_at: Thời gian tạo bản ghi
        updated_at: Thời gian cập nhật bản ghi
    """

    __tablename__ = "Route"

    index = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    route = Column(
        "ROUTE", String(20), nullable=False, index=True, comment="Route code"
    )
    ac = Column("AC", String(20), nullable=True, comment="Aircraft type for route")
    route_id = Column(
        "Route_ID", String(50), nullable=True, comment="Unique route identifier"
    )
    fh_theo_gio = Column(
        "FH (THEO GIỜ)", Time, nullable=True, comment="Flight hours (time format)"
    )
    flight_hour = Column(
        "FLIGHT HOUR", Float, nullable=True, comment="Flight hours (decimal)"
    )
    taxi = Column("TAXI", Float, nullable=True, comment="Taxi time in hours")
    block_hour = Column("BLOCK HOUR", Float, nullable=True, comment="Total block time")
    distance_km = Column(
        "DISTANCE KM", Float, nullable=True, comment="Distance in kilometers"
    )
    loai = Column("Loại", String(50), nullable=True, comment="Route type in Vietnamese")
    type = Column("Type", String(50), nullable=True, comment="Route type in English")
    country = Column(
        "Country",
        String(100),
        nullable=True,
        index=True,
        comment="Country classification",
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
        """Represent the Route model as a string"""
        return (
            f"<Route(route='{self.route}', ac='{self.ac}', country='{self.country}')>"
        )

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "index": self.index,
            "route": self.route,
            "ac": self.ac,
            "route_id": self.route_id,
            "fh_theo_gio": self.fh_theo_gio.isoformat() if self.fh_theo_gio else None,
            "flight_hour": self.flight_hour,
            "taxi": self.taxi,
            "block_hour": self.block_hour,
            "distance_km": self.distance_km,
            "loai": self.loai,
            "type": self.type,
            "country": self.country,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
