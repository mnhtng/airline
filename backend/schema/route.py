from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, time


class RouteBase(BaseModel):
    """
    Base schema cho Route

    Định nghĩa các trường cơ bản cho Route
    """

    route: str = Field(..., min_length=1, max_length=20, description="Mã tuyến bay")
    ac: Optional[str] = Field(
        None, max_length=20, description="Loại máy bay cho tuyến bay"
    )
    route_id: Optional[str] = Field(
        None, max_length=50, description="Định danh tuyến bay duy nhất"
    )
    flight_hour: Optional[float] = Field(
        None, ge=0, description="Thời gian bay (số thập phân)"
    )
    taxi: Optional[float] = Field(
        None, ge=0, description="Thời gian taxi tính bằng giờ"
    )
    block_hour: Optional[float] = Field(None, ge=0, description="Tổng thời gian block")
    distance_km: Optional[float] = Field(
        None, ge=0, description="Khoảng cách tính bằng kilomet"
    )
    loai: Optional[str] = Field(
        None, max_length=50, description="Loại tuyến bay tiếng Việt"
    )
    type: Optional[str] = Field(
        None, max_length=50, description="Loại tuyến bay tiếng Anh"
    )
    country: Optional[str] = Field(
        None, max_length=100, description="Phân loại quốc gia"
    )

    @field_validator("route")
    def validate_route(cls, v):
        """Validate route format"""
        v = v.upper().strip()
        if not v or len(v) == 0:
            raise ValueError("Mã tuyến bay không được để trống")
        return v


class RouteCreate(RouteBase):
    """Schema để tạo mới Route"""

    pass


class RouteUpdate(BaseModel):
    """Schema để cập nhật Route"""

    route: Optional[str] = Field(
        None, min_length=1, max_length=20, description="Mã tuyến bay"
    )
    ac: Optional[str] = Field(
        None, max_length=20, description="Loại máy bay cho tuyến bay"
    )
    route_id: Optional[str] = Field(
        None, max_length=50, description="Định danh tuyến bay duy nhất"
    )
    flight_hour: Optional[float] = Field(
        None, ge=0, description="Thời gian bay (số thập phân)"
    )
    taxi: Optional[float] = Field(
        None, ge=0, description="Thời gian taxi tính bằng giờ"
    )
    block_hour: Optional[float] = Field(None, ge=0, description="Tổng thời gian block")
    distance_km: Optional[float] = Field(
        None, ge=0, description="Khoảng cách tính bằng kilomet"
    )
    loai: Optional[str] = Field(
        None, max_length=50, description="Loại tuyến bay tiếng Việt"
    )
    type: Optional[str] = Field(
        None, max_length=50, description="Loại tuyến bay tiếng Anh"
    )
    country: Optional[str] = Field(
        None, max_length=100, description="Phân loại quốc gia"
    )

    @field_validator("route")
    def validate_route(cls, v):
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) == 0:
                raise ValueError("Mã tuyến bay không được để trống")
        return v


class RouteInDB(RouteBase):
    """Schema cho Route trong database"""

    index: int
    fh_theo_gio: Optional[str] = Field(
        None, description="Thời gian bay (định dạng time)"
    )
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class RouteResponse(RouteInDB):
    """Schema cho response của Route API"""

    pass


class RouteBulkCreate(BaseModel):
    """Schema để tạo nhiều Route cùng lúc"""

    routes: List[RouteCreate] = Field(
        ...,
        description="Danh sách tuyến bay cần tạo (tối đa 1000)",
    )

    @field_validator("routes")
    def validate_routes_count(cls, v):
        """Custom validation message for route count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 tuyến bay mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 tuyến bay để tạo")
        return v


class RouteBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create Route API"""

    created_routes: List[RouteResponse] = Field(
        ..., description="Danh sách tuyến bay đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số tuyến bay đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
