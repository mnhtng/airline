from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from backend.db.database import get_db
from backend.services.excel_batch_processor import ExcelBatchProcessor
from backend.schema.flight_data import (
    ExcelProcessRequest,
    ExcelProcessResponse,
    FlightRawResponse,
    MissingDimensionResponse,
    DataProcessingStats,
)
from backend.models.flight_raw import FlightRaw
from backend.models.missing_dimensions_log import MissingDimensionsLog


router = APIRouter(prefix="/data-processing", tags=["data-processing"])


@router.post("/process-excel", response_model=ExcelProcessResponse)
async def process_excel_data(
    request: ExcelProcessRequest, db: Session = Depends(get_db)
):
    """
    Xử lý dữ liệu Excel và lưu vào database - DEPRECATED
    Sử dụng /upload-files thay thế cho endpoint này
    """
    try:
        processor = ExcelBatchProcessor(db)

        # Tạo temporary file từ request data để process
        import tempfile
        import pandas as pd
        import os

        # Convert request data to DataFrame and save as temp Excel file
        df = pd.DataFrame(request.data)

        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
            temp_path = temp_file.name
            df.to_excel(temp_path, index=False)

            try:
                # Process using ExcelBatchProcessor logic
                processed_df = processor.process_excel_file(temp_path, request.filename)

                if processed_df.empty:
                    return ExcelProcessResponse(
                        success=False,
                        message="Không thể xử lý dữ liệu Excel",
                        processed_count=0,
                        errors=["Không có dữ liệu hợp lệ để xử lý"],
                    )

                # Save to database
                processor._save_to_database(processed_df)
                processed_count = len(processed_df)

                # Mark file as imported
                processor.mark_file_imported(request.filename, "excel", processed_count)

                # Run data cleaning stored procedure
                processor.run_data_cleaning_stored_procedure()

                db.commit()

                return ExcelProcessResponse(
                    success=True,
                    message=f"Đã xử lý thành công {processed_count} bản ghi từ file {request.filename}",
                    processed_count=processed_count,
                    duplicates_count=0,
                    errors=[],
                )

            finally:
                # Clean up temp file
                os.unlink(temp_path)

    except Exception as e:
        db.rollback()
        logging.error(f"Error processing Excel data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi xử lý dữ liệu: {str(e)}",
        )


