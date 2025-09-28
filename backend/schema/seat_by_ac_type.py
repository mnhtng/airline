from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class SeatByACTypeBase(BaseModel):
    """
    Base schema cho SeatByACType

    Định nghĩa các trường cơ bản cho SeatByACType
    """

    ac_reg_no: str = Field(
        ..., min_length=1, max_length=20, description="Số đăng ký máy bay"
    )
    brand: Optional[str] = Field(
        None, max_length=50, description="Nhà sản xuất máy bay"
    )
    ac_type: Optional[str] = Field(None, max_length=50, description="Loại máy bay")
    seat: Optional[int] = Field(
        None, ge=0, description="Số ghế thực tế của máy bay này"
    )

    @field_validator("ac_reg_no")
    def validate_ac_reg_no(cls, v):
        """Validate aircraft registration number"""
        v = v.upper().strip()
        if not v or len(v) == 0:
            raise ValueError("Số đăng ký máy bay không được để trống")
        return v

    @field_validator("seat")
    def validate_seat(cls, v):
        """Validate seat count"""
        if v is not None:
            if v < 0:
                raise ValueError("Số ghế không được âm")
            if v > 1000:
                raise ValueError("Số ghế không được vượt quá 1000")
        return v

    @field_validator("ac_type")
    def validate_ac_type(cls, v):
        """Validate aircraft type"""
        if v is not None:
            v = v.upper().strip()
        return v


class SeatByACTypeCreate(SeatByACTypeBase):
    """Schema để tạo mới SeatByACType"""

    pass


class SeatByACTypeUpdate(BaseModel):
    """Schema để cập nhật SeatByACType"""

    ac_reg_no: Optional[str] = Field(
        None, min_length=1, max_length=20, description="Số đăng ký máy bay"
    )
    brand: Optional[str] = Field(
        None, max_length=50, description="Nhà sản xuất máy bay"
    )
    ac_type: Optional[str] = Field(None, max_length=50, description="Loại máy bay")
    seat: Optional[int] = Field(None, ge=0, description="Số ghế thực tế")

    @field_validator("ac_reg_no")
    def validate_ac_reg_no(cls, v):
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) == 0:
                raise ValueError("Số đăng ký máy bay không được để trống")
        return v

    @field_validator("seat")
    def validate_seat(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Số ghế không được âm")
            if v > 1000:
                raise ValueError("Số ghế không được vượt quá 1000")
        return v

    @field_validator("ac_type")
    def validate_ac_type(cls, v):
        if v is not None:
            v = v.upper().strip()
        return v


class SeatByACTypeInDB(SeatByACTypeBase):
    """Schema cho SeatByACType trong database"""

    id: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class SeatByACTypeResponse(SeatByACTypeInDB):
    """Schema cho response của SeatByACType API"""

    pass


class SeatByACTypeBulkCreate(BaseModel):
    """Schema để tạo nhiều SeatByACType cùng lúc"""

    seat_by_ac_types: List[SeatByACTypeCreate] = Field(
        ...,
        description="Danh sách thông tin máy bay cần tạo (tối đa 1000)",
    )

    @field_validator("seat_by_ac_types")
    def validate_seat_by_ac_types_count(cls, v):
        """Custom validation message for seat by ac type count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 thông tin máy bay mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 thông tin máy bay để tạo")
        return v


class SeatByACTypeBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create SeatByACType API"""

    created_seat_by_ac_types: List[SeatByACTypeResponse] = Field(
        ..., description="Danh sách thông tin máy bay đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số thông tin máy bay đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
