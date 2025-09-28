from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class FlightCleanDataStgBase(BaseModel):
    """
    Base schema cho FlightCleanDataStg

    Định nghĩa các trường cơ bản cho FlightCleanDataStg
    """

    flightdate: Optional[str] = Field(None, max_length=255, description="Ngày bay")
    flightno: Optional[str] = Field(
        None, max_length=50, description="Số hiệu chuyến bay"
    )
    route: Optional[str] = Field(None, max_length=100, description="Tuyến bay")
    actype: Optional[str] = Field(None, max_length=50, description="Loại máy bay")
    seat: Optional[int] = Field(None, ge=0, description="Sức chứa ghế")
    adl: Optional[float] = Field(None, ge=0, description="Số hành khách người lớn")
    chd: Optional[float] = Field(None, ge=0, description="Số hành khách trẻ em")
    cgo: Optional[float] = Field(None, ge=0, description="Hàng hóa")
    mail: Optional[float] = Field(None, ge=0, description="Bưu kiện")
    source: Optional[str] = Field(None, max_length=500, description="File nguồn")
    acregno: Optional[str] = Field(
        None, max_length=50, description="Số đăng ký máy bay"
    )
    sheet_name: Optional[str] = Field(None, max_length=255, description="Tên sheet")
    totalpax: Optional[float] = Field(None, ge=0, description="Tổng số hành khách")
    int_dom: Optional[str] = Field(
        None, max_length=10, description="Domestic/International"
    )
    is_invalid_flight_date: Optional[int] = Field(
        None, description="Cờ validation ngày bay"
    )
    is_invalid_passenger_cargo: Optional[int] = Field(
        None, description="Cờ validation hành khách/hàng hóa"
    )
    is_invalid_route: Optional[int] = Field(None, description="Cờ validation tuyến bay")
    is_invalid_actype_seat: Optional[int] = Field(
        None, description="Cờ validation loại máy bay"
    )
    error_reason: Optional[str] = Field(None, description="Mô tả lỗi")
    total_errors: Optional[int] = Field(None, ge=0, description="Số lượng lỗi")

    @field_validator("int_dom")
    def validate_int_dom(cls, v):
        """Validate domestic/international flag"""
        if v is not None:
            v = v.upper().strip()
            if v and v not in ["DOM", "INT"]:
                raise ValueError("int_dom phải là 'DOM' hoặc 'INT'")
        return v

    @field_validator(
        "is_invalid_flight_date",
        "is_invalid_passenger_cargo",
        "is_invalid_route",
        "is_invalid_actype_seat",
    )
    def validate_error_flags(cls, v):
        """Validate error flags (0 or 1)"""
        if v is not None and v not in [0, 1]:
            raise ValueError("Cờ lỗi phải là 0 hoặc 1")
        return v


class FlightCleanDataStgCreate(FlightCleanDataStgBase):
    """Schema để tạo mới FlightCleanDataStg"""

    pass


class FlightCleanDataStgUpdate(BaseModel):
    """Schema để cập nhật FlightCleanDataStg"""

    flightdate: Optional[str] = Field(None, max_length=255, description="Ngày bay")
    flightno: Optional[str] = Field(
        None, max_length=50, description="Số hiệu chuyến bay"
    )
    route: Optional[str] = Field(None, max_length=100, description="Tuyến bay")
    actype: Optional[str] = Field(None, max_length=50, description="Loại máy bay")
    seat: Optional[int] = Field(None, ge=0, description="Sức chứa ghế")
    adl: Optional[float] = Field(None, ge=0, description="Số hành khách người lớn")
    chd: Optional[float] = Field(None, ge=0, description="Số hành khách trẻ em")
    cgo: Optional[float] = Field(None, ge=0, description="Hàng hóa")
    mail: Optional[float] = Field(None, ge=0, description="Bưu kiện")
    source: Optional[str] = Field(None, max_length=500, description="File nguồn")
    acregno: Optional[str] = Field(
        None, max_length=50, description="Số đăng ký máy bay"
    )
    sheet_name: Optional[str] = Field(None, max_length=255, description="Tên sheet")
    totalpax: Optional[float] = Field(None, ge=0, description="Tổng số hành khách")
    int_dom: Optional[str] = Field(
        None, max_length=10, description="Domestic/International"
    )
    is_invalid_flight_date: Optional[int] = Field(
        None, description="Cờ validation ngày bay"
    )
    is_invalid_passenger_cargo: Optional[int] = Field(
        None, description="Cờ validation hành khách/hàng hóa"
    )
    is_invalid_route: Optional[int] = Field(None, description="Cờ validation tuyến bay")
    is_invalid_actype_seat: Optional[int] = Field(
        None, description="Cờ validation loại máy bay"
    )
    error_reason: Optional[str] = Field(None, description="Mô tả lỗi")
    total_errors: Optional[int] = Field(None, ge=0, description="Số lượng lỗi")

    @field_validator("int_dom")
    def validate_int_dom(cls, v):
        if v is not None:
            v = v.upper().strip()
            if v and v not in ["DOM", "INT"]:
                raise ValueError("int_dom phải là 'DOM' hoặc 'INT'")
        return v

    @field_validator(
        "is_invalid_flight_date",
        "is_invalid_passenger_cargo",
        "is_invalid_route",
        "is_invalid_actype_seat",
    )
    def validate_error_flags(cls, v):
        if v is not None and v not in [0, 1]:
            raise ValueError("Cờ lỗi phải là 0 hoặc 1")
        return v


class FlightCleanDataStgInDB(FlightCleanDataStgBase):
    """Schema cho FlightCleanDataStg trong database"""

    id: int
    inserted_time: datetime = Field(..., description="Thời gian chèn")
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")

    class Config:
        from_attributes = True


class FlightCleanDataStgResponse(FlightCleanDataStgInDB):
    """Schema cho response của FlightCleanDataStg API"""

    pass


class FlightCleanDataStgBulkCreate(BaseModel):
    """Schema để tạo nhiều FlightCleanDataStg cùng lúc"""

    staging_records: List[FlightCleanDataStgCreate] = Field(
        ...,
        description="Danh sách dữ liệu staging cần tạo (tối đa 1000)",
    )

    @field_validator("staging_records")
    def validate_staging_records_count(cls, v):
        """Custom validation message for staging records count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 bản ghi staging mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 bản ghi staging để tạo")
        return v


class FlightCleanDataStgBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create FlightCleanDataStg API"""

    created_staging_records: List[FlightCleanDataStgResponse] = Field(
        ..., description="Danh sách bản ghi staging đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số bản ghi staging đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
