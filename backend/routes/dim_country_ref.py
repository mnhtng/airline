from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.db.database import get_db
from backend.models.dim_country_ref import DimCountryRef
from backend.schema.dim_country_ref import (
    DimCountryRefResponse,
)


router = APIRouter(prefix="/dim-countries", tags=["dim-countries"])


@router.get("/", response_model=List[DimCountryRefResponse])
async def get_all_dim_countries(
    skip: int = 0, limit: int = None, db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả quốc gia
    """

    try:
        query = db.query(DimCountryRef).order_by(DimCountryRef.country).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        dim_country_refs = query.all()
        return [
            DimCountryRefResponse(**dim_country_ref.to_dict())
            for dim_country_ref in dim_country_refs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách quốc gia: {str(e)}",
        )
