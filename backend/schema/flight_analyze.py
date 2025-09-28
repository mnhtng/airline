from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, date


class FlightAnalyzeBase(BaseModel):
    """
    Base schema cho FlightAnalyze

    Định nghĩa các trường cơ bản cho FlightAnalyze
    """

    flight_date: Optional[str] = Field(None, max_length=50, description="Ngày bay gốc")
    flight_date_format: Optional[date] = Field(
        None, description="Ngày bay đã chuẩn hóa"
    )
    flight_no: Optional[str] = Field(
        None, max_length=50, description="Số hiệu chuyến bay"
    )
    actype: Optional[str] = Field(None, max_length=50, description="Loại máy bay")
    sector: Optional[str] = Field(None, max_length=20, description="Sector tuyến bay")
    total_pax: Optional[float] = Field(None, ge=0, description="Tổng số hành khách")
    cgo: Optional[float] = Field(None, ge=0, description="Hàng hóa")
    mail: Optional[float] = Field(None, ge=0, description="Bưu kiện")
    seat: Optional[int] = Field(None, ge=0, description="Sức chứa ghế")
    departure: Optional[str] = Field(
        None, max_length=10, description="Mã sân bay khởi hành"
    )
    arrives: Optional[str] = Field(None, max_length=10, description="Mã sân bay đến")
    airlines_name: Optional[str] = Field(
        None, max_length=255, description="Tên hãng hàng không"
    )
    country: Optional[str] = Field(
        None, max_length=100, description="Quốc gia tuyến bay"
    )
    dom_int: Optional[str] = Field(
        None, max_length=10, description="Domestic/International"
    )
    com: str = Field(default="", max_length=1, description="Cờ thương mại")
    region: Optional[str] = Field(None, max_length=100, description="Khu vực địa lý")
    city_arrives: Optional[str] = Field(
        None, max_length=100, description="Thành phố đến"
    )
    country_arrives: Optional[str] = Field(
        None, max_length=100, description="Quốc gia đến"
    )
    city_departure: Optional[str] = Field(
        None, max_length=100, description="Thành phố khởi hành"
    )
    country_departure: Optional[str] = Field(
        None, max_length=100, description="Quốc gia khởi hành"
    )
    source: Optional[str] = Field(None, max_length=500, description="Nguồn dữ liệu")
    rnk_sg: int = Field(default=0, description="Xếp hạng")

    @field_validator("dom_int")
    def validate_dom_int(cls, v):
        """Validate domestic/international flag"""
        if v is not None:
            v = v.upper().strip()
            if v and v not in ["DOM", "INT"]:
                raise ValueError("dom_int phải là 'DOM' hoặc 'INT'")
        return v

    @field_validator("com")
    def validate_com(cls, v):
        """Validate commercial flag"""
        if v and v not in ["Y", "N", ""]:
            raise ValueError("com phải là 'Y', 'N' hoặc rỗng")
        return v


class FlightAnalyzeCreate(FlightAnalyzeBase):
    """Schema để tạo mới FlightAnalyze"""

    pass


class FlightAnalyzeUpdate(BaseModel):
    """Schema để cập nhật FlightAnalyze"""

    flight_date: Optional[str] = Field(None, max_length=50, description="Ngày bay gốc")
    flight_date_format: Optional[date] = Field(
        None, description="Ngày bay đã chuẩn hóa"
    )
    flight_no: Optional[str] = Field(
        None, max_length=50, description="Số hiệu chuyến bay"
    )
    actype: Optional[str] = Field(None, max_length=50, description="Loại máy bay")
    sector: Optional[str] = Field(None, max_length=20, description="Sector tuyến bay")
    total_pax: Optional[float] = Field(None, ge=0, description="Tổng số hành khách")
    cgo: Optional[float] = Field(None, ge=0, description="Hàng hóa")
    mail: Optional[float] = Field(None, ge=0, description="Bưu kiện")
    seat: Optional[int] = Field(None, ge=0, description="Sức chứa ghế")
    departure: Optional[str] = Field(
        None, max_length=10, description="Mã sân bay khởi hành"
    )
    arrives: Optional[str] = Field(None, max_length=10, description="Mã sân bay đến")
    airlines_name: Optional[str] = Field(
        None, max_length=255, description="Tên hãng hàng không"
    )
    country: Optional[str] = Field(
        None, max_length=100, description="Quốc gia tuyến bay"
    )
    dom_int: Optional[str] = Field(
        None, max_length=10, description="Domestic/International"
    )
    com: Optional[str] = Field(None, max_length=1, description="Cờ thương mại")
    region: Optional[str] = Field(None, max_length=100, description="Khu vực địa lý")
    city_arrives: Optional[str] = Field(
        None, max_length=100, description="Thành phố đến"
    )
    country_arrives: Optional[str] = Field(
        None, max_length=100, description="Quốc gia đến"
    )
    city_departure: Optional[str] = Field(
        None, max_length=100, description="Thành phố khởi hành"
    )
    country_departure: Optional[str] = Field(
        None, max_length=100, description="Quốc gia khởi hành"
    )
    source: Optional[str] = Field(None, max_length=500, description="Nguồn dữ liệu")
    rnk_sg: Optional[int] = Field(None, description="Xếp hạng")

    @field_validator("dom_int")
    def validate_dom_int(cls, v):
        if v is not None:
            v = v.upper().strip()
            if v and v not in ["DOM", "INT"]:
                raise ValueError("dom_int phải là 'DOM' hoặc 'INT'")
        return v

    @field_validator("com")
    def validate_com(cls, v):
        if v is not None and v and v not in ["Y", "N", ""]:
            raise ValueError("com phải là 'Y', 'N' hoặc rỗng")
        return v


class FlightAnalyzeInDB(FlightAnalyzeBase):
    """Schema cho FlightAnalyze trong database"""

    id: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class FlightAnalyzeResponse(FlightAnalyzeInDB):
    """Schema cho response của FlightAnalyze API"""

    pass


class FlightAnalyzeBulkCreate(BaseModel):
    """Schema để tạo nhiều FlightAnalyze cùng lúc"""

    flight_analyses: List[FlightAnalyzeCreate] = Field(
        ...,
        description="Danh sách phân tích chuyến bay cần tạo (tối đa 1000)",
    )

    @field_validator("flight_analyses")
    def validate_flight_analyses_count(cls, v):
        """Custom validation message for flight analyses count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 phân tích chuyến bay mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 phân tích chuyến bay để tạo")
        return v


class FlightAnalyzeBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create FlightAnalyze API"""

    created_flight_analyses: List[FlightAnalyzeResponse] = Field(
        ..., description="Danh sách phân tích chuyến bay đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số phân tích chuyến bay đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
