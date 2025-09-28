from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from backend.db.database import get_db
from backend.models.route import Route
from backend.schema.route import (
    RouteCreate,
    RouteUpdate,
    RouteResponse,
    RouteBulkCreate,
    RouteBulkCreateResponse,
)


router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("/", response_model=List[RouteResponse])
async def get_all_routes(
    skip: int = 0,
    limit: int = None,
    country: Optional[str] = None,
    route_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Lấy danh sách tất cả đường bay với filter tùy chọn
    """

    try:
        query = db.query(Route).order_by(Route.route).offset(skip)

        # Apply filters
        if country:
            query = query.filter(Route.country.ilike(f"%{country}%"))
        if route_type:
            query = query.filter(Route.type.ilike(f"%{route_type}%"))

        if limit is not None:
            query = query.limit(limit)

        routes = query.all()
        return routes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách đường bay: {str(e)}",
        )


# @router.get("/{route_code}", response_model=RouteResponse)
# async def get_route(route_code: str, db: Session = Depends(get_db)):
#     """
#     Lấy thông tin chi tiết đường bay theo mã
#     """

#     try:
#         route = db.query(Route).filter(Route.route == route_code.upper()).first()
#         if not route:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Không tìm thấy đường bay '{route_code}'",
#             )
#         return route

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi lấy thông tin đường bay: {str(e)}",
#         )


# @router.post("/", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
# async def create_route(route: RouteCreate, db: Session = Depends(get_db)):
#     """
#     Tạo đường bay mới
#     """

#     try:
#         # Kiểm tra xem route đã tồn tại chưa
#         existing = db.query(Route).filter(Route.route == route.route.upper()).first()
#         if existing:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=f"Đường bay '{route.route}' đã tồn tại",
#             )

#         db_route = Route(**route.model_dump())
#         db.add(db_route)
#         db.commit()
#         db.refresh(db_route)
#         return db_route

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


@router.post(
    "/bulk-create",
    response_model=RouteBulkCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_routes_bulk(
    route_bulk: RouteBulkCreate, db: Session = Depends(get_db)
):
    """
    Tạo nhiều đường bay cùng lúc

    - Tối đa 1000 routes mỗi lần
    - Trả về danh sách routes đã tạo thành công và các lỗi nếu có
    - Sử dụng transaction để đảm bảo tính nhất quán dữ liệu
    """

    if len(route_bulk.routes) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ được tạo tối đa 1000 đường bay mỗi lần",
        )

    created_routes = []
    errors = []

    try:
        # Tạo từng đường bay
        for idx, route_data in enumerate(route_bulk.routes):
            try:
                db_route = Route(**route_data.model_dump())
                db.add(db_route)
                db.flush()  # Sử dụng flush để lấy ID ngay lập tức
                created_routes.append(db_route)

            except Exception as e:
                errors.append(f"Đường bay thứ {idx+1} ({route_data.route}): {str(e)}")

        # Nếu có lỗi, rollback tất cả
        if errors:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Có lỗi xảy ra khi tạo đường bay",
                    "errors": errors,
                    "created_count": 0,
                },
            )

        # Commit nếu tất cả đều thành công
        db.commit()

        # Refresh tất cả objects để có đầy đủ thông tin
        for route in created_routes:
            db.refresh(route)

        return RouteBulkCreateResponse(
            created_routes=created_routes,
            total_created=len(created_routes),
            errors=[],
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tạo đường bay: {str(e)}",
        )


# @router.put("/{route_code}", response_model=RouteResponse)
# async def update_route(
#     route_code: str, route_update: RouteUpdate, db: Session = Depends(get_db)
# ):
#     """
#     Cập nhật thông tin đường bay
#     """

#     try:
#         route = db.query(Route).filter(Route.route == route_code.upper()).first()
#         if not route:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Không tìm thấy đường bay '{route_code}'",
#             )

#         # Cập nhật các trường được cung cấp
#         update_data = route_update.model_dump(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(route, field, value)

#         db.commit()
#         db.refresh(route)
#         return route

#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi cập nhật đường bay: {str(e)}",
#         )


# @router.delete("/{route_code}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_route(route_code: str, db: Session = Depends(get_db)):
#     """
#     Xóa đường bay
#     """

#     try:
#         route = db.query(Route).filter(Route.route == route_code.upper()).first()
#         if not route:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Không tìm thấy đường bay '{route_code}'",
#             )

#         db.delete(route)
#         db.commit()
#         return {"message": f"Đã xóa đường bay '{route_code}' thành công"}

#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi xóa đường bay: {str(e)}",
#         )


