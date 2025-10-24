from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class AirportRefBase(BaseModel):
    """
    Base schema cho AirportRef

    Định nghĩa các trường cơ bản cho AirportRef
    """

    airport_code: str = Field(
        ..., min_length=1, max_length=10, description="Mã sân bay"
    )
    airport_name: str = Field(
        ..., min_length=1, max_length=200, description="Tên sân bay"
    )
    city: str = Field(
        ..., min_length=1, max_length=100, description="Thành phố nơi sân bay được đặt"
    )
    country: str = Field(
        ..., min_length=1, max_length=100, description="Quốc gia nơi sân bay được đặt"
    )

    @field_validator("airport_code")
    def validate_airport_code(cls, v):
        """Validate airport code format"""
        v = v.upper().strip()
        if not v or len(v) == 0:
            raise ValueError("Mã sân bay không được để trống")
        if len(v) < 3:
            raise ValueError("Mã sân bay phải có ít nhất 3 ký tự")
        return v

    @field_validator("airport_name")
    def validate_airport_name(cls, v):
        """Validate airport name format"""
        v = v.strip()
        if not v or len(v) == 0:
            raise ValueError("Tên sân bay không được để trống")
        return v

    @field_validator("city")
    def validate_city(cls, v):
        """Validate city format"""
        v = v.strip()
        if not v or len(v) == 0:
            raise ValueError("Thành phố nơi sân bay được đặt không được để trống")
        return v

    @field_validator("country")
    def validate_country(cls, v):
        """Validate country format"""
        v = v.strip()
        if not v or len(v) == 0:
            raise ValueError("Quốc gia nơi sân bay được đặt không được để trống")
        return v


class AirportRefCreate(AirportRefBase):
    """Schema để tạo AirportRef"""

    pass


class AirportRefUpdate(AirportRefBase):
    """Schema để cập nhật AirportRef"""

    airport_code: Optional[str] = Field(None, ge=0, le=10, description="Mã sân bay")
    airport_name: Optional[str] = Field(None, ge=0, le=200, description="Tên sân bay")
    city: Optional[str] = Field(
        None, ge=0, le=100, description="Thành phố nơi sân bay được đặt"
    )
    country: Optional[str] = Field(
        None, ge=0, le=100, description="Quốc gia nơi sân bay được đặt"
    )

    @field_validator("airport_code")
    def validate_airport_code(cls, v):
        """Validate airport code format"""
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) == 0:
                raise ValueError("Mã sân bay không được để trống")
            if len(v) < 3:
                raise ValueError("Mã sân bay phải có ít nhất 3 ký tự")
        return v

    @field_validator("airport_name")
    def validate_airport_name(cls, v):
        """Validate airport name format"""
        if v is not None:
            v = v.strip()
            if not v or len(v) == 0:
                raise ValueError("Tên sân bay không được để trống")
        return v

    @field_validator("city")
    def validate_city(cls, v):
        """Validate city format"""
        if v is not None:
            v = v.strip()
            if not v or len(v) == 0:
                raise ValueError("Thành phố nơi sân bay được đặt không được để trống")
        return v

    @field_validator("country")
    def validate_country(cls, v):
        """Validate country format"""
        if v is not None:
            v = v.strip()
            if not v or len(v) == 0:
                raise ValueError("Quốc gia nơi sân bay được đặt không được để trống")
        return v


class AirportRefInDB(AirportRefBase):
    """Schema cho AirportRef trong database"""

    id: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class AirportRefResponse(AirportRefInDB):
    """Schema cho response của AirportRef"""

    pass


class AirportRefBulkCreate(BaseModel):
    """Schema để tạo nhiều AirportRef cùng lúc"""

    airport_refs: List[AirportRefCreate] = Field(
        ..., description="Danh sách AirportRef cần tạo"
    )

    @field_validator("airport_refs")
    def validate_airport_refs_count(cls, v):
        """Validate airport refs count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 sân bay mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 sân bay để tạo")
        return v


class AirportRefBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create AirportRef API"""

    created_airport_refs: List[AirportRefResponse] = Field(
        ..., description="Danh sách AirportRef đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số AirportRef đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
