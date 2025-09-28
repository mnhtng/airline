from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class ImportLogBase(BaseModel):
    """
    Base schema cho ImportLog

    Định nghĩa các trường cơ bản cho ImportLog
    """

    file_name: str = Field(
        ..., min_length=1, max_length=255, description="Tên file được import"
    )
    source_type: Optional[str] = Field(
        None, max_length=50, description="Loại nguồn (MN, MB, MT, etc.)"
    )
    status: str = Field(
        default="imported", max_length=20, description="Trạng thái import"
    )
    row_count: Optional[int] = Field(None, ge=0, description="Số dòng được import")
    clean_data: Optional[int] = Field(
        None, description="Cờ cho dữ liệu đã được làm sạch"
    )

    @field_validator("file_name")
    def validate_file_name(cls, v):
        """Validate file name"""
        v = v.strip()
        if not v:
            raise ValueError("Tên file không được để trống")
        return v

    @field_validator("status")
    def validate_status(cls, v):
        """Validate status"""
        allowed_statuses = ["imported", "processing", "completed", "failed"]
        if v not in allowed_statuses:
            raise ValueError(f"Status phải là một trong: {', '.join(allowed_statuses)}")
        return v


class ImportLogCreate(ImportLogBase):
    """Schema để tạo mới ImportLog"""

    pass


class ImportLogUpdate(BaseModel):
    """Schema để cập nhật ImportLog"""

    file_name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Tên file"
    )
    source_type: Optional[str] = Field(None, max_length=50, description="Loại nguồn")
    status: Optional[str] = Field(None, max_length=20, description="Trạng thái import")
    row_count: Optional[int] = Field(None, ge=0, description="Số dòng được import")
    clean_data: Optional[int] = Field(
        None, description="Cờ cho dữ liệu đã được làm sạch"
    )

    @field_validator("file_name")
    def validate_file_name(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Tên file không được để trống")
        return v

    @field_validator("status")
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ["imported", "processing", "completed", "failed"]
            if v not in allowed_statuses:
                raise ValueError(
                    f"Status phải là một trong: {', '.join(allowed_statuses)}"
                )
        return v


class ImportLogInDB(ImportLogBase):
    """Schema cho ImportLog trong database"""

    id: int
    import_date: datetime = Field(..., description="Timestamp import")
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")

    class Config:
        from_attributes = True


class ImportLogResponse(ImportLogInDB):
    """Schema cho response của ImportLog API"""

    pass


class ImportLogBulkCreate(BaseModel):
    """Schema để tạo nhiều ImportLog cùng lúc"""

    import_logs: List[ImportLogCreate] = Field(
        ...,
        description="Danh sách import log cần tạo (tối đa 100)",
    )

    @field_validator("import_logs")
    def validate_import_logs_count(cls, v):
        """Custom validation message for import log count"""
        if len(v) > 100:
            raise ValueError("Chỉ được tạo tối đa 100 import log mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 import log để tạo")
        return v


class ImportLogBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create ImportLog API"""

    created_import_logs: List[ImportLogResponse] = Field(
        ..., description="Danh sách import log đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số import log đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
