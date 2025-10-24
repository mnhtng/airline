from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.db.database import get_db
from backend.models.dim_airline_ref import DimAirlineRef
from backend.schema.dim_airline_ref import (
    DimAirlineRefResponse,
)

router = APIRouter(prefix="/dim-airlines", tags=["dim-airlines"])


@router.get("/", response_model=List[DimAirlineRefResponse])
async def get_all_dim_airline_refs(
    skip: int = 0, limit: int = None, db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả hãng hàng không
    """

    try:
        query = db.query(DimAirlineRef).order_by(DimAirlineRef.carrier).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        dim_airline_refs = query.all()
        return [
            DimAirlineRefResponse(**dim_airline_ref.to_dict())
            for dim_airline_ref in dim_airline_refs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách hãng hàng không: {str(e)}",
        )