@router.get("/flight-data", response_model=List[FlightRawResponse])
async def get_flight_data(
    skip: int = 0,
    limit: int = 100,
    route: Optional[str] = None,
    actype: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Lấy danh sách dữ liệu flight raw
    """
    query = db.query(FlightRaw).order_by(FlightRaw.id.desc())

    if route:
        query = query.filter(FlightRaw.route.contains(route))

    if actype:
        query = query.filter(FlightRaw.actype.contains(actype))

    flights = query.offset(skip).limit(limit).all()
    return flights


@router.get("/missing-dimensions", response_model=List[MissingDimensionResponse])
async def get_missing_dimensions(
    dimension_type: Optional[str] = None, db: Session = Depends(get_db)
):
    """
    Lấy danh sách missing dimensions
    """
    query = db.query(MissingDimensionsLog)

    if dimension_type:
        query = query.filter(MissingDimensionsLog.type == dimension_type)

    missing_dims = query.order_by(MissingDimensionsLog.count.desc()).all()
    return missing_dims


@router.get("/stats", response_model=DataProcessingStats)
async def get_processing_stats(db: Session = Depends(get_db)):
    """
    Lấy thống kê xử lý dữ liệu
    """
    try:
        processor = ExcelBatchProcessor(db)
        summary = processor.get_processing_summary()

        # Convert to DataProcessingStats format
        stats = {
            "total_flights": summary.get("raw_records", 0),
            "missing_actypes": summary.get("missing_actypes", 0),
            "missing_routes": summary.get("missing_routes", 0),
            "latest_import": None,  # Can add this to ExcelBatchProcessor if needed
            "file_count": summary.get("imported_files", 0),
        }

        return DataProcessingStats(**stats)

    except Exception as e:
        logging.error(f"Error getting processing stats: {e}")
        # Return empty stats if error
        return DataProcessingStats(
            total_flights=0,
            missing_actypes=0,
            missing_routes=0,
            latest_import=None,
            file_count=0,
        )


@router.post("/run-stored-procedure")
async def run_stored_procedure(db: Session = Depends(get_db)):
    """
    Chạy stored procedure để xử lý dữ liệu
    """
    try:
        processor = ExcelBatchProcessor(db)
        processor.run_data_cleaning_stored_procedure()

        return {"success": True, "message": "Đã chạy stored procedure thành công"}

    except Exception as e:
        logging.error(f"Error running stored procedure: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi chạy stored procedure: {str(e)}",
        )


@router.delete("/flight-data")
async def clear_flight_data(db: Session = Depends(get_db)):
    """
    Xóa tất cả dữ liệu flight raw (chỉ dùng cho development)
    """
    try:
        # Delete all flight raw data
        db.query(FlightRaw).delete()

        # Delete import log
        from sqlalchemy import text

        db.execute(text("DELETE FROM import_log"))

        # Delete missing dimensions log
        db.query(MissingDimensionsLog).delete()

        db.commit()

        return {"success": True, "message": "Đã xóa tất cả dữ liệu"}

    except Exception as e:
        db.rollback()
        logging.error(f"Error clearing data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi xóa dữ liệu: {str(e)}",
        )


@router.post("/import-missing-dimensions")
async def import_missing_dimensions_data(db: Session = Depends(get_db)):
    """
    Chạy stored procedure để import missing dimensions data từ temp tables
    Theo logic từ notebook để xử lý aircraft types và routes thiếu
    """
    try:
        from sqlalchemy import text

        print("🔧 Bắt đầu import missing dimensions data...")

        processor = ExcelBatchProcessor(db)

        # Get missing dimensions before import
        before_summary = processor.get_processing_summary()
        print(
            f"📊 Trước import: {before_summary['missing_actypes']} actypes thiếu, {before_summary['missing_routes']} routes thiếu"
        )

        # Run the stored procedure to import and update missing dimensions
        print("⚙️ Chạy stored procedure: usp_ImportAndUpdateMissingDimensions")
        db.execute(text("EXEC usp_ImportAndUpdateMissingDimensions"))
        db.commit()

        # Get summary after import
        after_summary = processor.get_processing_summary()
        print(
            f"📊 Sau import: {after_summary['missing_actypes']} actypes thiếu, {after_summary['missing_routes']} routes thiếu"
        )

        # Calculate what was imported
        actypes_resolved = (
            before_summary["missing_actypes"] - after_summary["missing_actypes"]
        )
        routes_resolved = (
            before_summary["missing_routes"] - after_summary["missing_routes"]
        )

        return {
            "success": True,
            "message": f"Đã import missing dimensions thành công. Resolved {actypes_resolved} actypes và {routes_resolved} routes",
            "before_import": {
                "missing_actypes": before_summary["missing_actypes"],
                "missing_routes": before_summary["missing_routes"],
            },
            "after_import": {
                "missing_actypes": after_summary["missing_actypes"],
                "missing_routes": after_summary["missing_routes"],
            },
            "resolved": {"actypes": actypes_resolved, "routes": routes_resolved},
        }

    except Exception as e:
        db.rollback()
        error_msg = f"Lỗi import missing dimensions: {str(e)}"
        print(f"❌ {error_msg}")
        logging.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg,
        )


@router.post("/batch-import-excel")
async def batch_import_excel_files(
    data_folder: str, destination_folder: str, db: Session = Depends(get_db)
):
    """
    Batch import tất cả file Excel từ folder theo logic notebook
    """
    try:
        processor = ExcelBatchProcessor(db)

        # Batch import files
        results = processor.batch_import_files(data_folder, destination_folder)

        if results["processed_files"] > 0:
            # Run data cleaning stored procedure
            processor.run_data_cleaning_stored_procedure()

        return {
            "success": True,
            "message": f"Đã xử lý {results['processed_files']} file với tổng {results['total_rows']} bản ghi",
            "processed_files": results["processed_files"],
            "total_rows": results["total_rows"],
            "skipped_files": results["skipped_files"],
            "errors": results["errors"],
            "file_details": results["file_details"],
        }

    except Exception as e:
        logging.error(f"Error in batch import: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi batch import: {str(e)}",
        )


@router.post("/run-data-cleaning")
async def run_data_cleaning(db: Session = Depends(get_db)):
    """
    Chạy stored procedure để làm sạch và xử lý dữ liệu flight
    """
    try:
        processor = ExcelBatchProcessor(db)
        processor.run_data_cleaning_stored_procedure()

        return {"success": True, "message": "Đã chạy data cleaning thành công"}

    except Exception as e:
        logging.error(f"Error running data cleaning: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi chạy data cleaning: {str(e)}",
        )


@router.post("/revalidate-error-data")
async def revalidate_error_data(db: Session = Depends(get_db)):
    """
    Chạy stored procedure để revalidate error data
    """
    try:
        from sqlalchemy import text

        db.execute(text("EXEC usp_RevalidateErrorData"))
        db.commit()

        return {"success": True, "message": "Đã revalidate error data thành công"}

    except Exception as e:
        db.rollback()
        logging.error(f"Error revalidating error data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi revalidate error data: {str(e)}",
        )


@router.get("/processing-summary")
async def get_processing_summary(db: Session = Depends(get_db)):
    """
    Lấy tóm tắt quá trình xử lý dữ liệu
    """
    try:
        processor = ExcelBatchProcessor(db)
        summary = processor.get_processing_summary()

        return {"success": True, "data": summary}

    except Exception as e:
        logging.error(f"Error getting processing summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi lấy processing summary: {str(e)}",
        )


@router.post("/export-missing-dimensions")
async def export_missing_dimensions_to_excel(db: Session = Depends(get_db)):
    """
    Xuất missing dimensions ra file Excel theo logic notebook
    Tạo file Add_information.xlsx với 3 sheets: Actype_seat, Route, Airline_Route_Details
    """
    try:
        import pandas as pd
        import tempfile
        import os
        from fastapi.responses import FileResponse
        from sqlalchemy import text

        print("📤 Bắt đầu export missing dimensions...")

        # Query 1: Actype_seat - missing actypes from error table
        query1 = """
        SELECT TOP 0 actype, seat
        FROM actype_seat
        UNION ALL
        SELECT Value as actype, NULL as seat
        FROM Missing_Dimensions_Log
        WHERE Type = 'ACTYPE'
        GROUP BY Value
        """

        # Query 2: Route - missing routes from error table
        query2 = """
        SELECT TOP 0
            [ROUTE],
            [AC],
            [Route_ID],
            [FLIGHT HOUR],
            [TAXI],
            [BLOCK HOUR],
            [DISTANCE KM],
            [Loại],
            [Type],
            [Country]
        FROM Route
        UNION
        SELECT Value as [ROUTE],
            NULL AS [AC],
            NULL AS [Route_ID],
            NULL AS [FLIGHT HOUR],
            NULL AS [TAXI],
            NULL AS [BLOCK HOUR],
            NULL AS [DISTANCE KM],
            NULL AS [Loại],
            NULL AS [Type],
            NULL AS [Country]
        FROM Missing_Dimensions_Log
        WHERE Type = 'ROUTE'
        AND Value IS NOT NULL
        """

        # Query 3: Airline_Route_Details - missing routes for route details
        query3 = """
        SELECT TOP 0
            [Sector] as [ROUTE],
            [Distance mile GDS],
            [Distance km GDS],
            [Sector_2],
            [Country 1],
            [Country 2],
            [Country],
            [DOM/INT],
            [Area]
        FROM Airline_Route_Details
        UNION
        SELECT Value as [ROUTE],
            NULL as [Distance mile GDS],
            NULL as [Distance km GDS],
            NULL as [Sector_2],
            NULL as [Country 1],
            NULL as [Country 2],
            NULL as [Country],
            NULL as [DOM/INT],
            NULL as [Area]
        FROM Missing_Dimensions_Log
        WHERE Type = 'ROUTE'
        AND Value IS NOT NULL
        """

        # Execute queries and create DataFrames
        df1 = pd.read_sql(query1, db.bind)
        df2 = pd.read_sql(query2, db.bind)
        df3 = pd.read_sql(query3, db.bind)

        print(
            f"📊 Export data: {len(df1)} actypes, {len(df2)} routes, {len(df3)} route details"
        )

        # Create temporary Excel file
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
            temp_path = temp_file.name

            # Write to Excel with multiple sheets
            with pd.ExcelWriter(temp_path, engine="openpyxl") as writer:
                df1.to_excel(writer, sheet_name="Actype_seat", index=False)
                df2.to_excel(writer, sheet_name="Route", index=False)
                df3.to_excel(writer, sheet_name="Airline_Route_Details", index=False)

        print(f"✅ Đã tạo file Excel: Add_information.xlsx")

        # Return file response
        return FileResponse(
            path=temp_path,
            filename="Add_information.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception as e:
        error_msg = f"Lỗi export missing dimensions: {str(e)}"
        print(f"❌ {error_msg}")
        logging.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_msg
        )


@router.post("/upload-files")
async def upload_excel_files(
    files: List[UploadFile] = File(...), db: Session = Depends(get_db)
):
    """
    Upload và xử lý multiple Excel files
    - Import dữ liệu từ file Excel
    - Phân loại file theo MN, MB, MT
    - Xử lý data theo từng loại
    - Chạy stored procedures để clean và enrich data

    Args:
        files (List[UploadFile]): Danh sách file Excel
        db (Session): Session của database

    Returns:
        Dict[str, Any]: Kết quả xử lý
    """

    try:
        import tempfile
        import os

        # All necessary functions
        processor = ExcelBatchProcessor(db)

        results = {
            "processed_files": 0,
            "total_rows": 0,
            "skipped_files": 0,
            "errors": [],
            "file_details": [],
            "processing_summary": {},
        }

        print(f"📤 Bắt đầu upload và xử lý {len(files)} file Excel...")

        # Create temp directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files to temp directory
            for file in files:
                if not file.filename.lower().endswith((".xlsx", ".xls")):
                    results["errors"].append(
                        f"File {file.filename} không phải là Excel file"
                    )
                    continue

                # Extract only filename from path (in case of folder upload)
                filename_only = os.path.basename(file.filename)
                file_path = os.path.join(temp_dir, filename_only)

                # Save file
                with open(file_path, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)

                try:
                    # Console log filename for debugging folder uploads
                    print(f"📁 Processing file: {file.filename} -> {filename_only}")

                    # Check if file already imported
                    if processor.is_file_imported(filename_only):
                        print(f"⏭️ File {filename_only} đã được import trước đó")
                        results["skipped_files"] += 1
                        continue

                    print(f"🔄 Đang xử lý file: {filename_only}")

                    # Determine file type first
                    file_type = processor.find_matching_key(filename_only)
                    if not file_type:
                        results["errors"].append(
                            f"Không thể xác định loại file: {filename_only}"
                        )
                        continue

                    print(f"📁 Loại file: {file_type} - {filename_only}")

                    # Process Excel file using notebook logic
                    df = processor.process_excel_file(file_path, filename_only)

                    if df.empty:
                        results["errors"].append(
                            f"Không có dữ liệu từ file {filename_only}"
                        )
                        continue

                    row_count = len(df)
                    print(f"📊 Extracted {row_count} rows từ {filename_only}")

                    # Save to flight_raw table
                    processor._save_to_database(df)

                    # Mark file as imported with file type
                    processor.mark_file_imported(filename_only, file_type, row_count)

                    results["processed_files"] += 1
                    results["total_rows"] += row_count
                    results["file_details"].append(
                        {
                            "file_name": filename_only,
                            "file_type": file_type,
                            "rows": row_count,
                        }
                    )

                    print(f"✅ Đã lưu {row_count} bản ghi từ file {filename_only}")

                except Exception as e:
                    error_msg = f"Lỗi xử lý file {filename_only}: {str(e)}"
                    print(f"❌ {error_msg}")
                    results["errors"].append(error_msg)

            # Commit raw data first
            db.commit()
            print(f"💾 Đã commit {results['total_rows']} bản ghi raw data")

            # Run data cleaning and processing if files were processed
            if results["processed_files"] > 0:
                print("🧹 Bắt đầu quá trình làm sạch và xử lý dữ liệu...")

                try:
                    # Step 1: Clean and process flight data
                    print("1️⃣ Chạy stored procedure: usp_CleanAndProcessFlightData")
                    processor.run_data_cleaning_stored_procedure()

                    # Step 2: Validate and move error data
                    print("2️⃣ Chạy stored procedure: usp_CleanAndValidateFlightData")
                    from sqlalchemy import text

                    db.execute(text("EXEC usp_CleanAndValidateFlightData"))
                    db.commit()

                    # Get processing summary
                    results["processing_summary"] = processor.get_processing_summary()

                    print("✅ Hoàn thành quá trình làm sạch và xử lý dữ liệu")

                except Exception as sp_error:
                    print(f"⚠️ Lỗi khi chạy stored procedures: {sp_error}")
                    results["errors"].append(f"Lỗi stored procedure: {str(sp_error)}")

        success_message = f"Đã xử lý thành công {results['processed_files']} file với tổng {results['total_rows']} bản ghi"
        if results["skipped_files"] > 0:
            success_message += f" (bỏ qua {results['skipped_files']} file đã import)"

        print(f"🎉 {success_message}")

        return {"success": True, "message": success_message, **results}

    except Exception as e:
        db.rollback()
        error_msg = f"Lỗi upload files: {str(e)}"
        print(f"💥 {error_msg}")
        logging.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_msg
        )


@router.post("/complete-workflow")
async def complete_data_processing_workflow(
    files: List[UploadFile] = File(...), db: Session = Depends(get_db)
):
    """
    Workflow hoàn chỉnh theo logic notebook:
    1. Upload và xử lý Excel files (MN, MB, MT)
    2. Import dữ liệu raw vào flight_raw
    3. Chạy stored procedures để clean và validate
    4. Export missing dimensions
    5. Trả về summary và file Excel cho missing data
    """
    try:
        print("🚀 Bắt đầu complete workflow xử lý dữ liệu Excel...")

        # Step 1: Upload and process Excel files
        upload_result = await upload_excel_files(files, db)

        if not upload_result["success"]:
            return upload_result

        print(f"✅ Step 1 hoàn thành: Upload {upload_result['processed_files']} files")

        # Step 2: Get processing summary after initial processing
        processor = ExcelBatchProcessor(db)
        summary_after_processing = processor.get_processing_summary()

        print(f"📊 Step 2: Summary sau xử lý - {summary_after_processing}")

        # Step 3: If there are missing dimensions, prepare export data
        missing_data_info = None
        if (
            summary_after_processing["missing_actypes"] > 0
            or summary_after_processing["missing_routes"] > 0
        ):
            print(
                f"⚠️ Phát hiện missing dimensions: {summary_after_processing['missing_actypes']} actypes, {summary_after_processing['missing_routes']} routes"
            )

            # Create export data info (without actually creating file here)
            missing_data_info = {
                "missing_actypes": summary_after_processing["missing_actypes"],
                "missing_routes": summary_after_processing["missing_routes"],
                "export_available": True,
                "message": "Có dữ liệu thiếu cần bổ sung. Sử dụng endpoint /export-missing-dimensions để tải file Excel.",
            }

        # Final summary
        final_summary = {
            "workflow_completed": True,
            "files_processed": upload_result["processed_files"],
            "total_rows": upload_result["total_rows"],
            "processing_summary": summary_after_processing,
            "missing_data_info": missing_data_info,
            "next_steps": [],
        }

        # Add next steps recommendations
        if missing_data_info:
            final_summary["next_steps"].append(
                "1. Tải file missing dimensions bằng endpoint /export-missing-dimensions"
            )
            final_summary["next_steps"].append("2. Điền thông tin thiếu vào file Excel")
            final_summary["next_steps"].append("3. Upload file đã điền vào temp tables")
            final_summary["next_steps"].append(
                "4. Chạy endpoint /import-missing-dimensions để cập nhật"
            )
            final_summary["next_steps"].append(
                "5. Chạy lại /revalidate-error-data để xử lý lại errors"
            )
        else:
            final_summary["next_steps"].append(
                "✅ Không có dữ liệu thiếu, workflow hoàn tất!"
            )

        print("🎉 Complete workflow hoàn thành!")

        return {
            "success": True,
            "message": "Complete workflow đã hoàn thành thành công",
            "data": final_summary,
        }

    except Exception as e:
        error_msg = f"Lỗi complete workflow: {str(e)}"
        print(f"💥 {error_msg}")
        logging.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_msg
        )
