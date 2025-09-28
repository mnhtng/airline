from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, date


class QuaDemBase(BaseModel):
    """
    Base schema cho QuaDem

    Định nghĩa các trường cơ bản cho QuaDem
    """

    flight_date_format: Optional[date] = Field(
        None, description="Ngày chuyến bay đầu tiên"
    )
    source: Optional[str] = Field(None, max_length=500, description="Sân bay nguồn")
    sortedroute: Optional[str] = Field(
        None, max_length=20, description="Tuyến bay đã chuẩn hóa"
    )
    flight_no: Optional[str] = Field(
        None, max_length=50, description="Số hiệu chuyến bay"
    )
    flight_date_format_: Optional[date] = Field(
        None, description="Ngày chuyến bay thứ hai"
    )
    source_: Optional[str] = Field(None, max_length=500, description="Sân bay đích")
    sortedroute_: Optional[str] = Field(None, max_length=20, description="Tuyến bay về")
    flight_no_: Optional[str] = Field(
        None, max_length=50, description="Số hiệu chuyến bay về"
    )


class QuaDemCreate(QuaDemBase):
    """Schema để tạo mới QuaDem"""

    pass


class QuaDemUpdate(BaseModel):
    """Schema để cập nhật QuaDem"""

    flight_date_format: Optional[date] = Field(
        None, description="Ngày chuyến bay đầu tiên"
    )
    source: Optional[str] = Field(None, max_length=500, description="Sân bay nguồn")
    sortedroute: Optional[str] = Field(
        None, max_length=20, description="Tuyến bay đã chuẩn hóa"
    )
    flight_no: Optional[str] = Field(
        None, max_length=50, description="Số hiệu chuyến bay"
    )
    flight_date_format_: Optional[date] = Field(
        None, description="Ngày chuyến bay thứ hai"
    )
    source_: Optional[str] = Field(None, max_length=500, description="Sân bay đích")
    sortedroute_: Optional[str] = Field(None, max_length=20, description="Tuyến bay về")
    flight_no_: Optional[str] = Field(
        None, max_length=50, description="Số hiệu chuyến bay về"
    )


class QuaDemInDB(QuaDemBase):
    """Schema cho QuaDem trong database"""

    id: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")

    class Config:
        from_attributes = True


class QuaDemResponse(QuaDemInDB):
    """Schema cho response của QuaDem API"""

    pass


class QuaDemBulkCreate(BaseModel):
    """Schema để tạo nhiều QuaDem cùng lúc"""

    qua_dems: List[QuaDemCreate] = Field(
        ...,
        description="Danh sách chuyến bay qua đêm cần tạo (tối đa 1000)",
    )

    @field_validator("qua_dems")
    def validate_qua_dems_count(cls, v):
        """Custom validation message for qua dem count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 chuyến bay qua đêm mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 chuyến bay qua đêm để tạo")
        return v


class QuaDemBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create QuaDem API"""

    created_qua_dems: List[QuaDemResponse] = Field(
        ..., description="Danh sách chuyến bay qua đêm đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số chuyến bay qua đêm đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
