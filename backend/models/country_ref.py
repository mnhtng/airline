from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from backend.db.database import Base


class CountryRef(Base):
    """
    Model cho thông tin quốc gia

    Ánh xạ các quốc gia với khu vực địa lý tương ứng cho mục đích báo cáo

    Attributes:
        id: ID duy nhất của bản ghi
        country: Tên quốc gia
        region: Khu vực
        region_vnm: Khu vực tiếng Việt
        two_letter_code: Mã 2 ký tự
        three_letter_code: Mã 3 ký tự
        created_at: Thời gian tạo bản ghi
        updated_at: Thời gian cập nhật bản ghi
    """

    __tablename__ = "Country_Ref"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    country = Column("Country", String(255), nullable=True, comment="Country name")
    region = Column("Region", String(255), nullable=True, comment="Region name")
    region_vnm = Column(
        "Region_(VNM)",
        String(255),
        nullable=True,
        comment="Region name in Vietnamese",
    )
    two_letter_code = Column(
        "2_Letter_Code", String(2), nullable=True, comment="2-letter code"
    )
    three_letter_code = Column(
        "3_Letter_Code", String(3), nullable=True, comment="3-letter code"
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
        """Represent the CountryRef model as a string"""
        return f"<CountryRef(country='{self.country}', region='{self.region}')>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "country": self.country,
            "region": self.region,
            "region_vnm": self.region_vnm,
            "two_letter_code": self.two_letter_code,
            "three_letter_code": self.three_letter_code,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
