from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class ActypeSeatBase(BaseModel):
    """
    Base schema cho ActypeSeat

    Định nghĩa các trường cơ bản cho ActypeSeat
    """

    actype: str = Field(
        ..., min_length=1, max_length=50, description="Mã loại máy bay (VD: A320, B777)"
    )
    seat: int = Field(..., gt=0, description="Sức chứa ghế tiêu chuẩn")

    @field_validator("actype")
    def validate_actype(cls, v):
        """Validate aircraft type format"""
        v = v.upper().strip()
        if not v or len(v) == 0:
            raise ValueError("Mã loại máy bay không được để trống")
        return v

    @field_validator("seat")
    def validate_seat(cls, v):
        """Validate seat count"""
        if v <= 0:
            raise ValueError("Số ghế phải lớn hơn 0")
        return v


class ActypeSeatCreate(ActypeSeatBase):
    """Schema để tạo mới ActypeSeat"""

    pass


class ActypeSeatUpdate(BaseModel):
    """Schema để cập nhật ActypeSeat"""

    actype: Optional[str] = Field(
        None, min_length=1, max_length=50, description="Mã loại máy bay"
    )
    seat: Optional[int] = Field(None, gt=0, description="Sức chứa ghế")

    @field_validator("actype")
    def validate_actype(cls, v):
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) == 0:
                raise ValueError("Mã loại máy bay không được để trống")
        return v

    @field_validator("seat")
    def validate_seat(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError("Số ghế phải lớn hơn 0")
        return v


class ActypeSeatInDB(ActypeSeatBase):
    """Schema cho ActypeSeat trong database"""

    index: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class ActypeSeatResponse(ActypeSeatInDB):
    """Schema cho response của ActypeSeat API"""

    pass


class ActypeSeatBulkCreate(BaseModel):
    """Schema để tạo nhiều ActypeSeat cùng lúc"""

    actype_seats: List[ActypeSeatCreate] = Field(
        ...,
        description="Danh sách cấu hình ghế máy bay cần tạo (tối đa 1000)",
    )

    @field_validator("actype_seats")
    def validate_actype_seats_count(cls, v):
        """Custom validation message for actype seat count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 cấu hình ghế mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 cấu hình ghế để tạo")
        return v


class ActypeSeatBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create ActypeSeat API"""

    created_actype_seats: List[ActypeSeatResponse] = Field(
        ..., description="Danh sách cấu hình ghế đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số cấu hình ghế đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
