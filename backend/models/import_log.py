from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from backend.db.database import Base


class ImportLog(Base):
    """
    Model cho Import Log - Theo dõi lịch sử import file và trạng thái

    Duy trì record của tất cả file imports với metadata

    Attributes:
        id: ID duy nhất của bản ghi
        file_name: Tên file được import
        import_date: Timestamp import
        source_type: Loại nguồn (MN, MB, MT, etc.)
        status: Trạng thái import
        row_count: Số dòng được import
        clean_data: Cờ cho dữ liệu đã được làm sạch
        created_at: Thời gian tạo bản ghi
    """

    __tablename__ = "import_log"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_name = Column(
        String(255), nullable=False, index=True, comment="Name of imported file"
    )
    import_date = Column(
        DateTime,
        default=func.getdate(),
        nullable=False,
        index=True,
        comment="Import timestamp",
    )
    source_type = Column(
        String(50), nullable=True, comment="Type of source (MN, MB, MT, etc.)"
    )
    status = Column(
        String(20), default="imported", nullable=False, comment="Import status"
    )
    row_count = Column(Integer, nullable=True, comment="Number of rows imported")
    clean_data = Column(Integer, nullable=True, comment="Flag for cleaned data")
    created_at = Column(
        DateTime, default=func.sysdatetime(), nullable=False, comment="Thời gian tạo"
    )

    def __repr__(self):
        """Represent the ImportLog model as a string"""
        return f"<ImportLog(file_name='{self.file_name}', source_type='{self.source_type}')>"

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "file_name": self.file_name,
            "import_date": self.import_date,
            "source_type": self.source_type,
            "status": self.status,
            "row_count": self.row_count,
            "clean_data": self.clean_data,
            "created_at": self.created_at,
        }
