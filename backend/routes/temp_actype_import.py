from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from backend.db.database import get_db
from backend.models.temp_actype_import import TempActypeImport
from backend.models.actype_seat import ActypeSeat
from backend.schema.temp_actype_import import (
    TempActypeImportCreate,
    TempActypeImportUpdate,
    TempActypeImportResponse,
    TempActypeImportBulkCreate,
    TempActypeImportBulkCreateResponse,
)


router = APIRouter(prefix="/temp-actype-import", tags=["temp-actype-import"])


@router.get("/", response_model=List[TempActypeImportResponse])
async def get_all_temp_actypes(
    skip: int = 0, limit: int = None, db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả loại máy bay trong bảng tạm
    """

    try:
        query = (
            db.query(TempActypeImport).order_by(TempActypeImport.actype).offset(skip)
        )
        if limit is not None:
            query = query.limit(limit)
        temp_actypes = query.all()
        return temp_actypes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách loại máy bay: {str(e)}",
        )


# @router.get("/{actype}", response_model=TempActypeImportResponse)
# async def get_temp_actype(actype: str, db: Session = Depends(get_db)):
#     """
#     Lấy thông tin một loại máy bay theo mã
#     """

#     try:
#         temp_actype = (
#             db.query(TempActypeImport)
#             .filter(TempActypeImport.actype == actype.upper())
#             .first()
#         )
#         if not temp_actype:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Không tìm thấy loại máy bay",
#             )
#         return temp_actype

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi lấy thông tin loại máy bay: {str(e)}",
#         )


# @router.post(
#     "/", response_model=TempActypeImportResponse, status_code=status.HTTP_201_CREATED
# )
# async def create_temp_actype(
#     temp_actype: TempActypeImportCreate, db: Session = Depends(get_db)
# ):
#     """
#     Tạo loại máy bay mới trong bảng tạm
#     """

#     try:
#         # Kiểm tra xem actype đã tồn tại chưa
#         existing = (
#             db.query(TempActypeImport)
#             .filter(TempActypeImport.actype == temp_actype.actype.upper())
#             .first()
#         )
#         if existing:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=f"Loại máy bay '{temp_actype.actype}' đã tồn tại trong bảng tạm",
#             )

#         db_temp_actype = TempActypeImport(**temp_actype.model_dump())
#         db.add(db_temp_actype)
#         db.commit()
#         db.refresh(db_temp_actype)
#         return db_temp_actype

#     except HTTPException:
#         raise
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Dữ liệu không hợp lệ hoặc đã tồn tại",
#         )
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi tạo loại máy bay: {str(e)}",
#         )


# @router.post(
#     "/bulk-create",
#     response_model=TempActypeImportBulkCreateResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_temp_actypes_bulk(
#     temp_actype_bulk: TempActypeImportBulkCreate, db: Session = Depends(get_db)
# ):
#     """
#     Tạo nhiều loại máy bay cùng lúc trong bảng tạm

#     - Tối đa 1000 aircraft types mỗi lần
#     - Trả về danh sách loại máy bay đã tạo thành công và các lỗi nếu có
#     - Sử dụng transaction để đảm bảo tính nhất quán dữ liệu
#     """

#     created_temp_actypes = []
#     errors = []

#     try:
#         # Tạo từng loại máy bay
#         for i, temp_actype_data in enumerate(temp_actype_bulk.temp_actypes):
#             try:
#                 # Kiểm tra trùng lặp
#                 existing = (
#                     db.query(TempActypeImport)
#                     .filter(TempActypeImport.actype == temp_actype_data.actype.upper())
#                     .first()
#                 )
#                 if existing:
#                     errors.append(
#                         f"Loại máy bay thứ {i+1} ({temp_actype_data.actype}): Đã tồn tại"
#                     )
#                     continue

#                 db_temp_actype = TempActypeImport(**temp_actype_data.model_dump())
#                 db.add(db_temp_actype)
#                 db.flush()  # Flush để có thông tin nhưng chưa commit
#                 created_temp_actypes.append(db_temp_actype)

#             except Exception as e:
#                 errors.append(
#                     f"Loại máy bay thứ {i+1} ({temp_actype_data.actype}): {str(e)}"
#                 )

#         # Commit nếu có ít nhất 1 thành công
#         if created_temp_actypes:
#             db.commit()
#             # Refresh tất cả objects để có đầy đủ thông tin
#             for temp_actype in created_temp_actypes:
#                 db.refresh(temp_actype)

#         return TempActypeImportBulkCreateResponse(
#             created_temp_actypes=created_temp_actypes,
#             total_created=len(created_temp_actypes),
#             errors=errors,
#         )

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi tạo loại máy bay: {str(e)}",
#         )


# @router.put("/{actype}", response_model=TempActypeImportResponse)
# async def update_temp_actype(
#     actype: str,
#     temp_actype_update: TempActypeImportUpdate,
#     db: Session = Depends(get_db),
# ):
#     """
#     Cập nhật thông tin loại máy bay trong bảng tạm
#     """

#     try:
#         temp_actype = (
#             db.query(TempActypeImport)
#             .filter(TempActypeImport.actype == actype.upper())
#             .first()
#         )
#         if not temp_actype:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Không tìm thấy loại máy bay",
#             )

#         # Cập nhật các trường được cung cấp
#         update_data = temp_actype_update.model_dump(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(temp_actype, field, value)

#         db.commit()
#         db.refresh(temp_actype)
#         return temp_actype

#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi cập nhật loại máy bay: {str(e)}",
#         )


# @router.delete("/{actype}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_temp_actype(actype: str, db: Session = Depends(get_db)):
#     """
#     Xóa loại máy bay khỏi bảng tạm
#     """

#     try:
#         temp_actype = (
#             db.query(TempActypeImport)
#             .filter(TempActypeImport.actype == actype.upper())
#             .first()
#         )
#         if not temp_actype:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Không tìm thấy loại máy bay",
#             )

#         db.delete(temp_actype)
#         db.commit()
#         return {"message": "Đã xóa loại máy bay thành công"}

#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi xóa loại máy bay: {str(e)}",
#         )


# @router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
# async def clear_all_temp_actypes(db: Session = Depends(get_db)):
#     """
#     Xóa tất cả loại máy bay khỏi bảng tạm
#     """

#     try:
#         db.query(TempActypeImport).delete()
#         db.commit()
#         return {"message": "Đã xóa tất cả loại máy bay thành công"}

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi xóa tất cả loại máy bay: {str(e)}",
#         )


# @router.get("/search/", response_model=List[TempActypeImportResponse])
# async def search_temp_actypes(
#     q: str = None,
#     db: Session = Depends(get_db),
# ):
#     """
#     Tìm kiếm loại máy bay trong bảng tạm theo mã máy bay
#     """

#     try:
#         query = db.query(TempActypeImport)
#         if q:
#             query = query.filter(TempActypeImport.actype.contains(q.upper()))
#         temp_actypes = query.all()
#         return temp_actypes

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi tìm kiếm loại máy bay: {str(e)}",
#         )


@router.post("/seed", response_model=dict)
async def seed_temp_actypes(db: Session = Depends(get_db)):
    """
    Thêm dữ liệu mẫu vào bảng temp_actypes
    """

    try:
        # Dữ liệu mẫu từ SQL file
        sample_data = [
            "THD",
            "HPH",
            "HAN",
            "VDO",
            "VDH",
            "VII",
            "DIN",
        ]

        created_count = 0
        for actype in sample_data:
            # Kiểm tra xem đã tồn tại chưa
            existing = (
                db.query(TempActypeImport)
                .filter(TempActypeImport.actype == actype)
                .first()
            )
            if not existing:
                new_draft = TempActypeImport(actype=actype, seat=None)
                db.add(new_draft)
                created_count += 1

        db.commit()

        return {
            "message": f"Đã tạo {created_count} bản ghi temp_actypes mới",
            "total_added": created_count,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi thêm dữ liệu mẫu vào bảng temp_actypes: {str(e)}",
        )
