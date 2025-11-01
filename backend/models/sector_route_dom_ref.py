from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from backend.db.database import Base


class SectorRouteDomRef(Base):
    """
    Model cho thông tin phân loại tuyến bay

    Chứa thông tin phân loại đường bay theo sector, khu vực/vùng địa lý level 1 và Domestic (DOM) hoặc International (INT)

    Attributes:
        id: ID duy nhất của bản ghi
        sector: Mã sector tuyến bay
        area_lv1: Khu vực/vùng địa lý level 1
        dom_int: Domestic (DOM) hoặc International (INT)
        created_at: Thời gian tạo bản ghi
        updated_at: Thời gian cập nhật bản ghi
    """

    __tablename__ = "Sector_Route_DOM_Ref"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    sector = Column("Sector", String(20), nullable=False, comment="Route sector code")
    area_lv1 = Column(
        "Area_Lv1",
        String(100),
        nullable=False,
        comment="Geographic area/region level 1 (e.g., Asia, Europe, etc.)",
    )
    dom_int = Column(
        "DOM/INT",
        String(10),
        nullable=False,
        comment="Domestic (DOM) or International (INT)",
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
        """Represent the SectorRouteDomRef model as a string"""
        return f"<SectorRouteDomRef(sector='{self.sector}', area_lv1='{self.area_lv1}', dom_int='{self.dom_int}')>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "sector": self.sector,
            "area_lv1": self.area_lv1,
            "dom_int": self.dom_int,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
