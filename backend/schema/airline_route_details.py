from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class AirlineRouteDetailsBase(BaseModel):
    """
    Base schema cho AirlineRouteDetails

    Định nghĩa các trường cơ bản cho AirlineRouteDetails
    """

    sector: str = Field(
        ..., min_length=1, max_length=20, description="Mã sector tuyến bay (VD: SGNHAN)"
    )
    distance_mile_gds: Optional[int] = Field(
        None, ge=0, description="Khoảng cách tính bằng dặm từ GDS"
    )
    distance_km_gds: Optional[float] = Field(
        None, ge=0, description="Khoảng cách tính bằng km từ GDS"
    )
    sector_2: Optional[str] = Field(
        None, max_length=20, description="Định dạng sector thay thế"
    )
    route: Optional[str] = Field(None, max_length=100, description="Mô tả tuyến bay")
    country_1: Optional[str] = Field(
        None, max_length=100, description="Quốc gia điểm khởi hành"
    )
    country_2: Optional[str] = Field(
        None, max_length=100, description="Quốc gia điểm đến"
    )
    country: Optional[str] = Field(
        None, max_length=100, description="Quốc gia chính để phân loại tuyến bay"
    )
    dom_int: Optional[str] = Field(
        None, max_length=10, description="Domestic (DOM) hoặc International (INT)"
    )
    area: Optional[str] = Field(None, max_length=100, description="Khu vực/vùng địa lý")

    @field_validator("sector")
    def validate_sector(cls, v):
        """Validate sector format"""
        v = v.upper().strip()
        if not v or len(v) == 0:
            raise ValueError("Mã sector không được để trống")
        return v

    @field_validator("dom_int")
    def validate_dom_int(cls, v):
        """Validate domestic/international flag"""
        if v is not None:
            v = v.upper().strip()
            if v and v not in ["DOM", "INT"]:
                raise ValueError("dom_int phải là 'DOM' hoặc 'INT'")
        return v


class AirlineRouteDetailsCreate(AirlineRouteDetailsBase):
    """Schema để tạo mới AirlineRouteDetails"""

    pass


class AirlineRouteDetailsUpdate(BaseModel):
    """Schema để cập nhật AirlineRouteDetails"""

    sector: Optional[str] = Field(
        None, min_length=1, max_length=20, description="Mã sector tuyến bay"
    )
    distance_mile_gds: Optional[int] = Field(
        None, ge=0, description="Khoảng cách tính bằng dặm từ GDS"
    )
    distance_km_gds: Optional[float] = Field(
        None, ge=0, description="Khoảng cách tính bằng km từ GDS"
    )
    sector_2: Optional[str] = Field(
        None, max_length=20, description="Định dạng sector thay thế"
    )
    route: Optional[str] = Field(None, max_length=100, description="Mô tả tuyến bay")
    country_1: Optional[str] = Field(
        None, max_length=100, description="Quốc gia điểm khởi hành"
    )
    country_2: Optional[str] = Field(
        None, max_length=100, description="Quốc gia điểm đến"
    )
    country: Optional[str] = Field(
        None, max_length=100, description="Quốc gia chính để phân loại tuyến bay"
    )
    dom_int: Optional[str] = Field(
        None, max_length=10, description="Domestic/International"
    )
    area: Optional[str] = Field(None, max_length=100, description="Khu vực/vùng địa lý")

    @field_validator("sector")
    def validate_sector(cls, v):
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) == 0:
                raise ValueError("Mã sector không được để trống")
        return v

    @field_validator("dom_int")
    def validate_dom_int(cls, v):
        if v is not None:
            v = v.upper().strip()
            if v and v not in ["DOM", "INT"]:
                raise ValueError("dom_int phải là 'DOM' hoặc 'INT'")
        return v


class AirlineRouteDetailsInDB(AirlineRouteDetailsBase):
    """Schema cho AirlineRouteDetails trong database"""

    index: int
    inserted_time: datetime = Field(..., description="Thời gian chèn bản ghi")
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class AirlineRouteDetailsResponse(AirlineRouteDetailsInDB):
    """Schema cho response của AirlineRouteDetails API"""

    pass


class AirlineRouteDetailsBulkCreate(BaseModel):
    """Schema để tạo nhiều AirlineRouteDetails cùng lúc"""

    route_details: List[AirlineRouteDetailsCreate] = Field(
        ...,
        description="Danh sách chi tiết tuyến bay cần tạo (tối đa 1000)",
    )

    @field_validator("route_details")
    def validate_route_details_count(cls, v):
        """Custom validation message for route details count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 chi tiết tuyến bay mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 chi tiết tuyến bay để tạo")
        return v


class AirlineRouteDetailsBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create AirlineRouteDetails API"""

    created_route_details: List[AirlineRouteDetailsResponse] = Field(
        ..., description="Danh sách chi tiết tuyến bay đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số chi tiết tuyến bay đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
