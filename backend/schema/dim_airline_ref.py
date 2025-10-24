from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class DimAirlineRefBase(BaseModel):
    """
    Base schema cho DimAirlineRef

    Định nghĩa các trường cơ bản cho DimAirlineRef
    """

    carrier: Optional[str] = Field(
        None, min_length=0, max_length=10, description="Mã hãng 2 ký tự (VD: VN, VJ)"
    )
    airline_nation: Optional[str] = Field(
        None, min_length=0, max_length=100, description="Quốc gia của hãng hàng không"
    )
    airlines_name: Optional[str] = Field(
        None, min_length=0, max_length=150, description="Tên đầy đủ của hãng hàng không"
    )

    @field_validator("carrier")
    def validate_carrier(cls, v):
        """Validate carrier code format"""
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) == 0:
                raise ValueError("Mã hãng không được để trống")
            if len(v) < 2:
                raise ValueError("Mã hãng phải có ít nhất 2 ký tự")
        return v

    @field_validator("airline_nation")
    def validate_airline_nation(cls, v):
        """Validate airline nation format"""
        if v is not None:
            v = v.strip()
            if not v or len(v) == 0:
                raise ValueError("Quốc gia của hãng hàng không không được để trống")
        return v

    @field_validator("airlines_name")
    def validate_airlines_name(cls, v):
        """Validate airlines name format"""
        if v is not None:
            v = v.strip()
            if not v or len(v) == 0:
                raise ValueError("Tên đầy đủ của hãng hàng không không được để trống")
        return v


class DimAirlineRefCreate(DimAirlineRefBase):
    """Schema để tạo mới DimAirlineRef"""

    pass


class DimAirlineRefUpdate(BaseModel):
    """Schema để cập nhật DimAirlineRef"""

    carrier: Optional[str] = Field(
        None, min_length=0, max_length=10, description="Mã hãng 2 ký tự (VD: VN, VJ)"
    )
    airline_nation: Optional[str] = Field(
        None, min_length=0, max_length=100, description="Quốc gia của hãng hàng không"
    )
    airlines_name: Optional[str] = Field(
        None, min_length=0, max_length=150, description="Tên đầy đủ của hãng hàng không"
    )

    @field_validator("carrier")
    def validate_carrier(cls, v):
        """Validate carrier code format"""
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) == 0:
                raise ValueError("Mã hãng không được để trống")
            if len(v) < 2:
                raise ValueError("Mã hãng phải có ít nhất 2 ký tự")
        return v

    @field_validator("airline_nation")
    def validate_airline_nation(cls, v):
        """Validate airline nation format"""
        if v is not None:
            v = v.strip()
            if not v or len(v) == 0:
                raise ValueError("Quốc gia của hãng hàng không không được để trống")
        return v

    @field_validator("airlines_name")
    def validate_airlines_name(cls, v):
        """Validate airlines name format"""
        if v is not None:
            v = v.strip()
            if not v or len(v) == 0:
                raise ValueError("Tên đầy đủ của hãng hàng không không được để trống")
        return v


class DimAirlineRefInDB(DimAirlineRefBase):
    """Schema cho DimAirlineRef trong database"""

    id: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class DimAirlineRefResponse(DimAirlineRefInDB):
    """Schema cho response của DimAirlineRef"""

    pass


class DimAirlineRefBulkCreate(BaseModel):
    """Schema để tạo nhiều DimAirlineRef cùng lúc"""

    dim_airline_refs: List[DimAirlineRefCreate] = Field(
        ..., description="Danh sách DimAirlineRef cần tạo"
    )

    @field_validator("dim_airline_refs")
    def validate_dim_airline_refs_count(cls, v):
        """Validate dim airline refs count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 hãng hàng không mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 hãng hàng không để tạo")
        return v


class DimAirlineRefBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create DimAirlineRef API"""

    created_dim_airline_refs: List[DimAirlineRefResponse] = Field(
        ..., description="Danh sách DimAirlineRef đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số DimAirlineRef đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
