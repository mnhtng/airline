from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from datetime import datetime
from backend.db.database import get_db
from backend.models.airline_ref import AirlineRef
from backend.schema.airline_ref import (
    AirlineRefCreate,
    AirlineRefUpdate,
    AirlineRefResponse,
    AirlineRefBulkCreate,
    AirlineRefBulkCreateResponse,
)

router = APIRouter(prefix="/airlines", tags=["airlines"])


@router.get("/", response_model=List[AirlineRefResponse])
async def get_all_airline_refs(
    skip: int = 0, limit: int = None, db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả hãng hàng không
    """

    try:
        query = db.query(AirlineRef).order_by(AirlineRef.carrier).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        airline_refs = query.all()
        return [
            AirlineRefResponse(**airline_ref.to_dict()) for airline_ref in airline_refs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách hãng hàng không: {str(e)}",
        )


@router.post("/", response_model=AirlineRefResponse)
async def create_airline_ref(
    airline_ref: AirlineRefCreate, db: Session = Depends(get_db)
):
    """
    Tạo mới hãng hàng không
    """

    try:
        db_airline_ref = AirlineRef(**airline_ref.model_dump())
        db.add(db_airline_ref)
        db.commit()
        db.refresh(db_airline_ref)
        return AirlineRefResponse(**db_airline_ref.to_dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tạo hãng hàng không: {str(e)}",
        )


@router.post("/bulk-create", response_model=AirlineRefBulkCreateResponse)
async def create_airline_refs_bulk(
    airline_refs: AirlineRefBulkCreate, db: Session = Depends(get_db)
):
    """
    Tạo nhiều hãng hàng không cùng lúc

    - Tối đa 1000 hãng hàng không mỗi lần
    - Trả về danh sách hãng hàng không đã tạo thành công và các lỗi nếu có
    - Sử dụng transaction để đảm bảo tính nhất quán dữ liệu
    """

    if len(airline_refs.airline_refs) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ được tạo tối đa 1000 hãng hàng không mỗi lần",
        )

    created_airline_refs = []
    errors = []

    try:
        for i, airline_ref_data in enumerate(airline_refs.airline_refs):
            try:
                db_airline_ref = AirlineRef(**airline_ref_data.model_dump())
                db.add(db_airline_ref)
                db.flush()  # Flush để có id nhưng chưa commit
                created_airline_refs.append(db_airline_ref)
            except Exception as e:
                errors.append(
                    f"Hãng hàng không thứ {i+1} ({airline_ref_data.carrier}): {str(e)}"
                )

        if errors:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Có lỗi xảy ra khi tạo hãng hàng không",
                    "errors": errors,
                    "created_count": 0,
                },
            )

        db.commit()

        for airline_ref in created_airline_refs:
            db.refresh(airline_ref)

        return AirlineRefBulkCreateResponse(
            created_airline_refs=created_airline_refs,
            total_created=len(created_airline_refs),
            errors=[],
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tạo hãng hàng không: {str(e)}",
        )


@router.put("/{airline_id}", response_model=AirlineRefResponse)
async def update_airline_ref(
    airline_id: int, airline_ref_update: AirlineRefUpdate, db: Session = Depends(get_db)
):
    """
    Cập nhật hãng hàng không
    """

    try:
        db_airline_ref = (
            db.query(AirlineRef).filter(AirlineRef.id == airline_id).first()
        )
        if not db_airline_ref:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy hãng hàng không trong hệ thống",
            )

        update_data = airline_ref_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_airline_ref, field, value)
        setattr(db_airline_ref, "updated_at", datetime.now())

        db.commit()
        db.refresh(db_airline_ref)
        return AirlineRefResponse(**db_airline_ref.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi cập nhật hãng hàng không: {str(e)}",
        )


@router.delete("/{airline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_airline_ref(airline_id: int, db: Session = Depends(get_db)):
    """
    Xóa hãng hàng không
    """

    try:
        db_airline_ref = (
            db.query(AirlineRef).filter(AirlineRef.id == airline_id).first()
        )
        if not db_airline_ref:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy hãng hàng không trong hệ thống",
            )

        db.delete(db_airline_ref)
        db.commit()
        return {
            "message": f"Đã xóa hãng hàng không {db_airline_ref.carrier} thành công"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi xóa hãng hàng không: {str(e)}",
        )


@router.get("/search/", response_model=List[AirlineRefResponse])
async def search_airline_refs(q: str = None, db: Session = Depends(get_db)):
    """
    Tìm kiếm hãng hàng không
    """

    try:
        # Using 'collate' for case-insensitive and accent-insensitive search in MSSQL
        collation = "SQL_Latin1_General_CP1_CI_AI"
        airline_refs = (
            db.query(AirlineRef)
            .filter(
                or_(
                    AirlineRef.carrier.collate(collation).like(f"%{q}%"),
                    AirlineRef.airline_nation.collate(collation).like(f"%{q}%"),
                    AirlineRef.airlines_name.collate(collation).like(f"%{q}%"),
                )
            )
            .order_by(AirlineRef.carrier)
            .all()
        )

        return [
            AirlineRefResponse(**airline_ref.to_dict()) for airline_ref in airline_refs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tìm kiếm hãng hàng không: {str(e)}",
        )
