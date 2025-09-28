from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class MissingDimensionsLogBase(BaseModel):
    """
    Base schema cho MissingDimensionsLog

    Định nghĩa các trường cơ bản cho MissingDimensionsLog
    """

    type: Optional[str] = Field(
        None, max_length=50, description="Loại dữ liệu bị thiếu (ACTYPE/ROUTE)"
    )
    value: Optional[str] = Field(None, max_length=255, description="Giá trị bị thiếu")
    source_sheet: Optional[str] = Field(
        None, max_length=255, description="Source sheet nơi tìm thấy dữ liệu bị thiếu"
    )

    @field_validator("type")
    def validate_type(cls, v):
        """Validate type field"""
        if v is not None:
            v = v.upper().strip()
            if v and v not in ["ACTYPE", "ROUTE"]:
                raise ValueError("type phải là 'ACTYPE' hoặc 'ROUTE'")
        return v


class MissingDimensionsLogCreate(MissingDimensionsLogBase):
    """Schema để tạo mới MissingDimensionsLog"""

    pass


class MissingDimensionsLogUpdate(BaseModel):
    """Schema để cập nhật MissingDimensionsLog"""

    type: Optional[str] = Field(
        None, max_length=50, description="Loại dữ liệu bị thiếu"
    )
    value: Optional[str] = Field(None, max_length=255, description="Giá trị bị thiếu")
    source_sheet: Optional[str] = Field(
        None, max_length=255, description="Source sheet"
    )

    @field_validator("type")
    def validate_type(cls, v):
        if v is not None:
            v = v.upper().strip()
            if v and v not in ["ACTYPE", "ROUTE"]:
                raise ValueError("type phải là 'ACTYPE' hoặc 'ROUTE'")
        return v


class MissingDimensionsLogInDB(MissingDimensionsLogBase):
    """Schema cho MissingDimensionsLog trong database"""

    id: int
    created_at_log: Optional[datetime] = Field(
        None, description="Khi dữ liệu bị thiếu được ghi lại"
    )
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")

    class Config:
        from_attributes = True


class MissingDimensionsLogResponse(MissingDimensionsLogInDB):
    """Schema cho response của MissingDimensionsLog API"""

    pass


class MissingDimensionsLogBulkCreate(BaseModel):
    """Schema để tạo nhiều MissingDimensionsLog cùng lúc"""

    missing_dimensions: List[MissingDimensionsLogCreate] = Field(
        ...,
        description="Danh sách missing dimensions cần tạo (tối đa 1000)",
    )

    @field_validator("missing_dimensions")
    def validate_missing_dimensions_count(cls, v):
        """Custom validation message for missing dimensions count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 missing dimensions mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 missing dimension để tạo")
        return v


class MissingDimensionsLogBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create MissingDimensionsLog API"""

    created_missing_dimensions: List[MissingDimensionsLogResponse] = Field(
        ..., description="Danh sách missing dimensions đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số missing dimensions đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
