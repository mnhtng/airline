from sqlalchemy import Column, String, Integer, Numeric, DateTime
from sqlalchemy.sql import func

from backend.db.database import Base


class TempRouteImport(Base):
    """
    Model cho Temporary Route Import - Cho bulk importing route data

    Được sử dụng khi import dữ liệu route và thời gian bay

    Attributes:
        route: Mã tuyến bay
        ac: Loại máy bay
        route_id: Định danh tuyến bay
        fh_theo_gio: Giờ bay
        flight_hour: Thời gian bay
        taxi: Thời gian taxi
        block_hour: Thời gian block
        distance_km: Khoảng cách tính km
        loai: Loại tuyến bay (Tiếng Việt)
        type: Loại tuyến bay (Tiếng Anh)
        country: Phân loại quốc gia
        created_at: Thời gian tạo bản ghi
    """

    __tablename__ = "TempRouteImport"

    route = Column("Route", String(255), primary_key=True, comment="Route code")
    ac = Column("AC", String(50), nullable=True, comment="Aircraft type")
    route_id = Column("Route_ID", String(50), nullable=True, comment="Route identifier")
    fh_theo_gio = Column(
        "FH (THEO GIỜ)", Numeric(10, 2), nullable=True, comment="Flight hours"
    )
    flight_hour = Column(
        "FLIGHT HOUR", Numeric(10, 2), nullable=True, comment="Flight duration"
    )
    taxi = Column("TAXI", Numeric(10, 2), nullable=True, comment="Taxi time")
    block_hour = Column(
        "BLOCK HOUR", Numeric(10, 2), nullable=True, comment="Block time"
    )
    distance_km = Column(
        "DISTANCE KM", Integer, nullable=True, comment="Distance in kilometers"
    )
    loai = Column("Loại", String(50), nullable=True, comment="Route type (Vietnamese)")
    type = Column("Type", String(50), nullable=True, comment="Route type (English)")
    country = Column(
        "Country", String(100), nullable=True, comment="Country classification"
    )
    created_at = Column(
        DateTime, default=func.sysdatetime(), nullable=False, comment="Thời gian tạo"
    )

    def __repr__(self):
        """Represent the TempRouteImport model as a string"""
        return f"<TempRouteImport(route='{self.route}', ac='{self.ac}', country='{self.country}')>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "route": self.route,
            "ac": self.ac,
            "route_id": self.route_id,
            "fh_theo_gio": float(self.fh_theo_gio) if self.fh_theo_gio else None,
            "flight_hour": float(self.flight_hour) if self.flight_hour else None,
            "taxi": float(self.taxi) if self.taxi else None,
            "block_hour": float(self.block_hour) if self.block_hour else None,
            "distance_km": self.distance_km,
            "loai": self.loai,
            "type": self.type,
            "country": self.country,
            "created_at": self.created_at,
        }
