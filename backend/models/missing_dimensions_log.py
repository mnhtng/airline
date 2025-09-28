from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from backend.db.database import Base


class MissingDimensionsLog(Base):
    """
    Model cho Missing Dimensions Log - Theo dõi dữ liệu reference bị thiếu

    Logs aircraft types và routes bị thiếu từ master data

    Attributes:
        id: ID duy nhất của bản ghi
        type: Loại dữ liệu bị thiếu (ACTYPE/ROUTE)
        value: Giá trị bị thiếu
        source_sheet: Source sheet nơi tìm thấy dữ liệu bị thiếu
        created_at_log: Khi dữ liệu bị thiếu được ghi lại
        created_at: Thời gian tạo bản ghi
    """

    __tablename__ = "Missing_Dimensions_Log"

    id = Column("ID", Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(
        "Type",
        String(50),
        nullable=True,
        index=True,
        comment="Type of missing data (ACTYPE/ROUTE)",
    )
    value = Column(
        "Value", String(255), nullable=True, index=True, comment="Missing value"
    )
    source_sheet = Column(
        "SourceSheet",
        String(255),
        nullable=True,
        comment="Source sheet where missing data found",
    )
    created_at_log = Column(
        "CreatedAt",
        DateTime,
        nullable=True,
        default=func.getdate(),
        comment="When missing data was logged",
    )
    created_at = Column(
        DateTime, default=func.sysdatetime(), nullable=False, comment="Thời gian tạo"
    )

    def __repr__(self):
        """Represent the MissingDimensionsLog model as a string"""
        return f"<MissingDimensionsLog(type='{self.type}', value='{self.value}', source_sheet='{self.source_sheet}')>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "type": self.type,
            "value": self.value,
            "source_sheet": self.source_sheet,
            "created_at_log": self.created_at_log,
            "created_at": self.created_at,
        }
