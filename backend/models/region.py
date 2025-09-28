from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func

from backend.db.database import Base


class Region(Base):
    """
    Model cho thông tin khu vực địa lý của các quốc gia

    Ánh xạ các quốc gia với khu vực địa lý tương ứng cho mục đích báo cáo

    Attributes:
        index: ID duy nhất của bản ghi
        country: Tên quốc gia
        region: Khu vực địa lý
        created_at: Thời gian tạo bản ghi
        updated_at: Thời gian cập nhật bản ghi
    """

    __tablename__ = "Region"

    index = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    country = Column(
        "Country", String(100), nullable=False, index=True, comment="Country name"
    )
    region = Column(
        "Region", String(100), nullable=False, index=True, comment="Geographic region"
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
        """Represent the Region model as a string"""
        return f"<Region(country='{self.country}', region='{self.region}')>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "index": self.index,
            "country": self.country,
            "region": self.region,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
