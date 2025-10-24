from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.db.database import get_db
from backend.models.dim_sector_route_dom_ref import DimSectorRouteDomRef
from backend.schema.dim_sector_route_dom_ref import (
    DimSectorRouteDomRefResponse,
)

router = APIRouter(prefix="/dim-sector-route-doms", tags=["dim-sector-route-doms"])


@router.get("/", response_model=List[DimSectorRouteDomRefResponse])
async def get_all_dim_sector_route_dom_refs(
    skip: int = 0, limit: int = None, db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả phân loại tuyến bay
    """

    try:
        query = (
            db.query(DimSectorRouteDomRef)
            .order_by(DimSectorRouteDomRef.sector)
            .offset(skip)
        )
        if limit is not None:
            query = query.limit(limit)
        dim_sector_route_dom_refs = query.all()
        return [
            DimSectorRouteDomRefResponse(**dim_sector_route_dom_ref.to_dict())
            for dim_sector_route_dom_ref in dim_sector_route_dom_refs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách phân loại tuyến bay: {str(e)}",
        )
