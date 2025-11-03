from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class DimAirportRefBase(BaseModel):
    """
    Base schema cho DimAirportRef

    Định nghĩa các trường cơ bản cho DimAirportRef
    """

    iata_code: Optional[str] = Field(
        None, min_length=0, max_length=50, description="Mã sân bay"
    )
    airport_name: Optional[str] = Field(
        None, min_length=0, max_length=255, description="Tên sân bay"
    )
    city: Optional[str] = Field(
        None, min_length=0, max_length=255, description="Thành phố nơi sân bay được đặt"
    )
    country: Optional[str] = Field(
        None, min_length=0, max_length=255, description="Quốc gia nơi sân bay được đặt"
    )

    @field_validator("iata_code")
    def validate_iata_code(cls, v):
        """Validate iata code format"""
        if v and len(v) == 0:
            raise ValueError("Mã sân bay không được để trống")
        return v.upper().strip() if v else None

    @field_validator("airport_name")
    def validate_airport_name(cls, v):
        """Validate airport name format"""
        if v and len(v) == 0:
            raise ValueError("Tên sân bay không được để trống")
        return v.strip() if v else None

    @field_validator("city")
    def validate_city(cls, v):
        """Validate city format"""
        if v and len(v) == 0:
            raise ValueError("Thành phố nơi sân bay được đặt không được để trống")
        return v.strip() if v else None

    @field_validator("country")
    def validate_country(cls, v):
        """Validate country format"""
        if v and len(v) == 0:
            raise ValueError("Quốc gia nơi sân bay được đặt không được để trống")
        return v.strip() if v else None


class DimAirportRefCreate(DimAirportRefBase):
    """Schema để tạo DimAirportRef"""

    pass


class DimAirportRefUpdate(DimAirportRefBase):
    """Schema để cập nhật DimAirportRef"""

    iata_code: Optional[str] = Field(
        None, min_length=0, max_length=50, description="Mã sân bay"
    )
    airport_name: Optional[str] = Field(
        None, min_length=0, max_length=255, description="Tên sân bay"
    )
    city: Optional[str] = Field(
        None, min_length=0, max_length=255, description="Thành phố nơi sân bay được đặt"
    )
    country: Optional[str] = Field(
        None, min_length=0, max_length=255, description="Quốc gia nơi sân bay được đặt"
    )

    @field_validator("iata_code")
    def validate_iata_code(cls, v):
        """Validate iata code format"""
        if v and len(v) == 0:
            raise ValueError("Mã sân bay không được để trống")
        return v.upper().strip() if v else None

    @field_validator("airport_name")
    def validate_airport_name(cls, v):
        """Validate airport name format"""
        if v and len(v) == 0:
            raise ValueError("Tên sân bay không được để trống")
        return v.strip() if v else None

    @field_validator("city")
    def validate_city(cls, v):
        """Validate city format"""
        if v and len(v) == 0:
            raise ValueError("Thành phố nơi sân bay được đặt không được để trống")
        return v.strip() if v else None

    @field_validator("country")
    def validate_country(cls, v):
        """Validate country format"""
        if v and len(v) == 0:
            raise ValueError("Quốc gia nơi sân bay được đặt không được để trống")
        return v.strip() if v else None


class DimAirportRefInDB(DimAirportRefBase):
    """Schema cho DimAirportRef trong database"""

    id: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class DimAirportRefResponse(DimAirportRefInDB):
    """Schema cho response của DimAirportRef"""

    pass


class DimAirportRefBulkCreate(BaseModel):
    """Schema để tạo nhiều DimAirportRef cùng lúc"""

    dim_airport_refs: List[DimAirportRefCreate] = Field(
        ..., description="Danh sách DimAirportRef cần tạo"
    )

    @field_validator("dim_airport_refs")
    def validate_dim_airport_refs_count(cls, v):
        """Validate dim airport refs count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 sân bay mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 sân bay để tạo")
        return v


class DimAirportRefBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create DimAirportRef API"""

    created_dim_airport_refs: List[DimAirportRefResponse] = Field(
        ..., description="Danh sách DimAirportRef đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số DimAirportRef đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
