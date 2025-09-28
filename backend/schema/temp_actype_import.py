from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class TempActypeImportBase(BaseModel):
    """
    Base schema cho TempActypeImport

    Định nghĩa các trường cơ bản cho TempActypeImport
    """

    actype: str = Field(
        ..., min_length=1, max_length=255, description="Mã loại máy bay"
    )
    seat: Optional[int] = Field(None, ge=0, description="Sức chứa ghế")

    @field_validator("actype")
    def validate_actype(cls, v):
        """Validate aircraft type"""
        v = v.upper().strip()
        if not v or len(v) == 0:
            raise ValueError("Mã loại máy bay không được để trống")
        return v

    @field_validator("seat")
    def validate_seat(cls, v):
        """Validate seat count"""
        if v is not None:
            if v < 0:
                raise ValueError("Số ghế không được âm")
            if v > 1000:
                raise ValueError("Số ghế không được vượt quá 1000")
        return v


class TempActypeImportCreate(TempActypeImportBase):
    """Schema để tạo mới TempActypeImport"""

    pass


class TempActypeImportUpdate(BaseModel):
    """Schema để cập nhật TempActypeImport"""

    seat: Optional[int] = Field(None, ge=0, description="Sức chứa ghế")

    @field_validator("seat")
    def validate_seat(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Số ghế không được âm")
            if v > 1000:
                raise ValueError("Số ghế không được vượt quá 1000")
        return v


class TempActypeImportInDB(TempActypeImportBase):
    """Schema cho TempActypeImport trong database"""

    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")

    class Config:
        from_attributes = True


class TempActypeImportResponse(TempActypeImportInDB):
    """Schema cho response của TempActypeImport API"""

    pass


class TempActypeImportBulkCreate(BaseModel):
    """Schema để tạo nhiều TempActypeImport cùng lúc"""

    temp_actypes: List[TempActypeImportCreate] = Field(
        ...,
        description="Danh sách temp actype cần tạo (tối đa 1000)",
    )

    @field_validator("temp_actypes")
    def validate_temp_actypes_count(cls, v):
        """Custom validation message for temp actypes count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 temp actype mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 temp actype để tạo")
        return v


class TempActypeImportBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create TempActypeImport API"""

    created_temp_actypes: List[TempActypeImportResponse] = Field(
        ..., description="Danh sách temp actype đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số temp actype đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
