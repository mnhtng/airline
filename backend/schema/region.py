from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class RegionBase(BaseModel):
    """
    Base schema cho Region

    Định nghĩa các trường cơ bản cho Region
    """

    country: str = Field(..., min_length=1, max_length=100, description="Tên quốc gia")
    region: str = Field(..., min_length=1, max_length=100, description="Khu vực địa lý")

    @field_validator("country")
    def validate_country(cls, v):
        """Validate country name"""
        v = v.strip()
        if not v or len(v) == 0:
            raise ValueError("Tên quốc gia không được để trống")
        return v

    @field_validator("region")
    def validate_region(cls, v):
        """Validate region name"""
        v = v.strip()
        if not v or len(v) == 0:
            raise ValueError("Tên khu vực không được để trống")
        return v


class RegionCreate(RegionBase):
    """Schema để tạo mới Region"""

    pass


class RegionUpdate(BaseModel):
    """Schema để cập nhật Region"""

    country: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Tên quốc gia"
    )
    region: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Khu vực địa lý"
    )

    @field_validator("country")
    def validate_country(cls, v):
        if v is not None:
            v = v.strip()
            if not v or len(v) == 0:
                raise ValueError("Tên quốc gia không được để trống")
        return v

    @field_validator("region")
    def validate_region(cls, v):
        if v is not None:
            v = v.strip()
            if not v or len(v) == 0:
                raise ValueError("Tên khu vực không được để trống")
        return v


class RegionInDB(RegionBase):
    """Schema cho Region trong database"""

    index: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class RegionResponse(RegionInDB):
    """Schema cho response của Region API"""

    pass


class RegionBulkCreate(BaseModel):
    """Schema để tạo nhiều Region cùng lúc"""

    regions: List[RegionCreate] = Field(
        ...,
        description="Danh sách khu vực cần tạo (tối đa 1000)",
    )

    @field_validator("regions")
    def validate_regions_count(cls, v):
        """Custom validation message for region count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 khu vực mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 khu vực để tạo")
        return v


class RegionBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create Region API"""

    created_regions: List[RegionResponse] = Field(
        ..., description="Danh sách khu vực đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số khu vực đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
