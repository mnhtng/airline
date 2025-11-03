from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class DimSectorRouteDomRefBase(BaseModel):
    """
    Base schema cho DimSectorRouteDomRef

    Định nghĩa các trường cơ bản cho DimSectorRouteDomRef
    """

    sector: Optional[str] = Field(
        None, min_length=0, max_length=50, description="Mã sector tuyến bay"
    )
    area_lv1: Optional[str] = Field(
        None, min_length=0, max_length=255, description="Khu vực/vùng địa lý level 1"
    )
    dom_int: Optional[str] = Field(
        None,
        min_length=0,
        max_length=20,
        description="Nội địa / Quốc tế",
    )

    @field_validator("sector")
    def validate_sector(cls, v):
        """Validate sector format"""
        if v and len(v) == 0:
            raise ValueError("Mã sector không được để trống")
        return v.strip() if v else None

    @field_validator("area_lv1")
    def validate_area_lv1(cls, v):
        """Validate area lv1 format"""
        if v and len(v) == 0:
            raise ValueError("Vùng cấp 1 không được để trống")
        return v.strip() if v else None

    @field_validator("dom_int")
    def validate_dom_int(cls, v):
        """Validate dom int format"""
        if v and len(v) == 0:
            raise ValueError("Nội địa / Quốc tế không được để trống")
        if v and v not in ["DOM", "INT"]:
            raise ValueError("Nội địa / Quốc tế không hợp lệ")
        return v.strip() if v else None


class DimSectorRouteDomRefCreate(DimSectorRouteDomRefBase):
    """Schema để tạo DimSectorRouteDomRef"""

    pass


class DimSectorRouteDomRefUpdate(DimSectorRouteDomRefBase):
    """Schema để cập nhật DimSectorRouteDomRef"""

    sector: Optional[str] = Field(
        None, min_length=0, max_length=50, description="Mã sector tuyến bay"
    )
    area_lv1: Optional[str] = Field(
        None, min_length=0, max_length=255, description="Khu vực/vùng địa lý level 1"
    )
    dom_int: Optional[str] = Field(
        None,
        min_length=0,
        max_length=20,
        description="Nội địa / Quốc tế",
    )

    @field_validator("sector")
    def validate_sector(cls, v):
        """Validate sector format"""
        if v and len(v) == 0:
            raise ValueError("Mã sector không được để trống")
        return v.strip() if v else None

    @field_validator("area_lv1")
    def validate_area_lv1(cls, v):
        """Validate area lv1 format"""
        if v and len(v) == 0:
            raise ValueError("Vùng cấp 1 không được để trống")
        return v.strip() if v else None

    @field_validator("dom_int")
    def validate_dom_int(cls, v):
        """Validate dom int format"""
        if v and len(v) == 0:
            raise ValueError("Nội địa / Quốc tế không được để trống")
        if v and v not in ["DOM", "INT"]:
            raise ValueError("Nội địa / Quốc tế không hợp lệ")
        return v.strip() if v else None


class DimSectorRouteDomRefInDB(DimSectorRouteDomRefBase):
    """Schema cho DimSectorRouteDomRef trong database"""

    id: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class DimSectorRouteDomRefResponse(DimSectorRouteDomRefInDB):
    """Schema cho response của DimSectorRouteDomRef"""

    pass


class DimSectorRouteDomRefBulkCreate(BaseModel):
    """Schema để tạo nhiều DimSectorRouteDomRef cùng lúc"""

    dim_sector_route_dom_refs: List[DimSectorRouteDomRefCreate] = Field(
        ..., description="Danh sách DimSectorRouteDomRef cần tạo"
    )

    @field_validator("dim_sector_route_dom_refs")
    def validate_dim_sector_route_dom_refs_count(cls, v):
        """Validate dim sector route dom refs count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 tuyến bay mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 tuyến bay để tạo")
        return v


class DimSectorRouteDomRefBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create DimSectorRouteDomRef API"""

    created_dim_sector_route_dom_refs: List[DimSectorRouteDomRefResponse] = Field(
        ..., description="Danh sách DimSectorRouteDomRef đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số DimSectorRouteDomRef đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
