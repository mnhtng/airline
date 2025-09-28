from sqlalchemy import Column, BigInteger, String, Float, DateTime, Date, Integer
from sqlalchemy.sql import func

from backend.db.database import Base


class FlightAnalyze(Base):
    """
    Model cho Flight Analysis Table - Dữ liệu flight nâng cao với các tính toán bổ sung

    Chứa dữ liệu flight đã xử lý với phân tích địa lý và vận hành

    Attributes:
        id: ID duy nhất của bản ghi
        flight_date: Ngày bay gốc
        flight_date_format: Ngày bay đã chuẩn hóa
        flight_no: Số hiệu chuyến bay
        actype: Loại máy bay
        sector: Sector tuyến bay
        total_pax: Tổng số hành khách
        cgo: Hàng hóa
        mail: Bưu kiện
        seat: Sức chứa ghế
        departure: Mã sân bay khởi hành
        arrives: Mã sân bay đến
        airlines_name: Tên hãng hàng không
        country: Quốc gia tuyến bay
        dom_int: Domestic/International
        com: Cờ thương mại
        region: Khu vực địa lý
        city_arrives: Thành phố đến
        country_arrives: Quốc gia đến
        city_departure: Thành phố khởi hành
        country_departure: Quốc gia khởi hành
        source: Nguồn dữ liệu
        rnk_sg: Xếp hạng
        created_at: Thời gian tạo bản ghi
        updated_at: Thời gian cập nhật bản ghi
    """

    __tablename__ = "flight_analyze"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    flight_date = Column(
        "FLIGHT_DATE", String(50), nullable=True, comment="Original flight date"
    )
    flight_date_format = Column(
        "FLIGHT_DATE_FORMAT",
        Date,
        nullable=True,
        index=True,
        comment="Standardized flight date",
    )
    flight_no = Column(
        "FLIGHT_NO", String(50), nullable=True, index=True, comment="Flight number"
    )
    actype = Column("ACTYPE", String(50), nullable=True, comment="Aircraft type")
    sector = Column(
        "SECTOR", String(20), nullable=True, index=True, comment="Route sector"
    )
    total_pax = Column("TOTAL_PAX", Float, nullable=True, comment="Total passengers")
    cgo = Column("CGO", Float, nullable=True, comment="Cargo")
    mail = Column("MAIL", Float, nullable=True, comment="Mail")
    seat = Column("SEAT", BigInteger, nullable=True, comment="Seat capacity")
    departure = Column(
        "DEPARTURE", String(10), nullable=True, comment="Departure airport code"
    )
    arrives = Column(
        "ARRIVES", String(10), nullable=True, comment="Arrival airport code"
    )
    airlines_name = Column(
        "AIRLINES NAME", String(255), nullable=True, comment="Airline name"
    )
    country = Column("COUNTRY", String(100), nullable=True, comment="Route country")
    dom_int = Column(
        "DOM/INT", String(10), nullable=True, comment="Domestic/International"
    )
    com = Column(
        "COM",
        String(1),
        nullable=False,
        default="",
        index=True,
        comment="Commercial flag",
    )
    region = Column(
        "REGION", String(100), nullable=True, index=True, comment="Geographic region"
    )
    city_arrives = Column(
        "CITY_ARRIVES", String(100), nullable=True, comment="Arrival city"
    )
    country_arrives = Column(
        "COUNTRY_ARRIVES", String(100), nullable=True, comment="Arrival country"
    )
    city_departure = Column(
        "CITY_DEPARTURE", String(100), nullable=True, comment="Departure city"
    )
    country_departure = Column(
        "COUNTRY_DEPARTURE", String(100), nullable=True, comment="Departure country"
    )
    source = Column(String(500), nullable=True, comment="Data source")
    rnk_sg = Column(Integer, nullable=False, default=0, comment="Ranking")
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
        """Represent the FlightAnalyze model as a string"""
        return f"<FlightAnalyze(flight_no='{self.flight_no}', sector='{self.sector}', flight_date_format={self.flight_date_format})>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "flight_date": self.flight_date,
            "flight_date_format": (
                self.flight_date_format.isoformat() if self.flight_date_format else None
            ),
            "flight_no": self.flight_no,
            "actype": self.actype,
            "sector": self.sector,
            "total_pax": self.total_pax,
            "cgo": self.cgo,
            "mail": self.mail,
            "seat": self.seat,
            "departure": self.departure,
            "arrives": self.arrives,
            "airlines_name": self.airlines_name,
            "country": self.country,
            "dom_int": self.dom_int,
            "com": self.com,
            "region": self.region,
            "city_arrives": self.city_arrives,
            "country_arrives": self.country_arrives,
            "city_departure": self.city_departure,
            "country_departure": self.country_departure,
            "source": self.source,
            "rnk_sg": self.rnk_sg,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
