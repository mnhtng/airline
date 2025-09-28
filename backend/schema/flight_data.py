from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, date


class FlightRawBase(BaseModel):
    """
    Base schema cho FlightRaw

    Định nghĩa các trường cơ bản cho FlightRaw
    """

    flightdate: Optional[str] = Field(
        None, max_length=255, description="Ngày bay (các định dạng khác nhau từ Excel)"
    )
    flightno: Optional[str] = Field(
        None, max_length=50, description="Số hiệu chuyến bay"
    )
    route: Optional[str] = Field(
        None, max_length=100, description="Tuyến bay (VD: SGN-HAN)"
    )
    actype: Optional[str] = Field(None, max_length=50, description="Loại máy bay")
    seat: Optional[int] = Field(None, ge=0, description="Sức chứa ghế")
    adl: Optional[float] = Field(None, ge=0, description="Số hành khách người lớn")
    chd: Optional[float] = Field(None, ge=0, description="Số hành khách trẻ em")
    cgo: Optional[float] = Field(None, ge=0, description="Khối lượng hàng hóa")
    mail: Optional[float] = Field(None, ge=0, description="Khối lượng bưu kiện")
    totalpax: Optional[float] = Field(
        None, ge=0, description="Tổng số hành khách (được tính)"
    )
    source: Optional[str] = Field(None, max_length=500, description="Tên file nguồn")
    acregno: Optional[str] = Field(
        None, max_length=50, description="Số đăng ký máy bay"
    )
    sheet_name: Optional[str] = Field(
        None, max_length=255, description="Tên sheet Excel"
    )
    int_dom: Optional[str] = Field(
        None, max_length=10, description="Cờ Domestic/International"
    )

    @field_validator("int_dom")
    def validate_int_dom(cls, v):
        """Validate domestic/international flag"""
        if v is not None:
            v = v.upper().strip()
            if v and v not in ["DOM", "INT"]:
                raise ValueError("int_dom phải là 'DOM' hoặc 'INT'")
        return v


class FlightRawCreate(FlightRawBase):
    """Schema để tạo mới FlightRaw"""

    pass


class FlightRawUpdate(BaseModel):
    """Schema để cập nhật FlightRaw"""

    flightdate: Optional[str] = Field(None, max_length=255, description="Ngày bay")
    flightno: Optional[str] = Field(
        None, max_length=50, description="Số hiệu chuyến bay"
    )
    route: Optional[str] = Field(None, max_length=100, description="Tuyến bay")
    actype: Optional[str] = Field(None, max_length=50, description="Loại máy bay")
    seat: Optional[int] = Field(None, ge=0, description="Sức chứa ghế")
    adl: Optional[float] = Field(None, ge=0, description="Số hành khách người lớn")
    chd: Optional[float] = Field(None, ge=0, description="Số hành khách trẻ em")
    cgo: Optional[float] = Field(None, ge=0, description="Khối lượng hàng hóa")
    mail: Optional[float] = Field(None, ge=0, description="Khối lượng bưu kiện")
    totalpax: Optional[float] = Field(None, ge=0, description="Tổng số hành khách")
    source: Optional[str] = Field(None, max_length=500, description="Tên file nguồn")
    acregno: Optional[str] = Field(
        None, max_length=50, description="Số đăng ký máy bay"
    )
    sheet_name: Optional[str] = Field(
        None, max_length=255, description="Tên sheet Excel"
    )
    int_dom: Optional[str] = Field(
        None, max_length=10, description="Domestic/International"
    )


class FlightRawInDB(FlightRawBase):
    """Schema cho FlightRaw trong database"""

    id: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")

    class Config:
        from_attributes = True


class FlightRawResponse(FlightRawInDB):
    """Schema cho response của FlightRaw API"""

    pass


