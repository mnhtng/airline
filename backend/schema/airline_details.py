from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class AirlineDetailsBase(BaseModel):
    """
    Base schema cho AirlineDetails

    Định nghĩa các trường cơ bản cho AirlineDetails
    """

    carrier: str = Field(
        ..., min_length=1, max_length=10, description="Mã hãng 2 ký tự (VD: VN, VJ)"
    )
    qg: Optional[str] = Field(
        None, max_length=10, description="Mã quốc gia của hãng hàng không"
    )
    airlines_name: Optional[str] = Field(
        None, max_length=255, description="Tên đầy đủ của hãng hàng không"
    )

    @field_validator("carrier")
    def validate_carrier(cls, v):
        """Validate carrier code format"""
        v = v.upper().strip()
        if not v or len(v) == 0:
            raise ValueError("Mã hãng không được để trống")
        if len(v) < 2:
            raise ValueError("Mã hãng phải có ít nhất 2 ký tự")
        return v


class AirlineDetailsCreate(AirlineDetailsBase):
    """Schema để tạo mới AirlineDetails"""

    pass


class AirlineDetailsUpdate(BaseModel):
    """Schema để cập nhật AirlineDetails"""

    carrier: Optional[str] = Field(
        None, min_length=1, max_length=10, description="Mã hãng"
    )
    qg: Optional[str] = Field(
        None, max_length=10, description="Mã quốc gia của hãng hàng không"
    )
    airlines_name: Optional[str] = Field(
        None, max_length=255, description="Tên hãng hàng không"
    )

    @field_validator("carrier")
    def validate_carrier(cls, v):
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) == 0:
                raise ValueError("Mã hãng không được để trống")
            if len(v) < 2:
                raise ValueError("Mã hãng phải có ít nhất 2 ký tự")
        return v


class AirlineDetailsInDB(AirlineDetailsBase):
    """Schema cho AirlineDetails trong database"""

    index: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class AirlineDetailsResponse(AirlineDetailsInDB):
    """Schema cho response của AirlineDetails API"""

    pass


class AirlineDetailsBulkCreate(BaseModel):
    """Schema để tạo nhiều AirlineDetails cùng lúc"""

    airline_details: List[AirlineDetailsCreate] = Field(
        ...,
        description="Danh sách hãng hàng không cần tạo (tối đa 1000)",
    )

    @field_validator("airline_details")
    def validate_airline_details_count(cls, v):
        """Custom validation message for airline details count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 hãng hàng không mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 hãng hàng không để tạo")
        return v


class AirlineDetailsBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create AirlineDetails API"""

    created_airline_details: List[AirlineDetailsResponse] = Field(
        ..., description="Danh sách hãng hàng không đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số hãng hàng không đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
