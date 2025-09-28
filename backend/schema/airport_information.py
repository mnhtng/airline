from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class AirportInformationBase(BaseModel):
    """
    Base schema cho AirportInformation

    Định nghĩa các trường cơ bản cho AirportInformation
    """

    iata_code: str = Field(
        ..., min_length=3, max_length=3, description="Mã IATA 3 ký tự (VD: SGN, HAN)"
    )
    airport_name: Optional[str] = Field(
        None, max_length=255, description="Tên đầy đủ của sân bay"
    )
    city: Optional[str] = Field(
        None, max_length=100, description="Thành phố nơi sân bay được đặt"
    )
    country: Optional[str] = Field(
        None, max_length=100, description="Quốc gia nơi sân bay được đặt"
    )

    @field_validator("iata_code")
    def validate_iata_code(cls, v):
        """Validate IATA code format"""
        v = v.upper().strip()
        if not v or len(v) != 3:
            raise ValueError("Mã IATA phải có đúng 3 ký tự")
        if not v.isalpha():
            raise ValueError("Mã IATA chỉ được chứa ký tự chữ cái")
        return v


class AirportInformationCreate(AirportInformationBase):
    """Schema để tạo mới AirportInformation"""

    pass


class AirportInformationUpdate(BaseModel):
    """Schema để cập nhật AirportInformation"""

    iata_code: Optional[str] = Field(
        None, min_length=3, max_length=3, description="Mã IATA 3 ký tự"
    )
    airport_name: Optional[str] = Field(None, max_length=255, description="Tên sân bay")
    city: Optional[str] = Field(None, max_length=100, description="Thành phố")
    country: Optional[str] = Field(None, max_length=100, description="Quốc gia")

    @field_validator("iata_code")
    def validate_iata_code(cls, v):
        if v is not None:
            v = v.upper().strip()
            if not v or len(v) != 3:
                raise ValueError("Mã IATA phải có đúng 3 ký tự")
            if not v.isalpha():
                raise ValueError("Mã IATA chỉ được chứa ký tự chữ cái")
        return v


class AirportInformationInDB(AirportInformationBase):
    """Schema cho AirportInformation trong database"""

    index: int
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    class Config:
        from_attributes = True


class AirportInformationResponse(AirportInformationInDB):
    """Schema cho response của AirportInformation API"""

    pass


class AirportInformationBulkCreate(BaseModel):
    """Schema để tạo nhiều AirportInformation cùng lúc"""

    airports: List[AirportInformationCreate] = Field(
        ...,
        description="Danh sách sân bay cần tạo (tối đa 1000)",
    )

    @field_validator("airports")
    def validate_airports_count(cls, v):
        """Custom validation message for airport count"""
        if len(v) > 1000:
            raise ValueError("Chỉ được tạo tối đa 1000 sân bay mỗi lần")
        if len(v) < 1:
            raise ValueError("Cần ít nhất 1 sân bay để tạo")
        return v


class AirportInformationBulkCreateResponse(BaseModel):
    """Schema cho response của bulk create AirportInformation API"""

    created_airports: List[AirportInformationResponse] = Field(
        ..., description="Danh sách sân bay đã tạo thành công"
    )
    total_created: int = Field(..., description="Tổng số sân bay đã tạo")
    errors: List[str] = Field(default_factory=list, description="Danh sách lỗi nếu có")
