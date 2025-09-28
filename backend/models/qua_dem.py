from sqlalchemy import Column, BigInteger, String, DateTime, Date
from sqlalchemy.sql import func

from backend.db.database import Base


class QuaDem(Base):
    """
    Model cho Overnight Flights - Theo dõi đặc biệt cho các chuyến bay qua đêm

    Theo dõi các chuyến bay cần nghỉ qua đêm hoặc nối chuyến

    Attributes:
        id: ID duy nhất của bản ghi
        flight_date_format: Ngày chuyến bay đầu tiên
        source: Sân bay nguồn
        sortedroute: Tuyến bay đã chuẩn hóa
        flight_no: Số hiệu chuyến bay
        flight_date_format_: Ngày chuyến bay thứ hai
        source_: Sân bay đích
        sortedroute_: Tuyến bay về
        flight_no_: Số hiệu chuyến bay về
        created_at: Thời gian tạo bản ghi
    """

    __tablename__ = "qua_dem"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    flight_date_format = Column(
        Date, nullable=True, index=True, comment="First flight date"
    )
    source = Column(String(500), nullable=True, comment="Source airport")
    sortedroute = Column(String(20), nullable=True, comment="Standardized route")
    flight_no = Column(String(50), nullable=True, index=True, comment="Flight number")
    flight_date_format_ = Column(Date, nullable=True, comment="Second flight date")
    source_ = Column(String(500), nullable=True, comment="Destination airport")
    sortedroute_ = Column(String(20), nullable=True, comment="Return route")
    flight_no_ = Column(String(50), nullable=True, comment="Return flight number")
    created_at = Column(
        DateTime, default=func.sysdatetime(), nullable=False, comment="Thời gian tạo"
    )

    def __repr__(self):
        """Represent the QuaDem model as a string"""
        return f"<QuaDem(flight_no='{self.flight_no}', sortedroute='{self.sortedroute}', flight_date_format={self.flight_date_format})>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "flight_date_format": (
                self.flight_date_format.isoformat() if self.flight_date_format else None
            ),
            "source": self.source,
            "sortedroute": self.sortedroute,
            "flight_no": self.flight_no,
            "flight_date_format_": (
                self.flight_date_format_.isoformat()
                if self.flight_date_format_
                else None
            ),
            "source_": self.source_,
            "sortedroute_": self.sortedroute_,
            "flight_no_": self.flight_no_,
            "created_at": self.created_at,
        }
