from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class AirlineRefBase(BaseModel):
    """
    Base schema cho AirlineRef

    Định nghĩa các trường cơ bản cho AirlineRef
    """

    carrier: Optional[str] = Field(
        None, min_length=0, max_length=50, description="Mã hãng 2 ký tự (VD: VN, VJ)"
    )
    airline_nation: Optional[str] = Field(
        None, min_length=0, max_length=255, description="Quốc gia của hãng hàng không"
    )
    airlines_name: Optional[str] = Field(
        None, min_length=0, max_length=255, description="Tên đầy đủ của hãng hàng không"
    )

    @field_validator("carrier")
    def validate_carrier(cls, v):
        """Validate carrier code format"""
        if v and len(v) == 0:
            raise ValueError("Mã hãng không được để trống")
        return v.upper().strip() if v else None

    @field_validator("airline_nation")
    def validate_airline_nation(cls, v):
        """Validate airline nation format"""
        if v and len(v) == 0:
            raise ValueError("Quốc gia của hãng hàng không không được để trống")
        return v.strip() if v else None

    @field_validator("airlines_name")
    def validate_airlines_name(cls, v):
        """Validate airlines name format"""
        if v and len(v) == 0:
            raise ValueError("Tên đầy đủ của hãng hàng không không được để trống")
        return v.strip() if v else None


class AirlineRefCreate(AirlineRefBase):
    """Schema để tạo mới AirlineRef"""

    pass


class AirlineRefUpdate(BaseModel):
    """Schema để cập nhật AirlineRef"""

    carrier: Optional[str] = Field(
        None, min_length=0, max_length=50, description="Mã hãng 2 ký tự (VD: VN, VJ)"
    )
    airline_nation: Optional[str] = Field(
        None, min_length=0, max_length=255, description="Quốc gia của hãng hàng không"
    )
    airlines_name: Optional[str] = Field(
        None, min_length=0, max_length=255, description="Tên đầy đủ của hãng hàng không"
    )

    @field_validator("carrier")
    def validate_carrier(cls, v):
        """Validate carrier code format"""
        if v and len(v) == 0:
            raise ValueError("Mã hãng không được để trống")
        return v.upper().strip() if v else None

    @field_validator("airline_nation")
    def validate_airline_nation(cls, v):
        """Validate airline nation format"""
        if v and len(v) == 0:
            raise ValueError("Quốc gia của hãng hàng không không được để trống")
        return v.strip() if v else None

    @field_validator("airlines_name")
    def validate_airlines_name(cls, v):
        """Validate airlines name format"""
        if v and len(v) == 0:
            raise ValueError("Tên đầy đủ của hãng hàng không không được để trống")
        return v.strip() if v else None


class AirlineRefInDB(AirlineRefBase):
    """Schema cho AirlineRef trong database"""

    id: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class AirlineRefResponse(AirlineRefInDB):
    """Schema cho response của AirlineRef"""

    pass


class AirlineRefBulkCreate(BaseModel):
    """Schema để tạo nhiều AirlineRef cùng lúc"""

    airline_refs: List[AirlineRefCreate] = Field(
        ..., description="Danh sách AirlineRef cần tạo"
    )

    @field_validator("airline_refs")
    def validate_airline_refs_count(cls, v):
        """Validate airline refs count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 hãng hàng không mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 hãng hàng không để tạo")
        return v


class AirlineRefBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create AirlineRef API"""

    created_airline_refs: List[AirlineRefResponse] = Field(
        ..., description="Danh sách AirlineRef đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số AirlineRef đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
