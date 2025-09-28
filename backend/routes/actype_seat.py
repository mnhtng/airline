from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from backend.db.database import get_db
from backend.models.actype_seat import ActypeSeat
from backend.schema.actype_seat import (
    ActypeSeatCreate,
    ActypeSeatUpdate,
    ActypeSeatResponse,
    ActypeSeatBulkCreate,
    ActypeSeatBulkCreateResponse,
)


router = APIRouter(prefix="/actype-seats", tags=["actype-seats"])


@router.get("/", response_model=List[ActypeSeatResponse])
async def get_all_actype_seats(
    skip: int = 0, limit: int = None, db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả cấu hình ghế theo loại máy bay
    """

    try:
        query = db.query(ActypeSeat).order_by(ActypeSeat.actype).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        actype_seats = query.all()
        return actype_seats

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách cấu hình ghế: {str(e)}",
        )


# @router.get("/{actype}", response_model=ActypeSeatResponse)
# async def get_actype_seat(actype: str, db: Session = Depends(get_db)):
#     """
#     Lấy thông tin cấu hình ghế theo loại máy bay
#     """

#     try:
#         actype_seat = (
#             db.query(ActypeSeat).filter(ActypeSeat.actype == actype.upper()).first()
#         )
#         if not actype_seat:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Không tìm thấy cấu hình ghế cho aircraft type '{actype}'",
#             )
#         return actype_seat

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi lấy thông tin cấu hình ghế: {str(e)}",
#         )


# @router.post(
#     "/", response_model=ActypeSeatResponse, status_code=status.HTTP_201_CREATED
# )
# async def create_actype_seat(
#     actype_seat: ActypeSeatCreate, db: Session = Depends(get_db)
# ):
#     """
#     Tạo cấu hình ghế mới cho loại máy bay
#     """

#     try:
#         # Kiểm tra xem actype đã tồn tại chưa
#         existing = (
#             db.query(ActypeSeat)
#             .filter(ActypeSeat.actype == actype_seat.actype.upper())
#             .first()
#         )
#         if existing:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=f"Aircraft type '{actype_seat.actype}' đã tồn tại",
#             )

#         db_actype_seat = ActypeSeat(**actype_seat.model_dump())
#         db.add(db_actype_seat)
#         db.commit()
#         db.refresh(db_actype_seat)
#         return db_actype_seat

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
#             detail=f"Lỗi server khi tạo cấu hình ghế: {str(e)}",
#         )


@router.post(
    "/bulk-create",
    response_model=ActypeSeatBulkCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_actype_seats_bulk(
    actype_seat_bulk: ActypeSeatBulkCreate, db: Session = Depends(get_db)
):
    """
    Tạo nhiều cấu hình ghế cùng lúc

    - Tối đa 1000 cấu hình ghế mỗi lần
    - Trả về danh sách cấu hình ghế đã tạo thành công và các lỗi nếu có
    - Sử dụng transaction để đảm bảo tính nhất quán dữ liệu
    """

    if len(actype_seat_bulk.actype_seats) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ được tạo tối đa 1000 cấu hình ghế mỗi lần",
        )

    created_actype_seats = []
    errors = []

    try:
        # Tạo từng cấu hình ghế
        for i, actype_seat_data in enumerate(actype_seat_bulk.actype_seats):
            try:
                db_actype_seat = ActypeSeat(**actype_seat_data.model_dump())
                db.add(db_actype_seat)
                db.flush()  # Flush để có id nhưng chưa commit
                created_actype_seats.append(db_actype_seat)

            except Exception as e:
                errors.append(
                    f"Cấu hình ghế thứ {i+1} ({actype_seat_data.actype}): {str(e)}"
                )

        # Nếu có lỗi, rollback tất cả
        if errors:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Có lỗi xảy ra khi tạo cấu hình ghế",
                    "errors": errors,
                    "created_count": 0,
                },
            )

        # Commit nếu tất cả đều thành công
        db.commit()

        # Refresh tất cả objects để có đầy đủ thông tin
        for actype_seat in created_actype_seats:
            db.refresh(actype_seat)

        return ActypeSeatBulkCreateResponse(
            created_actype_seats=created_actype_seats,
            total_created=len(created_actype_seats),
            errors=[],
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tạo cấu hình ghế: {str(e)}",
        )


