from sqlalchemy import Column, BigInteger, String, Float, Integer, DateTime, Text
from sqlalchemy.sql import func

from backend.db.database import Base


class ErrorTable(Base):
    """
    Model cho Error Table - Lưu trữ records thất bại validation

    Chứa dữ liệu flight không thể xử lý được do các lỗi validation

    Attributes:
        id: ID duy nhất của bản ghi
        flightdate: Ngày bay gốc
        flightno: Số hiệu chuyến bay
        route: Tuyến bay
        actype: Loại máy bay
        seat: Sức chứa ghế
        adl: Số hành khách người lớn
        chd: Số hành khách trẻ em
        cgo: Hàng hóa
        mail: Bưu kiện
        source: File nguồn
        acregno: Số đăng ký máy bay
        sheet_name: Tên sheet
        totalpax: Tổng số hành khách
        int_dom: Domestic/International
        is_invalid_flight_date: Cờ validation ngày bay
        is_invalid_passenger_cargo: Cờ validation hành khách/hàng hóa
        is_invalid_route: Cờ validation tuyến bay
        is_invalid_actype_seat: Cờ validation loại máy bay
        error_reason: Mô tả lỗi
        total_errors: Tổng số lỗi
        time_import: Thời gian import
        created_at: Thời gian tạo bản ghi
    """

    __tablename__ = "error_table"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    flightdate = Column(String(255), nullable=True, comment="Original flight date")
    flightno = Column(String(50), nullable=True, index=True, comment="Flight number")
    route = Column(String(100), nullable=True, index=True, comment="Route")
    actype = Column(String(50), nullable=True, index=True, comment="Aircraft type")
    seat = Column(BigInteger, nullable=True, comment="Seat capacity")
    adl = Column(Float, nullable=True, comment="Adult passengers")
    chd = Column(Float, nullable=True, comment="Child passengers")
    cgo = Column(Float, nullable=True, comment="Cargo")
    mail = Column(Float, nullable=True, comment="Mail")
    source = Column(String(500), nullable=True, index=True, comment="Source file")
    acregno = Column(String(50), nullable=True, comment="Aircraft registration")
    sheet_name = Column(String(255), nullable=True, comment="Sheet name")
    totalpax = Column(Float, nullable=True, comment="Total passengers")
    int_dom = Column(String(10), nullable=True, comment="Domestic/International")
    is_invalid_flight_date = Column(
        "Is_InvalidFlightDate", Integer, nullable=True, comment="Date validation flag"
    )
    is_invalid_passenger_cargo = Column(
        "Is_InvalidPassengerCargo",
        Integer,
        nullable=True,
        comment="Passenger/cargo validation flag",
    )
    is_invalid_route = Column(
        "Is_InvalidRoute", Integer, nullable=True, comment="Route validation flag"
    )
    is_invalid_actype_seat = Column(
        "Is_InvalidActypeSeat",
        Integer,
        nullable=True,
        comment="Aircraft type validation flag",
    )
    error_reason = Column(
        "ErrorReason", Text, nullable=True, comment="Description of errors"
    )
    total_errors = Column(
        "TotalErrors", Integer, nullable=True, index=True, comment="Total error count"
    )
    time_import = Column(
        DateTime, nullable=False, default=func.getdate(), comment="Import timestamp"
    )
    created_at = Column(
        DateTime, default=func.sysdatetime(), nullable=False, comment="Thời gian tạo"
    )

    def __repr__(self):
        """Represent the ErrorTable model as a string"""
        return f"<ErrorTable(flightno='{self.flightno}', route='{self.route}', total_errors={self.total_errors})>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "flightdate": self.flightdate,
            "flightno": self.flightno,
            "route": self.route,
            "actype": self.actype,
            "seat": self.seat,
            "adl": self.adl,
            "chd": self.chd,
            "cgo": self.cgo,
            "mail": self.mail,
            "source": self.source,
            "acregno": self.acregno,
            "sheet_name": self.sheet_name,
            "totalpax": self.totalpax,
            "int_dom": self.int_dom,
            "is_invalid_flight_date": self.is_invalid_flight_date,
            "is_invalid_passenger_cargo": self.is_invalid_passenger_cargo,
            "is_invalid_route": self.is_invalid_route,
            "is_invalid_actype_seat": self.is_invalid_actype_seat,
            "error_reason": self.error_reason,
            "total_errors": self.total_errors,
            "time_import": self.time_import,
            "created_at": self.created_at,
        }
