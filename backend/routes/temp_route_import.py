from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from backend.db.database import get_db
from backend.models.temp_route_import import TempRouteImport
from backend.models.route import Route
from backend.schema.temp_route_import import (
    TempRouteImportCreate,
    TempRouteImportUpdate,
    TempRouteImportResponse,
    TempRouteImportBulkCreate,
    TempRouteImportBulkCreateResponse,
)


router = APIRouter(prefix="/temp-route-import", tags=["temp-route-import"])


@router.get("/", response_model=List[TempRouteImportResponse])
async def get_all_temp_routes(
    skip: int = 0, limit: int = None, db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả đường bay trong bảng tạm
    """

    try:
        query = db.query(TempRouteImport).order_by(TempRouteImport.route).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        temp_routes = query.all()
        return temp_routes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách đường bay: {str(e)}",
        )


# @router.get("/{route_code}", response_model=TempRouteImportResponse)
# async def get_temp_route(route_code: str, db: Session = Depends(get_db)):
#     """
#     Lấy thông tin một đường bay theo mã
#     """

#     try:
#         temp_route = (
#             db.query(TempRouteImport)
#             .filter(TempRouteImport.route == route_code.upper())
#             .first()
#         )
#         if not temp_route:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy đường bay"
#             )
#         return temp_route

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi lấy thông tin đường bay: {str(e)}",
#         )


# @router.post(
#     "/", response_model=TempRouteImportResponse, status_code=status.HTTP_201_CREATED
# )
# async def create_temp_route(
#     temp_route: TempRouteImportCreate, db: Session = Depends(get_db)
# ):
#     """
#     Tạo đường bay mới trong bảng tạm
#     """

#     try:
#         # Kiểm tra xem route đã tồn tại chưa
#         existing = (
#             db.query(TempRouteImport)
#             .filter(TempRouteImport.route == temp_route.route.upper())
#             .first()
#         )
#         if existing:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=f"Đường bay '{temp_route.route}' đã tồn tại trong bảng tạm",
#             )

#         db_temp_route = TempRouteImport(**temp_route.model_dump())
#         db.add(db_temp_route)
#         db.commit()
#         db.refresh(db_temp_route)
#         return db_temp_route

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
#             detail=f"Lỗi server khi tạo đường bay: {str(e)}",
#         )


# @router.post(
#     "/bulk-create",
#     response_model=TempRouteImportBulkCreateResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_temp_routes_bulk(
#     temp_route_bulk: TempRouteImportBulkCreate, db: Session = Depends(get_db)
# ):
#     """
#     Tạo nhiều đường bay cùng lúc trong bảng tạm

#     - Tối đa 1000 routes mỗi lần
#     - Trả về danh sách đường bay đã tạo thành công và các lỗi nếu có
#     - Sử dụng transaction để đảm bảo tính nhất quán dữ liệu
#     """

#     created_temp_routes = []
#     errors = []

#     try:
#         # Tạo từng đường bay
#         for i, temp_route_data in enumerate(temp_route_bulk.temp_routes):
#             try:
#                 # Kiểm tra trùng lặp
#                 existing = (
#                     db.query(TempRouteImport)
#                     .filter(TempRouteImport.route == temp_route_data.route.upper())
#                     .first()
#                 )
#                 if existing:
#                     errors.append(
#                         f"Đường bay thứ {i+1} ({temp_route_data.route}): Đã tồn tại"
#                     )
#                     continue

#                 db_temp_route = TempRouteImport(**temp_route_data.model_dump())
#                 db.add(db_temp_route)
#                 db.flush()  # Flush để có thông tin nhưng chưa commit
#                 created_temp_routes.append(db_temp_route)

#             except Exception as e:
#                 errors.append(
#                     f"Đường bay thứ {i+1} ({temp_route_data.route}): {str(e)}"
#                 )

#         # Commit nếu có ít nhất 1 thành công
#         if created_temp_routes:
#             db.commit()
#             # Refresh tất cả objects để có đầy đủ thông tin
#             for temp_route in created_temp_routes:
#                 db.refresh(temp_route)

#         return TempRouteImportBulkCreateResponse(
#             created_temp_routes=created_temp_routes,
#             total_created=len(created_temp_routes),
#             errors=errors,
#         )

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi tạo đường bay: {str(e)}",
#         )


# @router.put("/{route_code}", response_model=TempRouteImportResponse)
# async def update_temp_route(
#     route_code: str,
#     temp_route_update: TempRouteImportUpdate,
#     db: Session = Depends(get_db),
# ):
#     """
#     Cập nhật thông tin đường bay trong bảng tạm
#     """

#     try:
#         temp_route = (
#             db.query(TempRouteImport)
#             .filter(TempRouteImport.route == route_code.upper())
#             .first()
#         )
#         if not temp_route:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy đường bay"
#             )

#         # Cập nhật các trường được cung cấp
#         update_data = temp_route_update.model_dump(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(temp_route, field, value)

#         db.commit()
#         db.refresh(temp_route)
#         return temp_route

#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi cập nhật đường bay: {str(e)}",
#         )


# @router.delete("/{route_code}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_temp_route(route_code: str, db: Session = Depends(get_db)):
#     """
#     Xóa đường bay khỏi bảng tạm
#     """

#     try:
#         temp_route = (
#             db.query(TempRouteImport)
#             .filter(TempRouteImport.route == route_code.upper())
#             .first()
#         )
#         if not temp_route:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy đường bay"
#             )

#         db.delete(temp_route)
#         db.commit()
#         return {"message": "Đã xóa đường bay thành công"}

#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi xóa đường bay: {str(e)}",
#         )


# @router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
# async def clear_all_temp_routes(db: Session = Depends(get_db)):
#     """
#     Xóa tất cả đường bay khỏi bảng tạm
#     """

#     try:
#         db.query(TempRouteImport).delete()
#         db.commit()
#         return {"message": "Đã xóa tất cả đường bay thành công"}

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi xóa tất cả đường bay: {str(e)}",
#         )


# @router.get("/search/", response_model=List[TempRouteImportResponse])
# async def search_temp_routes(
#     q: str = None,
#     country: str = None,
#     type: str = None,
#     db: Session = Depends(get_db),
# ):
#     """
#     Tìm kiếm đường bay trong bảng tạm theo các tiêu chí
#     """

#     try:
#         query = db.query(TempRouteImport)

#         if q:
#             query = query.filter(TempRouteImport.route.contains(q.upper()))

#         if country:
#             query = query.filter(TempRouteImport.country.contains(country))

#         if type:
#             query = query.filter(TempRouteImport.type.contains(type))

#         temp_routes = query.order_by(TempRouteImport.route).all()
#         return temp_routes

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi tìm kiếm đường bay: {str(e)}",
#         )
