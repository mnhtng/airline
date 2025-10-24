from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.db.database import get_db
from backend.models.dim_airport_ref import DimAirportRef
from backend.schema.dim_airport_ref import (
    DimAirportRefResponse,
)

router = APIRouter(prefix="/dim-airports", tags=["dim-airports"])


@router.get("/", response_model=List[DimAirportRefResponse])
async def get_all_dim_airport_refs(
    skip: int = 0, limit: int = None, db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả sân bay
    """

    try:
        query = db.query(DimAirportRef).order_by(DimAirportRef.iata_code).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        dim_airport_refs = query.all()
        return [
            DimAirportRefResponse(**dim_airport_ref.to_dict())
            for dim_airport_ref in dim_airport_refs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách sân bay: {str(e)}",
        )
