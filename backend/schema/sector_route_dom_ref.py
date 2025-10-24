from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class SectorRouteDomRefBase(BaseModel):
    """
    Base schema cho SectorRouteDomRef

    Định nghĩa các trường cơ bản cho SectorRouteDomRef
    """

    sector: str = Field(
        ..., min_length=1, max_length=20, description="Mã sector tuyến bay"
    )
    area_lv1: str = Field(
        ..., min_length=1, max_length=100, description="Khu vực/vùng địa lý level 1"
    )
    dom_int: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Domestic (DOM) hoặc International (INT)",
    )

    @field_validator("sector")
    def validate_sector(cls, v):
        """Validate sector format"""
        v = v.upper().strip()
        if not v or len(v) == 0:
            raise ValueError("Mã sector không được để trống")
        return v

    @field_validator("area_lv1")
    def validate_area_lv1(cls, v):
        """Validate area lv1 format"""
        v = v.strip()
        if not v or len(v) == 0:
            raise ValueError("Khu vực/vùng địa lý level 1 không được để trống")
        return v

    @field_validator("dom_int")
    def validate_dom_int(cls, v):
        """Validate dom int format"""
        v = v.upper().strip()
        if not v or len(v) == 0:
            raise ValueError(
                "Domestic (DOM) hoặc International (INT) không được để trống"
            )
        if v not in ["DOM", "INT"]:
            raise ValueError("Domestic (DOM) hoặc International (INT) không hợp lệ")
        return v


class SectorRouteDomRefCreate(SectorRouteDomRefBase):
    """Schema để tạo SectorRouteDomRef"""

    pass


class SectorRouteDomRefUpdate(SectorRouteDomRefBase):
    """Schema để cập nhật SectorRouteDomRef"""

    sector: Optional[str] = Field(
        None, min_length=0, max_length=20, description="Mã sector tuyến bay"
    )
    area_lv1: Optional[str] = Field(
        None, min_length=0, max_length=100, description="Khu vực/vùng địa lý level 1"
    )
    dom_int: Optional[str] = Field(
        None,
        min_length=0,
        max_length=10,
        description="Domestic (DOM) hoặc International (INT)",
    )

    @field_validator("sector")
    def validate_sector(cls, v):
        """Validate sector format"""
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) == 0:
                raise ValueError("Mã sector không được để trống")
        return v

    @field_validator("area_lv1")
    def validate_area_lv1(cls, v):
        """Validate area lv1 format"""
        if v is not None:
            v = v.strip()
            if not v or len(v) == 0:
                raise ValueError("Khu vực/vùng địa lý level 1 không được để trống")
        return v

    @field_validator("dom_int")
    def validate_dom_int(cls, v):
        """Validate dom int format"""
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) == 0:
                raise ValueError(
                    "Domestic (DOM) hoặc International (INT) không được để trống"
                )
            if v not in ["DOM", "INT"]:
                raise ValueError("Domestic (DOM) hoặc International (INT) không hợp lệ")
        return v


class SectorRouteDomRefInDB(SectorRouteDomRefBase):
    """Schema cho SectorRouteDomRef trong database"""

    id: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class SectorRouteDomRefResponse(SectorRouteDomRefInDB):
    """Schema cho response của SectorRouteDomRef"""

    pass


class SectorRouteDomRefBulkCreate(BaseModel):
    """Schema để tạo nhiều SectorRouteDomRef cùng lúc"""

    sector_route_dom_refs: List[SectorRouteDomRefCreate] = Field(
        ..., description="Danh sách SectorRouteDomRef cần tạo"
    )

    @field_validator("sector_route_dom_refs")
    def validate_sector_route_dom_refs_count(cls, v):
        """Validate sector route dom refs count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 tuyến bay mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 tuyến bay để tạo")
        return v


class SectorRouteDomRefBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create SectorRouteDomRef API"""

    created_sector_route_dom_refs: List[SectorRouteDomRefResponse] = Field(
        ..., description="Danh sách SectorRouteDomRef đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số SectorRouteDomRef đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
