from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class CountryRefBase(BaseModel):
    """
    Base schema cho CountryRef

    Định nghĩa các trường cơ bản cho CountryRef
    """

    country: str = Field(..., min_length=1, max_length=100, description="Tên quốc gia")
    region: str = Field(..., min_length=1, max_length=100, description="Khu vực địa lý")
    region_vnm: Optional[str] = Field(
        None, min_length=0, max_length=100, description="Khu vực địa lý tiếng Việt"
    )
    two_letter_code: str = Field(
        ..., min_length=2, max_length=2, description="Mã 2 ký tự"
    )
    three_letter_code: str = Field(
        ..., min_length=3, max_length=3, description="Mã 3 ký tự"
    )

    @field_validator("country", "region", "region_vnm")
    def validate_name(cls, v):
        """Validate name format"""
        v = v.strip()
        if not v or len(v) == 0:
            raise ValueError("Tên quốc gia hoặc khu vực địa lý không được để trống")
        return v

    @field_validator("two_letter_code", "three_letter_code")
    def validate_code(cls, v):
        """Validate code format"""
        v = v.upper().strip()
        if not v or len(v) != 2 or len(v) != 3:
            raise ValueError("Mã phải có đúng 2 hoặc 3 ký tự")
        return v


class CountryRefCreate(CountryRefBase):
    """Schema để tạo mới CountryRef"""

    pass


class CountryRefUpdate(BaseModel):
    """Schema để cập nhật CountryRef"""

    country: Optional[str] = Field(
        None, min_length=0, max_length=100, description="Tên quốc gia"
    )
    region: Optional[str] = Field(
        None, min_length=0, max_length=100, description="Khu vực địa lý"
    )
    region_vnm: Optional[str] = Field(
        None, min_length=0, max_length=100, description="Khu vực địa lý tiếng Việt"
    )
    two_letter_code: Optional[str] = Field(
        None, min_length=0, max_length=2, description="Mã 2 ký tự"
    )
    three_letter_code: Optional[str] = Field(
        None, min_length=0, max_length=3, description="Mã 3 ký tự"
    )

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


class CountryRefInDB(CountryRefBase):
    """Schema cho CountryRef trong database"""

    id: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class CountryRefResponse(CountryRefInDB):
    """Schema cho response của CountryRef API"""

    pass


class CountryRefBulkCreate(BaseModel):
    """Schema để tạo nhiều CountryRef cùng lúc"""

    country_refs: List[CountryRefCreate] = Field(
        ...,
        description="Danh sách quốc gia cần tạo (tối đa 1000)",
    )

    @field_validator("country_refs")
    def validate_country_refs_count(cls, v):
        """Custom validation message for country refs count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 quốc gia mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 quốc gia để tạo")
        return v


class CountryRefBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create CountryRef API"""

    created_country_refs: List[CountryRefResponse] = Field(
        ..., description="Danh sách quốc gia đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số quốc gia đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