# @router.put("/{actype}", response_model=ActypeSeatResponse)
# async def update_actype_seat(
#     actype: str, actype_seat_update: ActypeSeatUpdate, db: Session = Depends(get_db)
# ):
#     """
#     Cập nhật cấu hình ghế cho loại máy bay
#     """

#     try:
#         actype_seat = (
#             db.query(ActypeSeat).filter(ActypeSeat.actype == actype.upper()).first()
#         )
#         if not actype_seat:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Không tìm thấy cấu hình ghế cho aircraft type '{actype}'",
#             )

#         # Cập nhật các trường được cung cấp
#         update_data = actype_seat_update.model_dump(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(actype_seat, field, value)

#         db.commit()
#         db.refresh(actype_seat)
#         return actype_seat

#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi cập nhật cấu hình ghế: {str(e)}",
#         )


# @router.delete("/{actype}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_actype_seat(actype: str, db: Session = Depends(get_db)):
#     """
#     Xóa cấu hình ghế cho loại máy bay
#     """

#     try:
#         actype_seat = (
#             db.query(ActypeSeat).filter(ActypeSeat.actype == actype.upper()).first()
#         )
#         if not actype_seat:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Không tìm thấy cấu hình ghế cho aircraft type '{actype}'",
#             )

#         db.delete(actype_seat)
#         db.commit()
#         return {
#             "message": f"Đã xóa cấu hình ghế cho aircraft type '{actype}' thành công"
#         }

#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi xóa cấu hình ghế: {str(e)}",
#         )


# @router.get("/search/", response_model=List[ActypeSeatResponse])
# async def search_actype_seats(
#     q: str = None,
#     min_seat: int = None,
#     max_seat: int = None,
#     db: Session = Depends(get_db),
# ):
#     """
#     Tìm kiếm cấu hình ghế theo các tiêu chí
#     """

#     try:
#         query = db.query(ActypeSeat)

#         if q:
#             query = query.filter(ActypeSeat.actype.contains(q.upper()))

#         if min_seat is not None:
#             query = query.filter(ActypeSeat.seat >= min_seat)

#         if max_seat is not None:
#             query = query.filter(ActypeSeat.seat <= max_seat)

#         actype_seats = query.order_by(ActypeSeat.actype).all()
#         return actype_seats

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi tìm kiếm cấu hình ghế: {str(e)}",
#         )


@router.get("/stats/summary", response_model=dict)
async def get_actype_seat_stats(db: Session = Depends(get_db)):
    """
    Thống kê tổng quan về cấu hình ghế
    """

    try:
        from sqlalchemy import func

        total_count = db.query(ActypeSeat).count()

        if total_count == 0:
            return {
                "total_aircraft_types": 0,
                "average_seat_capacity": 0,
                "min_seat_capacity": 0,
                "max_seat_capacity": 0,
                "most_common_capacity": None,
            }

        # Thống kê cơ bản
        stats = db.query(
            func.avg(ActypeSeat.seat).label("avg_seat"),
            func.min(ActypeSeat.seat).label("min_seat"),
            func.max(ActypeSeat.seat).label("max_seat"),
        ).first()

        # Tìm seat capacity phổ biến nhất
        most_common = (
            db.query(ActypeSeat.seat, func.count(ActypeSeat.seat).label("count"))
            .group_by(ActypeSeat.seat)
            .order_by(func.count(ActypeSeat.seat).desc())
            .first()
        )

        return {
            "total_aircraft_types": total_count,
            "average_seat_capacity": (
                round(float(stats.avg_seat), 2) if stats.avg_seat else 0
            ),
            "min_seat_capacity": stats.min_seat,
            "max_seat_capacity": stats.max_seat,
            "most_common_capacity": (
                {"seat_count": most_common.seat, "aircraft_types": most_common.count}
                if most_common
                else None
            ),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi thống kê cấu hình ghế: {str(e)}",
        )
