from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class DimCountryRefBase(BaseModel):
    """
    Base schema cho DimCountryRef

    Định nghĩa các trường cơ bản cho DimCountryRef
    """

    country: Optional[str] = Field(None, ge=0, le=100, description="Tên quốc gia")
    region: Optional[str] = Field(None, ge=0, le=100, description="Khu vực địa lý")
    region_vnm: Optional[str] = Field(
        None, ge=0, le=100, description="Khu vực địa lý tiếng Việt"
    )
    two_letter_code: Optional[str] = Field(None, ge=0, le=2, description="Mã 2 ký tự")
    three_letter_code: Optional[str] = Field(None, ge=0, le=3, description="Mã 3 ký tự")

    @field_validator("country", "region", "region_vnm")
    def validate_name(cls, v):
        """Validate name format"""
        if v is not None:
            v = v.strip()
            if not v or len(v) == 0:
                raise ValueError("Tên quốc gia hoặc khu vực địa lý không được để trống")
        return v

    @field_validator("two_letter_code", "three_letter_code")
    def validate_code(cls, v):
        """Validate code format"""
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) != 2 or len(v) != 3:
                raise ValueError("Mã phải có đúng 2 hoặc 3 ký tự")
        return v


class DimCountryRefCreate(DimCountryRefBase):
    """Schema để tạo mới DimCountryRef"""

    pass


class DimCountryRefUpdate(BaseModel):
    """Schema để cập nhật DimCountryRef"""

    country: Optional[str] = Field(None, ge=0, le=100, description="Tên quốc gia")
    region: Optional[str] = Field(None, ge=0, le=100, description="Khu vực địa lý")
    region_vnm: Optional[str] = Field(
        None, ge=0, le=100, description="Khu vực địa lý tiếng Việt"
    )
    two_letter_code: Optional[str] = Field(None, ge=0, le=2, description="Mã 2 ký tự")
    three_letter_code: Optional[str] = Field(None, ge=0, le=3, description="Mã 3 ký tự")

    @field_validator("country", "region", "region_vnm")
    def validate_name(cls, v):
        """Validate name format"""
        if v is not None:
            v = v.strip()
            if not v or len(v) == 0:
                raise ValueError("Tên quốc gia hoặc khu vực địa lý không được để trống")
        return v

    @field_validator("two_letter_code", "three_letter_code")
    def validate_code(cls, v):
        """Validate code format"""
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) != 2 or len(v) != 3:
                raise ValueError("Mã phải có đúng 2 hoặc 3 ký tự")
        return v


class DimCountryRefInDB(DimCountryRefBase):
    """Schema cho DimCountryRef trong database"""

    id: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class DimCountryRefResponse(DimCountryRefInDB):
    """Schema cho response của DimCountryRef"""

    pass


class DimCountryRefBulkCreate(BaseModel):
    """Schema để tạo nhiều DimCountryRef cùng lúc"""

    dim_country_refs: List[DimCountryRefCreate] = Field(
        ..., description="Danh sách DimCountryRef cần tạo"
    )

    @field_validator("dim_country_refs")
    def validate_dim_country_refs_count(cls, v):
        """Validate dim country refs count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 quốc gia mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 quốc gia để tạo")
        return v


class DimCountryRefBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create DimCountryRef API"""

    created_dim_country_refs: List[DimCountryRefResponse] = Field(
        ..., description="Danh sách DimCountryRef đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số DimCountryRef đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
