from sqlalchemy import INT, NVARCHAR, Column, BigInteger, String, Float, DateTime
from sqlalchemy.sql import func

from backend.db.database import Base


class FlightRaw(Base):
    """
    Model cho dữ liệu flight raw - Initial data import từ Excel files

    Lưu trữ dữ liệu flight raw trước khi xử lý và validation

    Attributes:
        id: ID duy nhất của bản ghi
        flightdate: Ngày bay (các định dạng khác nhau từ Excel)
        flightno: Số hiệu chuyến bay
        route: Tuyến bay (VD: SGN-HAN)
        actype: Loại máy bay
        seat: Sức chứa ghế
        adl: Số hành khách người lớn
        chd: Số hành khách trẻ em
        cgo: Khối lượng hàng hóa
        mail: Khối lượng bưu kiện
        totalpax: Tổng số hành khách (được tính)
        source: Tên file nguồn
        acregno: Số đăng ký máy bay
        sheet_name: Tên sheet Excel
        int_dom: Cờ Domestic/International
        is_invalid_flightdate: Cờ kiểm tra tính hợp lệ của ngày bay
        is_invalid_passenger_cargo: Cờ kiểm tra tính hợp lệ của hành khách và hàng hóa
        is_invalid_route: Cờ kiểm tra tính hợp lệ của tuyến bay
        is_invalid_actype_seat: Cờ kiểm tra tính hợp lệ của loại máy bay và sức chứa ghế
        error_reason: Mô tả lỗi nếu có
        total_errors: Tổng số lỗi phát hiện
        created_at: Thời gian tạo bản ghi
    """

    __tablename__ = "flight_raw"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    flightdate = Column(
        String(255),
        nullable=True,
        index=True,
        comment="Flight date (various formats from Excel)",
    )
    flightno = Column(String(50), nullable=True, comment="Flight number")
    route = Column(
        String(100), nullable=True, index=True, comment="Route (e.g., SGN-HAN)"
    )
    actype = Column(String(50), nullable=True, comment="Aircraft type")
    seat = Column(BigInteger, nullable=True, comment="Seat capacity")
    adl = Column(Float, nullable=True, comment="Adult passengers")
    chd = Column(Float, nullable=True, comment="Child passengers")
    cgo = Column(Float, nullable=True, comment="Cargo weight")
    mail = Column(Float, nullable=True, comment="Mail weight")
    totalpax = Column(Float, nullable=True, comment="Total passengers (calculated)")
    source = Column(String(500), nullable=True, index=True, comment="Source file name")
    acregno = Column(String(50), nullable=True, comment="Aircraft registration")
    sheet_name = Column(String(255), nullable=True, comment="Excel sheet name")
    int_dom = Column(String(10), nullable=True, comment="Domestic/International flag")
    is_invalid_flightdate = Column(
        "Is_InvalidFlightDate", BigInteger, nullable=True, comment="Validation flags"
    )
    is_invalid_passenger_cargo = Column(
        "Is_InvalidPassengerCargo",
        BigInteger,
        nullable=True,
        comment="Validation flags",
    )
    is_invalid_route = Column(
        "Is_InvalidRoute", BigInteger, nullable=True, comment="Validation flags"
    )
    is_invalid_actype_seat = Column(
        "Is_InvalidActypeSeat", BigInteger, nullable=True, comment="Validation flags"
    )
    error_reason = Column(
        "ErrorReason", NVARCHAR(1000), nullable=True, comment="Description of errors"
    )
    total_errors = Column(
        "TotalErrors", INT, nullable=True, comment="Total error count"
    )
    created_at = Column(
        DateTime, default=func.sysdatetime(), nullable=False, comment="Thời gian tạo"
    )

    def __repr__(self):
        """Represent the FlightRaw model as a string"""
        return f"<FlightRaw(flightno='{self.flightno}', route='{self.route}', actype='{self.actype}')>"

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
            "totalpax": self.totalpax,
            "source": self.source,
            "acregno": self.acregno,
            "sheet_name": self.sheet_name,
            "int_dom": self.int_dom,
            "is_invalid_flightdate": self.is_invalid_flightdate,
            "is_invalid_passenger_cargo": self.is_invalid_passenger_cargo,
            "is_invalid_route": self.is_invalid_route,
            "is_invalid_actype_seat": self.is_invalid_actype_seat,
            "error_reason": self.error_reason,
            "total_errors": self.total_errors,
            "created_at": self.created_at,
        }
