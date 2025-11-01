from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from datetime import datetime
from backend.db.database import get_db
from backend.models.sector_route_dom_ref import SectorRouteDomRef
from backend.schema.sector_route_dom_ref import (
    SectorRouteDomRefCreate,
    SectorRouteDomRefUpdate,
    SectorRouteDomRefResponse,
    SectorRouteDomRefBulkCreate,
    SectorRouteDomRefBulkCreateResponse,
)

router = APIRouter(prefix="/sector-route-doms", tags=["sector-route-doms"])


@router.get("/", response_model=List[SectorRouteDomRefResponse])
async def get_all_sector_route_dom_refs(
    skip: int = 0, limit: int = None, db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả phân loại tuyến bay
    """

    try:
        query = (
            db.query(SectorRouteDomRef).order_by(SectorRouteDomRef.sector).offset(skip)
        )
        if limit is not None:
            query = query.limit(limit)
        sector_route_dom_refs = query.all()
        return [
            SectorRouteDomRefResponse(**sector_route_dom_ref.to_dict())
            for sector_route_dom_ref in sector_route_dom_refs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi lấy danh sách phân loại tuyến bay: {str(e)}",
        )


@router.post("/", response_model=SectorRouteDomRefResponse)
async def create_sector_route_dom_ref(
    sector_route_dom_ref: SectorRouteDomRefCreate, db: Session = Depends(get_db)
):
    """
    Tạo mới phân loại tuyến bay
    """

    try:
        db_sector_route_dom_ref = SectorRouteDomRef(**sector_route_dom_ref.model_dump())
        db.add(db_sector_route_dom_ref)
        db.commit()
        db.refresh(db_sector_route_dom_ref)
        return SectorRouteDomRefResponse(**db_sector_route_dom_ref.to_dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tạo phân loại tuyến bay: {str(e)}",
        )


@router.post("/bulk-create", response_model=SectorRouteDomRefBulkCreateResponse)
async def create_sector_route_dom_refs_bulk(
    sector_route_dom_refs: SectorRouteDomRefBulkCreate, db: Session = Depends(get_db)
):
    """
    Tạo nhiều phân loại tuyến bay cùng lúc

    - Tối đa 1000 phân loại tuyến bay mỗi lần
    - Trả về danh sách phân loại tuyến bay đã tạo thành công và các lỗi nếu có
    - Sử dụng transaction để đảm bảo tính nhất quán dữ liệu
    """

    if len(sector_route_dom_refs.sector_route_dom_refs) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ được tạo tối đa 1000 phân loại tuyến bay mỗi lần",
        )

    created_sector_route_dom_refs = []
    errors = []

    try:
        for i, sector_route_dom_ref_data in enumerate(
            sector_route_dom_refs.sector_route_dom_refs
        ):
            try:
                db_sector_route_dom_ref = SectorRouteDomRef(
                    **sector_route_dom_ref_data.model_dump()
                )
                db.add(db_sector_route_dom_ref)
                db.flush()  # Flush để có id nhưng chưa commit
                created_sector_route_dom_refs.append(db_sector_route_dom_ref)
            except Exception as e:
                errors.append(
                    f"Phân loại tuyến bay thứ {i+1} ({sector_route_dom_ref_data.sector}): {str(e)}"
                )

        if errors:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Có lỗi xảy ra khi tạo phân loại tuyến bay",
                    "errors": errors,
                    "created_count": 0,
                },
            )

        db.commit()

        for sector_route_dom_ref in created_sector_route_dom_refs:
            db.refresh(sector_route_dom_ref)

        return SectorRouteDomRefBulkCreateResponse(
            created_sector_route_dom_refs=created_sector_route_dom_refs,
            total_created=len(created_sector_route_dom_refs),
            errors=[],
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tạo phân loại tuyến bay: {str(e)}",
        )


@router.put("/{sector_route_dom_id}", response_model=SectorRouteDomRefResponse)
async def update_sector_route_dom_ref(
    sector_route_dom_id: int,
    sector_route_dom_ref_update: SectorRouteDomRefUpdate,
    db: Session = Depends(get_db),
):
    """
    Cập nhật phân loại tuyến bay
    """

    try:
        db_sector_route_dom_ref = (
            db.query(SectorRouteDomRef)
            .filter(SectorRouteDomRef.id == sector_route_dom_id)
            .first()
        )
        if not db_sector_route_dom_ref:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy phân loại tuyến bay trong hệ thống",
            )

        update_data = sector_route_dom_ref_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sector_route_dom_ref, field, value)
        setattr(db_sector_route_dom_ref, "updated_at", datetime.now)

        db.commit()
        db.refresh(db_sector_route_dom_ref)
        return SectorRouteDomRefResponse(**db_sector_route_dom_ref.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi cập nhật phân loại tuyến bay: {str(e)}",
        )


@router.delete("/{sector_route_dom_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sector_route_dom_ref(
    sector_route_dom_id: int, db: Session = Depends(get_db)
):
    """
    Xóa phân loại tuyến bay
    """

    try:
        db_sector_route_dom_ref = (
            db.query(SectorRouteDomRef)
            .filter(SectorRouteDomRef.id == sector_route_dom_id)
            .first()
        )
        if not db_sector_route_dom_ref:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy phân loại tuyến bay trong hệ thống",
            )

        db.delete(db_sector_route_dom_ref)
        db.commit()
        return {
            "message": f"Đã xóa phân loại tuyến bay {db_sector_route_dom_ref.sector} thành công"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi xóa phân loại tuyến bay: {str(e)}",
        )


@router.get("/search/", response_model=List[SectorRouteDomRefResponse])
async def search_sector_route_dom_refs(q: str = None, db: Session = Depends(get_db)):
    """
    Tìm kiếm phân loại tuyến bay
    """

    try:
        query = db.query(SectorRouteDomRef).order_by(SectorRouteDomRef.sector)

        if q:
            search_term = f"%{q.lower().strip()}%"
            query = query.filter(
                or_(
                    SectorRouteDomRef.sector.ilike(search_term),
                    SectorRouteDomRef.area_lv1.ilike(search_term),
                    SectorRouteDomRef.dom_int.ilike(search_term),
                )
            )

        sector_route_dom_refs = query.all()
        return [
            SectorRouteDomRefResponse(**sector_route_dom_ref.to_dict())
            for sector_route_dom_ref in sector_route_dom_refs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server khi tìm kiếm phân loại tuyến bay: {str(e)}",
        )