# @router.get("/search/", response_model=List[RouteResponse])
# async def search_routes(
#     q: str = None,
#     country: str = None,
#     route_type: str = None,
#     ac: str = None,
#     min_distance: float = None,
#     max_distance: float = None,
#     min_flight_hour: float = None,
#     max_flight_hour: float = None,
#     db: Session = Depends(get_db),
# ):
#     """
#     Tìm kiếm đường bay theo các tiêu chí chi tiết
#     """

#     try:
#         query = db.query(Route)

#         if q:
#             query = query.filter(Route.route.contains(q.upper()))

#         if country:
#             query = query.filter(Route.country.ilike(f"%{country}%"))

#         if route_type:
#             query = query.filter(Route.type.ilike(f"%{route_type}%"))

#         if ac:
#             query = query.filter(Route.ac.ilike(f"%{ac}%"))

#         if min_distance is not None:
#             query = query.filter(Route.distance_km >= min_distance)

#         if max_distance is not None:
#             query = query.filter(Route.distance_km <= max_distance)

#         if min_flight_hour is not None:
#             query = query.filter(Route.flight_hour >= min_flight_hour)

#         if max_flight_hour is not None:
#             query = query.filter(Route.flight_hour <= max_flight_hour)

#         routes = query.order_by(Route.route).all()
#         return routes

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Lỗi server khi tìm kiếm đường bay: {str(e)}",
#         )


@router.get("/stats/summary", response_model=dict)
async def get_route_stats(db: Session = Depends(get_db)):
    """
    Thống kê tổng quan về đường bay
    """

    try:
        from sqlalchemy import func

        total_count = db.query(Route).count()

        if total_count == 0:
            return {
                "total_routes": 0,
                "countries": [],
                "route_types": [],
                "aircraft_types": [],
                "distance_stats": {},
                "flight_hour_stats": {},
            }

        # Thống kê khoảng cách
        distance_stats = (
            db.query(
                func.avg(Route.distance_km).label("avg_distance"),
                func.min(Route.distance_km).label("min_distance"),
                func.max(Route.distance_km).label("max_distance"),
            )
            .filter(Route.distance_km.isnot(None))
            .first()
        )

        # Thống kê thời gian bay
        flight_hour_stats = (
            db.query(
                func.avg(Route.flight_hour).label("avg_flight_hour"),
                func.min(Route.flight_hour).label("min_flight_hour"),
                func.max(Route.flight_hour).label("max_flight_hour"),
            )
            .filter(Route.flight_hour.isnot(None))
            .first()
        )

        # Thống kê theo quốc gia
        countries = (
            db.query(Route.country, func.count(Route.country).label("count"))
            .filter(Route.country.isnot(None))
            .group_by(Route.country)
            .order_by(func.count(Route.country).desc())
            .limit(10)
            .all()
        )

        # Thống kê theo loại route
        route_types = (
            db.query(Route.type, func.count(Route.type).label("count"))
            .filter(Route.type.isnot(None))
            .group_by(Route.type)
            .order_by(func.count(Route.type).desc())
            .all()
        )

        # Thống kê theo aircraft type
        aircraft_types = (
            db.query(Route.ac, func.count(Route.ac).label("count"))
            .filter(Route.ac.isnot(None))
            .group_by(Route.ac)
            .order_by(func.count(Route.ac).desc())
            .limit(10)
            .all()
        )

        return {
            "total_routes": total_count,
            "countries": [{"name": c.country, "count": c.count} for c in countries],
            "route_types": [{"name": rt.type, "count": rt.count} for rt in route_types],
            "aircraft_types": [
                {"name": ac.ac, "count": ac.count} for ac in aircraft_types
            ],
            "distance_stats": {
                "average": (
                    round(float(distance_stats.avg_distance), 2)
                    if distance_stats.avg_distance
                    else 0
                ),
                "min": (
                    float(distance_stats.min_distance)
                    if distance_stats.min_distance
                    else 0
                ),
                "max": (
                    float(distance_stats.max_distance)
                    if distance_stats.max_distance
                    else 0
                ),
            },
            "flight_hour_stats": {
                "average": (
                    round(float(flight_hour_stats.avg_flight_hour), 2)
                    if flight_hour_stats.avg_flight_hour
                    else 0
                ),
                "min": (
                    float(flight_hour_stats.min_flight_hour)
                    if flight_hour_stats.min_flight_hour
                    else 0
                ),
                "max": (
                    float(flight_hour_stats.max_flight_hour)
                    if flight_hour_stats.max_flight_hour
                    else 0
                ),
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi thống kê đường bay: {str(e)}",
        )
