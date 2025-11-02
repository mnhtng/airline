from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from backend.db.database import get_db
from backend.models.country_ref import CountryRef
from backend.schema.country_ref import (
    CountryRefCreate,
    CountryRefUpdate,
    CountryRefResponse,
    CountryRefBulkCreate,
    CountryRefBulkCreateResponse,
)


router = APIRouter(prefix="/countries", tags=["countries"])


@router.get("/", response_model=List[CountryRefResponse])
async def get_all_country_refs(
    skip: int = 0, limit: int = None, db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả quốc gia
    """

    try:
        query = db.query(CountryRef).order_by(CountryRef.country).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        country_refs = query.all()
        return [
            CountryRefResponse(**country_ref.to_dict()) for country_ref in country_refs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách quốc gia: {str(e)}",
        )


@router.post("/", response_model=CountryRefResponse)
async def create_country_ref(
    country_ref: CountryRefCreate, db: Session = Depends(get_db)
):
    """
    Tạo mới quốc gia
    """

    try:
        db_country_ref = CountryRef(**country_ref.model_dump())
        db.add(db_country_ref)
        db.commit()
        db.refresh(db_country_ref)
        return CountryRefResponse(**db_country_ref.to_dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tạo quốc gia: {str(e)}",
        )


@router.post(
    "/bulk-create",
    response_model=CountryRefBulkCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_country_refs_bulk(
    country_refs: CountryRefBulkCreate, db: Session = Depends(get_db)
):
    """
    Tạo nhiều quốc gia cùng lúc

    - Tối đa 1000 quốc gia mỗi lần
    - Trả về danh sách quốc gia đã tạo thành công và các lỗi nếu có
    - Sử dụng transaction để đảm bảo tính nhất quán dữ liệu
    """

    if len(country_refs.country_refs) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ được tạo tối đa 1000 quốc gia mỗi lần",
        )

    created_country_refs = []
    errors = []

    try:
        for i, country_ref_data in enumerate(country_refs.country_refs):
            try:
                db_country_ref = CountryRef(**country_ref_data.model_dump())
                db.add(db_country_ref)
                db.flush()  # Flush để có id nhưng chưa commit
                created_country_refs.append(db_country_ref)
            except Exception as e:
                errors.append(
                    f"Quốc gia thứ {i+1} ({country_ref_data.country}): {str(e)}"
                )

        if errors:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Có lỗi xảy ra khi tạo quốc gia",
                    "errors": errors,
                    "created_count": 0,
                },
            )

        db.commit()

        for country_ref in created_country_refs:
            db.refresh(country_ref)

        return CountryRefBulkCreateResponse(
            created_country_refs=created_country_refs,
            total_created=len(created_country_refs),
            errors=[],
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tạo quốc gia: {str(e)}",
        )


@router.put("/{country_id}", response_model=CountryRefResponse)
async def update_country_ref(
    country_id: int, country_ref_update: CountryRefUpdate, db: Session = Depends(get_db)
):
    """
    Cập nhật quốc gia
    """

    try:
        db_country_ref = (
            db.query(CountryRef).filter(CountryRef.id == country_id).first()
        )
        if not db_country_ref:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy quốc gia trong hệ thống",
            )

        update_data = country_ref_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_country_ref, field, value)
        setattr(db_country_ref, "updated_at", datetime.now())

        db.commit()
        db.refresh(db_country_ref)
        return CountryRefResponse(**db_country_ref.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi cập nhật quốc gia: {str(e)}",
        )


@router.delete("/{country_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_country_ref(country_id: int, db: Session = Depends(get_db)):
    """
    Xóa quốc gia
    """

    try:
        db_country_ref = (
            db.query(CountryRef).filter(CountryRef.id == country_id).first()
        )
        if not db_country_ref:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy quốc gia trong hệ thống",
            )

        db.delete(db_country_ref)
        db.commit()
        return {"message": f"Đã xóa quốc gia {db_country_ref.country} thành công"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi xóa quốc gia: {str(e)}",
        )


@router.get("/search/", response_model=List[CountryRefResponse])
async def search_country_refs(q: str = None, db: Session = Depends(get_db)):
    """
    Tìm kiếm quốc gia
    """

    collation = "SQL_Latin1_General_CP1_CI_AI"
    try:
        query = db.query(CountryRef).order_by(CountryRef.country)

        if q:
            query = query.filter(
                or_(
                    CountryRef.country.collate(collation).like(f"%{q}%"),
                    CountryRef.region.collate(collation).like(f"%{q}%"),
                    CountryRef.region_vnm.collate(collation).like(f"%{q}%"),
                    CountryRef.two_letter_code.collate(collation).like(f"%{q}%"),
                    CountryRef.three_letter_code.collate(collation).like(f"%{q}%"),
                )
            )

        country_refs = query.all()
        return [
            CountryRefResponse(**country_ref.to_dict()) for country_ref in country_refs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tìm kiếm quốc gia: {str(e)}",
        )
