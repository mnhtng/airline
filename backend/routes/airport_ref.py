from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from datetime import datetime
from backend.db.database import get_db
from backend.models.airport_ref import AirportRef
from backend.schema.airport_ref import (
    AirportRefCreate,
    AirportRefUpdate,
    AirportRefResponse,
    AirportRefBulkCreate,
    AirportRefBulkCreateResponse,
)

router = APIRouter(prefix="/airports", tags=["airports"])


@router.get("/", response_model=List[AirportRefResponse])
async def get_all_airport_refs(
    skip: int = 0, limit: int = None, db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả sân bay
    """

    try:
        query = db.query(AirportRef).order_by(AirportRef.iata_code).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        airport_refs = query.all()
        return [
            AirportRefResponse(**airport_ref.to_dict()) for airport_ref in airport_refs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách sân bay: {str(e)}",
        )


@router.post("/", response_model=AirportRefResponse)
async def create_airport_ref(
    airport_ref: AirportRefCreate, db: Session = Depends(get_db)
):
    """
    Tạo mới sân bay
    """

    try:
        db_airport_ref = AirportRef(**airport_ref.model_dump())
        db.add(db_airport_ref)
        db.commit()
        db.refresh(db_airport_ref)
        return AirportRefResponse(**db_airport_ref.to_dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tạo sân bay: {str(e)}",
        )


@router.post("/bulk-create", response_model=AirportRefBulkCreateResponse)
async def create_airport_refs_bulk(
    airport_refs: AirportRefBulkCreate, db: Session = Depends(get_db)
):
    """
    Tạo nhiều sân bay cùng lúc

    - Tối đa 1000 sân bay mỗi lần
    - Trả về danh sách sân bay đã tạo thành công và các lỗi nếu có
    - Sử dụng transaction để đảm bảo tính nhất quán dữ liệu
    """

    if len(airport_refs.airport_refs) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ được tạo tối đa 1000 sân bay mỗi lần",
        )

    created_airport_refs = []
    errors = []

    try:
        for i, airport_ref_data in enumerate(airport_refs.airport_refs):
            try:
                db_airport_ref = AirportRef(**airport_ref_data.model_dump())
                db.add(db_airport_ref)
                db.flush()  # Flush để có id nhưng chưa commit
                created_airport_refs.append(db_airport_ref)
            except Exception as e:
                errors.append(
                    f"Sân bay thứ {i+1} ({airport_ref_data.iata_code}): {str(e)}"
                )

        if errors:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Có lỗi xảy ra khi tạo sân bay",
                    "errors": errors,
                    "created_count": 0,
                },
            )

        db.commit()

        for airport_ref in created_airport_refs:
            db.refresh(airport_ref)

        return AirportRefBulkCreateResponse(
            created_airport_refs=created_airport_refs,
            total_created=len(created_airport_refs),
            errors=[],
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tạo sân bay: {str(e)}",
        )


@router.put("/{airport_id}", response_model=AirportRefResponse)
async def update_airport_ref(
    airport_id: int, airport_ref_update: AirportRefUpdate, db: Session = Depends(get_db)
):
    """
    Cập nhật sân bay
    """

    try:
        db_airport_ref = (
            db.query(AirportRef).filter(AirportRef.id == airport_id).first()
        )
        if not db_airport_ref:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy sân bay trong hệ thống",
            )

        update_data = airport_ref_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_airport_ref, field, value)
        setattr(db_airport_ref, "updated_at", datetime.now)

        db.commit()
        db.refresh(db_airport_ref)
        return AirportRefResponse(**db_airport_ref.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi cập nhật sân bay: {str(e)}",
        )


@router.delete("/{airport_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_airport_ref(airport_id: int, db: Session = Depends(get_db)):
    """
    Xóa sân bay
    """

    try:
        db_airport_ref = (
            db.query(AirportRef).filter(AirportRef.id == airport_id).first()
        )
        if not db_airport_ref:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy sân bay trong hệ thống",
            )

        db.delete(db_airport_ref)
        db.commit()
        return {"message": f"Đã xóa sân bay {db_airport_ref.iata_code} thành công"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi xóa sân bay: {str(e)}",
        )


@router.get("/search/", response_model=List[AirportRefResponse])
async def search_airport_refs(q: str = None, db: Session = Depends(get_db)):
    """
    Tìm kiếm sân bay
    """

    try:
        query = db.query(AirportRef).order_by(AirportRef.iata_code)

        if q:
            search_term = f"%{q.lower().strip()}%"
            query = query.filter(
                or_(
                    AirportRef.iata_code.ilike(search_term),
                    AirportRef.airport_name.ilike(search_term),
                    AirportRef.city.ilike(search_term),
                    AirportRef.country.ilike(search_term),
                )
            )

        airport_refs = query.all()
        return [
            AirportRefResponse(**airport_ref.to_dict()) for airport_ref in airport_refs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tìm kiếm sân bay: {str(e)}",
        )