class FlightDataChotBase(BaseModel):
    """
    Base schema cho FlightDataChot

    Định nghĩa các trường cơ bản cho FlightDataChot
    """

    convert_date: Optional[int] = Field(
        None, description="Ngày bay ở định dạng YYYYMMDD"
    )
    flightno: Optional[str] = Field(
        None, max_length=50, description="Số hiệu chuyến bay"
    )
    route: Optional[str] = Field(None, max_length=100, description="Tuyến bay")
    actype: Optional[str] = Field(None, max_length=50, description="Loại máy bay")
    totalpax: Optional[float] = Field(None, ge=0, description="Tổng số hành khách")
    cgo: Optional[float] = Field(None, ge=0, description="Khối lượng hàng hóa")
    mail: Optional[float] = Field(None, ge=0, description="Khối lượng bưu kiện")
    acregno: Optional[str] = Field(
        None, max_length=50, description="Số đăng ký máy bay"
    )
    source: Optional[str] = Field(None, max_length=500, description="File nguồn")
    sheet_name: Optional[str] = Field(None, max_length=255, description="Sheet nguồn")
    region_type: int = Field(default=0, description="Phân loại khu vực")
    seat: Optional[int] = Field(None, ge=0, description="Sức chứa ghế")
    week_number: Optional[int] = Field(None, description="Số tuần")
    year_number: Optional[int] = Field(None, description="Năm")
    note: Optional[str] = Field(None, max_length=255, description="Ghi chú")
    type_filter: Optional[int] = Field(None, description="Bộ lọc loại chuyến bay")
    int_dom_: Optional[str] = Field(
        None, max_length=10, description="Domestic/International"
    )

    @field_validator("int_dom_")
    def validate_int_dom_(cls, v):
        """Validate domestic/international flag"""
        if v is not None:
            v = v.upper().strip()
            if v and v not in ["DOM", "INT"]:
                raise ValueError("int_dom_ phải là 'DOM' hoặc 'INT'")
        return v


class FlightDataChotCreate(FlightDataChotBase):
    """Schema để tạo mới FlightDataChot"""

    pass


class FlightDataChotInDB(FlightDataChotBase):
    """Schema cho FlightDataChot trong database"""

    id: int
    inserted_time: datetime = Field(..., description="Thời gian chèn")
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class FlightDataChotResponse(FlightDataChotInDB):
    """Schema cho response của FlightDataChot API"""

    pass


class FlightBulkCreate(BaseModel):
    """Schema để tạo nhiều FlightRaw cùng lúc"""

    flights: List[FlightRawCreate] = Field(
        ...,
        description="Danh sách chuyến bay cần tạo (tối đa 1000)",
    )

    @field_validator("flights")
    def validate_flights_count(cls, v):
        """Custom validation message for flight count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 chuyến bay mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 chuyến bay để tạo")
        return v


class FlightBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create Flight API"""

    created_flights: List[FlightRawResponse] = Field(
        ..., description="Danh sách chuyến bay đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số chuyến bay đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")


class ExcelProcessRequest(BaseModel):
    """Schema cho request xử lý Excel data"""

    filename: str = Field(..., description="Tên file Excel")
    data: List[dict] = Field(..., description="Dữ liệu Excel dạng list of dict")


class ExcelProcessResponse(BaseModel):
    """Schema cho response xử lý Excel data"""

    success: bool = Field(..., description="Trạng thái xử lý thành công hay không")
    message: str = Field(..., description="Thông báo kết quả")
    processed_count: int = Field(..., description="Số bản ghi đã xử lý")
    duplicates_count: Optional[int] = Field(
        default=0, description="Số bản ghi trùng lặp"
    )
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")


class MissingDimensionResponse(BaseModel):
    """Schema cho response missing dimension data"""

    id: int = Field(..., description="ID của missing dimension")
    type: Optional[str] = Field(
        None, description="Loại dữ liệu bị thiếu (ACTYPE/ROUTE)"
    )
    value: Optional[str] = Field(None, description="Giá trị bị thiếu")
    source_sheet: Optional[str] = Field(
        None, description="Source sheet nơi tìm thấy dữ liệu bị thiếu"
    )
    created_at_log: Optional[datetime] = Field(
        None, description="Khi dữ liệu bị thiếu được ghi lại"
    )
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")

    class Config:
        from_attributes = True


class DataProcessingStats(BaseModel):
    """Schema cho thống kê xử lý dữ liệu"""

    total_flights: int = Field(..., description="Tổng số chuyến bay")
    missing_actypes: int = Field(..., description="Số aircraft type bị thiếu")
    missing_routes: int = Field(..., description="Số route bị thiếu")
    latest_import: Optional[datetime] = Field(None, description="Lần import gần nhất")
    file_count: int = Field(..., description="Số file đã import")
