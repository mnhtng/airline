from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class ErrorTableBase(BaseModel):
    """
    Base schema cho ErrorTable

    Định nghĩa các trường cơ bản cho ErrorTable
    """

    flightdate: Optional[str] = Field(None, max_length=255, description="Ngày bay gốc")
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
    total_errors: Optional[int] = Field(None, ge=0, description="Tổng số lỗi")

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


class ErrorTableCreate(ErrorTableBase):
    """Schema để tạo mới ErrorTable"""

    pass


class ErrorTableUpdate(BaseModel):
    """Schema để cập nhật ErrorTable"""

    flightdate: Optional[str] = Field(None, max_length=255, description="Ngày bay gốc")
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
    total_errors: Optional[int] = Field(None, ge=0, description="Tổng số lỗi")

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


class ErrorTableInDB(ErrorTableBase):
    """Schema cho ErrorTable trong database"""

    id: int
    time_import: datetime = Field(..., description="Thời gian import")
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")

    class Config:
        from_attributes = True


class ErrorTableResponse(ErrorTableInDB):
    """Schema cho response của ErrorTable API"""

    pass


class ErrorTableBulkCreate(BaseModel):
    """Schema để tạo nhiều ErrorTable cùng lúc"""

    error_records: List[ErrorTableCreate] = Field(
        ...,
        description="Danh sách lỗi cần tạo (tối đa 1000)",
    )

    @field_validator("error_records")
    def validate_error_records_count(cls, v):
        """Custom validation message for error records count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 bản ghi lỗi mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 bản ghi lỗi để tạo")
        return v


class ErrorTableBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create ErrorTable API"""

    created_error_records: List[ErrorTableResponse] = Field(
        ..., description="Danh sách bản ghi lỗi đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số bản ghi lỗi đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
