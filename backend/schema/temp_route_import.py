from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class TempRouteImportBase(BaseModel):
    """
    Base schema cho TempRouteImport

    Định nghĩa các trường cơ bản cho TempRouteImport
    """

    route: str = Field(..., min_length=1, max_length=255, description="Mã tuyến bay")
    ac: Optional[str] = Field(None, max_length=50, description="Loại máy bay")
    route_id: Optional[str] = Field(
        None, max_length=50, description="Định danh tuyến bay"
    )
    fh_theo_gio: Optional[Decimal] = Field(None, description="Giờ bay")
    flight_hour: Optional[Decimal] = Field(None, description="Thời gian bay")
    taxi: Optional[Decimal] = Field(None, description="Thời gian taxi")
    block_hour: Optional[Decimal] = Field(None, description="Thời gian block")
    distance_km: Optional[int] = Field(None, ge=0, description="Khoảng cách tính km")
    loai: Optional[str] = Field(
        None, max_length=50, description="Loại tuyến bay (Tiếng Việt)"
    )
    type: Optional[str] = Field(
        None, max_length=50, description="Loại tuyến bay (Tiếng Anh)"
    )
    country: Optional[str] = Field(
        None, max_length=100, description="Phân loại quốc gia"
    )

    @field_validator("route")
    def validate_route(cls, v):
        """Validate route code"""
        v = v.upper().strip()
        if not v or len(v) == 0:
            raise ValueError("Mã tuyến bay không được để trống")
        return v

    @field_validator("fh_theo_gio", "flight_hour", "taxi", "block_hour")
    def validate_time_fields(cls, v):
        """Validate time fields are non-negative"""
        if v is not None and v < 0:
            raise ValueError("Thời gian không được âm")
        return v

    @field_validator("distance_km")
    def validate_distance(cls, v):
        """Validate distance is non-negative"""
        if v is not None and v < 0:
            raise ValueError("Khoảng cách không được âm")
        return v


class TempRouteImportCreate(TempRouteImportBase):
    """Schema để tạo mới TempRouteImport"""

    pass


class TempRouteImportUpdate(BaseModel):
    """Schema để cập nhật TempRouteImport"""

    ac: Optional[str] = Field(None, max_length=50, description="Loại máy bay")
    route_id: Optional[str] = Field(
        None, max_length=50, description="Định danh tuyến bay"
    )
    fh_theo_gio: Optional[Decimal] = Field(None, description="Giờ bay")
    flight_hour: Optional[Decimal] = Field(None, description="Thời gian bay")
    taxi: Optional[Decimal] = Field(None, description="Thời gian taxi")
    block_hour: Optional[Decimal] = Field(None, description="Thời gian block")
    distance_km: Optional[int] = Field(None, ge=0, description="Khoảng cách tính km")
    loai: Optional[str] = Field(
        None, max_length=50, description="Loại tuyến bay (Tiếng Việt)"
    )
    type: Optional[str] = Field(
        None, max_length=50, description="Loại tuyến bay (Tiếng Anh)"
    )
    country: Optional[str] = Field(
        None, max_length=100, description="Phân loại quốc gia"
    )

    @field_validator("fh_theo_gio", "flight_hour", "taxi", "block_hour")
    def validate_time_fields(cls, v):
        if v is not None and v < 0:
            raise ValueError("Thời gian không được âm")
        return v

    @field_validator("distance_km")
    def validate_distance(cls, v):
        if v is not None and v < 0:
            raise ValueError("Khoảng cách không được âm")
        return v


class TempRouteImportInDB(TempRouteImportBase):
    """Schema cho TempRouteImport trong database"""

    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")

    class Config:
        from_attributes = True


class TempRouteImportResponse(TempRouteImportInDB):
    """Schema cho response của TempRouteImport API"""

    pass


class TempRouteImportBulkCreate(BaseModel):
    """Schema để tạo nhiều TempRouteImport cùng lúc"""

    temp_routes: List[TempRouteImportCreate] = Field(
        ...,
        description="Danh sách temp route cần tạo (tối đa 1000)",
    )

    @field_validator("temp_routes")
    def validate_temp_routes_count(cls, v):
        """Custom validation message for temp routes count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 temp route mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 temp route để tạo")
        return v


class TempRouteImportBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create TempRouteImport API"""

    created_temp_routes: List[TempRouteImportResponse] = Field(
        ..., description="Danh sách temp route đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số temp route đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
