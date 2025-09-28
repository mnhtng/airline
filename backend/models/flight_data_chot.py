from sqlalchemy import Column, BigInteger, String, Float, DateTime, Integer
from sqlalchemy.sql import func

from backend.db.database import Base


class FlightDataChot(Base):
    """
    Model cho Flight Data Main - Dữ liệu flight đã được xử lý và validation

    Bảng chính cho dữ liệu flight sạch sau validation

    Attributes:
        id: ID duy nhất của bản ghi
        convert_date: Ngày bay ở định dạng YYYYMMDD
        flightno: Số hiệu chuyến bay
        route: Tuyến bay
        actype: Loại máy bay
        totalpax: Tổng số hành khách
        cgo: Khối lượng hàng hóa
        mail: Khối lượng bưu kiện
        acregno: Số đăng ký máy bay
        source: File nguồn
        sheet_name: Sheet nguồn
        region_type: Phân loại khu vực
        seat: Sức chứa ghế
        week_number: Số tuần
        year_number: Năm
        note: Ghi chú
        type_filter: Bộ lọc loại chuyến bay
        inserted_time: Thời gian chèn
        int_dom_: Domestic/International
        created_at: Thời gian tạo bản ghi
        updated_at: Thời gian cập nhật bản ghi
    """

    __tablename__ = "flight_data_chot"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    convert_date = Column(
        BigInteger, nullable=True, index=True, comment="Flight date in YYYYMMDD format"
    )
    flightno = Column(String(50), nullable=True, index=True, comment="Flight number")
    route = Column(String(100), nullable=True, index=True, comment="Route")
    actype = Column(String(50), nullable=True, index=True, comment="Aircraft type")
    totalpax = Column(Float, nullable=True, comment="Total passengers")
    cgo = Column(Float, nullable=True, comment="Cargo weight")
    mail = Column(Float, nullable=True, comment="Mail weight")
    acregno = Column(String(50), nullable=True, comment="Aircraft registration")
    source = Column(String(500), nullable=True, index=True, comment="Source file")
    sheet_name = Column(String(255), nullable=True, index=True, comment="Source sheet")
    region_type = Column(
        Integer, nullable=False, default=0, comment="Region classification"
    )
    seat = Column(BigInteger, nullable=True, comment="Seat capacity")
    week_number = Column(Integer, nullable=True, comment="Week number")
    year_number = Column(Integer, nullable=True, comment="Year")
    note = Column(String(255), nullable=True, comment="Notes")
    type_filter = Column(
        Integer, nullable=True, index=True, comment="Flight type filter"
    )
    inserted_time = Column(
        DateTime, default=func.getdate(), nullable=False, comment="Thời gian chèn"
    )
    int_dom_ = Column(String(10), nullable=True, comment="Domestic/International")
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
        """Represent the FlightDataChot model as a string"""
        return f"<FlightDataChot(flightno='{self.flightno}', route='{self.route}', convert_date={self.convert_date})>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "convert_date": self.convert_date,
            "flightno": self.flightno,
            "route": self.route,
            "actype": self.actype,
            "totalpax": self.totalpax,
            "cgo": self.cgo,
            "mail": self.mail,
            "acregno": self.acregno,
            "source": self.source,
            "sheet_name": self.sheet_name,
            "region_type": self.region_type,
            "seat": self.seat,
            "week_number": self.week_number,
            "year_number": self.year_number,
            "note": self.note,
            "type_filter": self.type_filter,
            "inserted_time": self.inserted_time,
            "int_dom_": self.int_dom_,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
