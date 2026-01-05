import pandas as pd
import logging
import os
import shutil
from typing import Dict, List, Any, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.types import UnicodeText
import re
import datetime
from pathlib import Path


class ExcelBatchProcessor:
    """
    Xử lý batch import dữ liệu Excel

    Args:
        db (Session): Session của database

    Returns:
        Dict[str, Any]: Kết quả xử lý
    """

    def __init__(self, db: Session):
        self.db = db

        # Cấu hình từ notebook
        self.json_data = {
            "MN": ["toan cang"],  # miền nam - chứa tên biến
            "MB": ["NAA"],  # miền bắc - bắt đầu
            "MT": ["CV1"],  # miền trung - bắt đầu
        }

        # Danh sách các airport codes
        self.search_list = ["THD", "HPH", "HAN", "VDO", "VDH", "VII", "DIN"]

        # Các cột cần extract
        self.columns_to_extract = [
            "flightdate",
            "flightno",
            "actype",
            "route",
            "cgo",
            "mail",
            "seat",
            "adl",
            "chd",
            "totalpax",
            "acregno",
            "source",
            "sheet_name",
        ]

        # Các cột kiểu số thực
        self.numeric_columns = ["cgo", "mail", "adl", "chd", "seat", "totalpax"]

    def find_matching_key(self, text: str) -> Optional[str]:
        """
        Xác định loại file Excel (MN: miền nam, MB: miền bắc, MT: miền trung)

        Args:
            text (str): Chuỗi cần kiểm tra

        Returns:
            str or None: Loại file tìm thấy hoặc None nếu không tìm thấy
        """

        text_lower = text.lower().strip()

        for key, values in self.json_data.items():
            for value in values:
                value_lower = value.lower().strip()

                if key == "MN":
                    if value_lower in text_lower:
                        return key
                else:  # MB, MT
                    if text_lower.startswith(value_lower):
                        return key

        return None

    def convert_to_float(self, value: Any) -> float:
        """
        Chuyển text thành số thực

        Args:
            value (Any): Giá trị cần chuyển đổi

        Returns:
            float: Giá trị số thực hoặc 0.0 nếu không thể chuyển đổi
        """

        try:
            # Convert ',' to '.' if present
            if isinstance(value, str):
                value = value.replace(",", ".")

            # Convert to float, return 0 if not possible
            return float(value) if pd.notnull(value) else 0.0
        except (ValueError, TypeError):
            return 0.0

    def mb_sheet(self, text: str) -> Optional[str]:
        """
        Tìm giá trị đầu tiên trong search_list có chứa trong text

        Args:
            text (str): Chuỗi cần kiểm tra
            search_list (list): Danh sách các giá trị cần tìm

        Returns:
            str or None: Giá trị đầu tiên tìm thấy hoặc None nếu không tìm thấy
        """

        if pd.isna(text):  # Xử lý trường hợp NaN
            return None

        text_str = str(text).upper()

        for value in self.search_list:
            if str(value).upper() in text_str:
                return value

        return None

    def process_excel_file(self, file_path: str, file_name: str) -> pd.DataFrame:
        """
        Xử lý một file Excel

        Args:
            file_path (str): Đường dẫn đến file Excel
            file_name (str): Tên file Excel

        Returns:
            pd.DataFrame: DataFrame chứa dữ liệu đã xử lý
        """

        combined_data = []

        try:
            # Determine file type
            file_type = self.find_matching_key(file_name)
            if not file_type:
                logging.error(f"Không thể xác định loại file: {file_name}")
                return pd.DataFrame()

            if file_type == "MN":
                # Process MN (Miền Nam) files
                combined_data = self._process_mn_file(file_path, file_name)

            elif file_type == "MT":
                # Process MT (Miền Trung) files
                combined_data = self._process_mt_file(file_path, file_name)

            elif file_type == "MB":
                # Process MB (Miền Bắc) files
                combined_data = self._process_mb_file(file_path, file_name)

            # Combine all DataFrames
            if combined_data:
                final_df = pd.concat(combined_data, ignore_index=True)
                return final_df
            else:
                logging.warning(
                    f"Không có dữ liệu được trích xuất từ file: {file_name}"
                )
                return pd.DataFrame()

        except Exception as e:
            logging.error(f"Lỗi xử lý file {file_name}: {e}")
            return pd.DataFrame()

    def _process_mn_file(self, file_path: str, file_name: str) -> List[pd.DataFrame]:
        """
        Xử lý file MN (Miền Nam)

        Args:
            file_path (str): Đường dẫn đến file Excel
            file_name (str): Tên file Excel

        Returns:
            List[pd.DataFrame]: Danh sách các DataFrame đã xử lý
        """

        combined_data = []

        try:
            # Read all sheets in the Excel file
            excel_sheets = pd.read_excel(file_path, sheet_name=None)

            # Loop through each sheet
            for sheet_name, df_sheet in excel_sheets.items():
                # Process only sheets with at least 1 character
                if len(sheet_name) >= 1:
                    processed_df = self._process_sheet_common(
                        df_sheet, file_name, sheet_name
                    )
                    if not processed_df.empty:
                        combined_data.append(processed_df)

        except Exception as e:
            logging.error(f"Lỗi xử lý file MN {file_name}: {e}")

        return combined_data

    def _process_mt_file(self, file_path: str, file_name: str) -> List[pd.DataFrame]:
        """
        Xử lý file MT (Miền Trung)

        Args:
            file_path (str): Đường dẫn đến file Excel
            file_name (str): Tên file Excel

        Returns:
            List[pd.DataFrame]: Danh sách các DataFrame đã xử lý
        """

        combined_data = []

        try:
            # Read all sheets in the Excel file
            excel_sheets = pd.read_excel(file_path, sheet_name=None)

            for sheet_name, df_sheet in excel_sheets.items():
                # Process only sheets with at least 1 character
                if len(sheet_name) >= 1:
                    processed_df = self._process_sheet_common(
                        df_sheet, file_name, sheet_name
                    )
                    if not processed_df.empty:
                        combined_data.append(processed_df)

        except Exception as e:
            logging.error(f"Lỗi xử lý file MT {file_name}: {e}")

        return combined_data

    def _process_mb_file(self, file_path: str, file_name: str) -> List[pd.DataFrame]:
        """
        Xử lý file MB (Miền Bắc)

        Args:
            file_path (str): Đường dẫn đến file Excel
            file_name (str): Tên file Excel

        Returns:
            List[pd.DataFrame]: Danh sách các DataFrame đã xử lý
        """

        combined_data = []

        try:
            print(f"MB: file {file_name}")
            # Read all sheets in the Excel file
            excel_sheets = pd.read_excel(file_path, sheet_name=None)

            for sheet_name, df_sheet in excel_sheets.items():
                # Process only sheets with at least 1 character
                if len(sheet_name) >= 1:
                    # Lowercase column names
                    df_sheet.columns = df_sheet.columns.str.lower()

                    # Add missing columns with None/NaN
                    for col in self.columns_to_extract:
                        if col not in df_sheet.columns:
                            df_sheet[col] = pd.NA

                    # Add metadata columns
                    df_sheet["source"] = file_name

                    # Handle specific column data types and fill missing values
                    df_sheet["flightdate"] = df_sheet["flightdate"].ffill()
                    df_sheet["flightno"] = df_sheet["flightno"].fillna("").astype(str)
                    df_sheet["actype"] = df_sheet["actype"].fillna("").astype(str)
                    df_sheet["route"] = df_sheet["route"].fillna("").astype(str)

                    # For MB, sheet_name is derived from route
                    df_sheet["sheet_name"] = df_sheet["route"].apply(
                        lambda x: self.mb_sheet(x)
                    )

                    # Convert numeric columns using custom conversion function
                    for col in self.numeric_columns:
                        df_sheet[col] = df_sheet[col].apply(self.convert_to_float)

                    # Extract specified columns
                    extracted_df = df_sheet[self.columns_to_extract].copy()
                    combined_data.append(extracted_df)

        except Exception as e:
            logging.error(f"Lỗi xử lý file MB {file_name}: {e}")

        return combined_data

    def _process_sheet_common(
        self, df_sheet: pd.DataFrame, file_name: str, sheet_name: str
    ) -> pd.DataFrame:
        """
        Xử lý chung cho các sheet (MN, MT)

        Args:
            df_sheet (pd.DataFrame): DataFrame chứa dữ liệu của sheet
            file_name (str): Tên file Excel
            sheet_name (str): Tên sheet

        Returns:
            pd.DataFrame: DataFrame chứa dữ liệu đã xử lý
        """

        try:
            # Lowercase column names
            df_sheet.columns = df_sheet.columns.str.lower()

            # Add missing columns with None/NaN
            for col in self.columns_to_extract:
                if col not in df_sheet.columns:
                    df_sheet[col] = pd.NA

            # Add metadata columns
            df_sheet["source"] = file_name
            df_sheet["sheet_name"] = sheet_name

            # Handle specific column data types and fill missing values
            df_sheet["flightdate"] = df_sheet["flightdate"].ffill()
            df_sheet["flightno"] = df_sheet["flightno"].fillna("").astype(str)
            df_sheet["actype"] = df_sheet["actype"].fillna("").astype(str)
            df_sheet["route"] = df_sheet["route"].fillna("").astype(str)

            # Convert numeric columns using custom conversion function
            for col in self.numeric_columns:
                try:
                    df_sheet[col] = df_sheet[col].apply(self.convert_to_float)
                    df_sheet[col] = df_sheet[col].fillna(0)
                except Exception as e:
                    logging.error(
                        f"Lỗi xử lý cột số thực '{col}' trong sheet '{sheet_name}' từ file '{file_name}': {e}"
                    )
                    df_sheet[col] = df_sheet[col].fillna(0)

            # Extract specified columns
            extracted_df = df_sheet[self.columns_to_extract].copy()
            return extracted_df

        except Exception as e:
            logging.error(f"Lỗi xử lý sheet '{sheet_name}' từ file '{file_name}': {e}")
            return pd.DataFrame()

    def is_file_imported(self, file_name: str) -> bool:
        """
        Kiểm tra file đã import chưa

        Args:
            file_name (str): Tên file Excel

        Returns:
            bool: True nếu file đã import, False nếu không
        """

        try:
            query = text("SELECT 1 FROM import_log WHERE file_name = :file_name")
            result = self.db.execute(query, {"file_name": file_name}).fetchone()
            return result is not None
        except Exception as e:
            logging.error(f"Lỗi kiểm tra file đã import: {e}")
            return False

    def mark_file_imported(self, file_name: str, source_type: str, row_count: int):
        """
        Đánh dấu file đã import

        Args:
            file_name (str): Tên file Excel
            source_type (str): Loại source
            row_count (int): Số lượng dòng

        Returns:
            None
        """

        try:
            insert_query = text(
                """
                INSERT INTO import_log (file_name, source_type, row_count)
                VALUES (:file_name, :source_type, :row_count)
            """
            )
            self.db.execute(
                insert_query,
                {
                    "file_name": file_name,
                    "source_type": source_type,
                    "row_count": row_count,
                },
            )
            print(f"Đã đánh dấu file đã import: {file_name}")
        except Exception as e:
            logging.error(f"Lỗi đánh dấu file đã import: {e}")
            raise e

    def batch_import_files(
        self, data_folder: str, destination_folder: str
    ) -> Dict[str, Any]:
        """
        Import batch các file Excel từ folder

        Args:
            data_folder (str): Đường dẫn đến folder chứa các file Excel
            destination_folder (str): Đường dẫn đến folder chứa các file Excel đã import

        Returns:
            Dict[str, Any]: Kết quả xử lý
        """

        results = {
            "processed_files": 0,
            "total_rows": 0,
            "skipped_files": 0,
            "errors": [],
            "file_details": [],
        }

        try:
            # Ensure destination folder exists
            os.makedirs(destination_folder, exist_ok=True)

            # Process each file in the data folder
            for file_name in os.listdir(data_folder):
                if not self._is_excel_file(file_name):
                    continue

                try:
                    # Check if file already imported
                    if self.is_file_imported(file_name):
                        print(f"{file_name} đã được import trước đó, bỏ qua.")
                        results["skipped_files"] += 1
                        continue

                    print(f"Đang xử lý: {file_name}")

                    # Process Excel file
                    file_path = os.path.join(data_folder, file_name)
                    df = self.process_excel_file(file_path, file_name)

                    if df.empty:
                        results["errors"].append(
                            f"Không có dữ liệu được trích xuất từ file {file_name}"
                        )
                        continue

                    row_count = len(df)
                    print(f"Đã trích xuất {row_count} dòng từ file {file_name}")

                    # Save to database
                    self._save_to_database(df)

                    # Mark file as imported
                    self.mark_file_imported(file_name, "batch_excel", row_count)

                    # Move processed file to destination folder
                    shutil.move(file_path, os.path.join(destination_folder, file_name))

                    print(f"Đã import file: {file_name}")

                    results["processed_files"] += 1
                    results["total_rows"] += row_count
                    results["file_details"].append(
                        {"file_name": file_name, "rows": row_count}
                    )

                except Exception as e:
                    error_msg = f"Lỗi xử lý file {file_name}: {e}"
                    print(error_msg)
                    results["errors"].append(error_msg)

            # Commit all changes
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            results["errors"].append(f"Lỗi batch import: {str(e)}")

        return results

    def _is_excel_file(self, file_name: str) -> bool:
        """
        Kiểm tra có phải file Excel không

        Args:
            file_name (str): Tên file Excel

        Returns:
            bool: True nếu là file Excel, False nếu không
        """

        excel_extensions = [".xlsx", ".xls"]
        return any(file_name.lower().endswith(ext) for ext in excel_extensions)

    def _save_to_database(self, df: pd.DataFrame):
        """
        Lưu DataFrame vào database sử dụng bulk insert

        Args:
            df (pd.DataFrame): DataFrame cần lưu

        Returns:
            None
        """

        try:
            # Filter: chỉ lưu các row có flightno và actype không null
            filtered_df = df[df["flightno"].notna() & df["actype"].notna()][
                [
                    "flightdate",
                    "flightno",
                    "route",
                    "actype",
                    "seat",
                    "adl",
                    "chd",
                    "cgo",
                    "mail",
                    "totalpax",
                    "source",
                    "acregno",
                    "sheet_name",
                ]
            ]

            # Convert DataFrame to SQL
            filtered_df.to_sql(
                "flight_raw",
                con=self.db.bind,
                if_exists="append",
                index=False,
                dtype={
                    "source": UnicodeText(),
                    "sheet_name": UnicodeText(),
                    "flightdate": UnicodeText(),
                },
            )

            # Log số lượng rows đã lọc
            original_count = len(df)
            filtered_count = len(filtered_df)
            if original_count > filtered_count:
                logging.info(
                    f"📊 Đã lọc {original_count - filtered_count} rows thiếu flightno/actype"
                )

        except Exception as e:
            logging.error(f"Lỗi lưu vào database: {e}")
            raise e

    def run_data_cleaning_stored_procedure(self):
        """
        Chạy stored procedure để làm sạch dữ liệu

        Returns:
            None
        """

        try:
            print("Chạy stored procedure làm sạch dữ liệu...")
            self.db.execute(text("EXEC usp_CleanAndProcessFlightData"))

            print("Chạy stored procedure log missing dimensions...")
            self.db.execute(text("EXEC usp_LogMissingDimensions"))

            self.db.commit()
            print("Làm sạch dữ liệu hoàn tất!")
        except Exception as e:
            self.db.rollback()
            logging.error(f"Lỗi chạy stored procedure làm sạch dữ liệu: {e}")
            raise e

    def run_missing_dimensions_import(self):
        """
        Chạy stored procedure để import missing dimensions

        Returns:
            None
        """

        try:
            print("Chạy stored procedure import missing dimensions...")
            self.db.execute(text("EXEC usp_ImportAndUpdateMissingDimensions"))
            self.db.commit()
            print("Import missing dimensions hoàn tất!")
        except Exception as e:
            self.db.rollback()
            logging.error(f"Lỗi chạy stored procedure import missing dimensions: {e}")
            raise e

    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Lấy tóm tắt quá trình xử lý dữ liệu theo schema thực tế (TOÀN BỘ DATABASE)

        Returns:
            Dict[str, Any]: Tóm tắt quá trình xử lý dữ liệu
        """

        try:
            # Get total records in each table
            raw_count_result = self.db.execute(
                text("SELECT COUNT(*) FROM flight_raw")
            ).fetchone()

            processed_count_result = self.db.execute(
                text("SELECT COUNT(*) FROM flight_data_chot")
            ).fetchone()

            error_count_result = self.db.execute(
                text("SELECT COUNT(*) FROM error_table")
            ).fetchone()

            missing_actype_result = self.db.execute(
                text(
                    "SELECT COUNT(*) FROM Missing_Dimensions_Log WHERE Type = 'ACTYPE'"
                )
            ).fetchone()

            missing_route_result = self.db.execute(
                text("SELECT COUNT(*) FROM Missing_Dimensions_Log WHERE Type = 'ROUTE'")
            ).fetchone()

            # Get imported files count
            imported_files_result = self.db.execute(
                text("SELECT COUNT(*) FROM import_log")
            ).fetchone()

            return {
                "raw_records": raw_count_result[0] if raw_count_result else 0,
                "processed_records": (
                    processed_count_result[0] if processed_count_result else 0
                ),
                "error_records": error_count_result[0] if error_count_result else 0,
                "missing_actypes": (
                    missing_actype_result[0] if missing_actype_result else 0
                ),
                "missing_routes": (
                    missing_route_result[0] if missing_route_result else 0
                ),
                "imported_files": (
                    imported_files_result[0] if imported_files_result else 0
                ),
            }

        except Exception as e:
            logging.error(f"Lỗi lấy tóm tắt quá trình xử lý dữ liệu: {e}")
            return {
                "raw_records": 0,
                "processed_records": 0,
                "error_records": 0,
                "missing_actypes": 0,
                "missing_routes": 0,
                "imported_files": 0,
            }

    def get_current_session_summary(self, source_files: List[str]) -> Dict[str, Any]:
        """
        Lấy tóm tắt quá trình xử lý CHỈ CHO BATCH HIỆN TẠI (filtered by source files)

        Args:
            source_files: Danh sách tên files đã xử lý trong session hiện tại

        Returns:
            Dict[str, Any]: Tóm tắt quá trình xử lý của batch hiện tại
        """
        try:
            if not source_files:
                return {
                    "raw_records": 0,
                    "processed_records": 0,
                    "error_records": 0,
                    "missing_actypes": 0,
                    "missing_routes": 0,
                    "imported_files": 0,
                }

            # Build IN clause for SQL query
            files_placeholder = ", ".join(
                [f":file_{i}" for i in range(len(source_files))]
            )
            files_params = {f"file_{i}": file for i, file in enumerate(source_files)}

            # Get records count from flight_raw for current batch
            raw_count_result = self.db.execute(
                text(
                    f"SELECT COUNT(*) FROM flight_raw WHERE source IN ({files_placeholder})"
                ),
                files_params,
            ).fetchone()

            # Get records count from flight_data_chot for current batch
            processed_count_result = self.db.execute(
                text(
                    f"SELECT COUNT(*) FROM flight_data_chot WHERE source IN ({files_placeholder})"
                ),
                files_params,
            ).fetchone()

            # Get records count from error_table for current batch
            error_count_result = self.db.execute(
                text(
                    f"SELECT COUNT(*) FROM error_table WHERE source IN ({files_placeholder})"
                ),
                files_params,
            ).fetchone()

            # Get missing actypes from Missing_Dimensions_Log for current batch
            # Note: Missing_Dimensions_Log có thể không có source column,
            # nên ta lấy từ error_table của batch hiện tại
            missing_actype_result = self.db.execute(
                text(
                    f"""
                    SELECT COUNT(DISTINCT actype) 
                    FROM error_table 
                    WHERE source IN ({files_placeholder})
                    AND Is_InvalidActypeSeat = 1
                    AND actype IS NOT NULL
                """
                ),
                files_params,
            ).fetchone()

            # Get missing routes from error_table for current batch
            missing_route_result = self.db.execute(
                text(
                    f"""
                    SELECT COUNT(DISTINCT route) 
                    FROM error_table 
                    WHERE source IN ({files_placeholder})
                    AND Is_InvalidRoute = 1
                    AND route IS NOT NULL
                """
                ),
                files_params,
            ).fetchone()

            # Get imported files count for current batch
            imported_files_result = self.db.execute(
                text(
                    f"SELECT COUNT(*) FROM import_log WHERE file_name IN ({files_placeholder})"
                ),
                files_params,
            ).fetchone()

            return {
                "raw_records": raw_count_result[0] if raw_count_result else 0,
                "processed_records": (
                    processed_count_result[0] if processed_count_result else 0
                ),
                "error_records": error_count_result[0] if error_count_result else 0,
                "missing_actypes": (
                    missing_actype_result[0] if missing_actype_result else 0
                ),
                "missing_routes": (
                    missing_route_result[0] if missing_route_result else 0
                ),
                "imported_files": (
                    imported_files_result[0] if imported_files_result else 0
                ),
            }

        except Exception as e:
            logging.error(f"Lỗi lấy tóm tắt batch hiện tại: {e}")
            return {
                "raw_records": 0,
                "processed_records": 0,
                "error_records": 0,
                "missing_actypes": 0,
                "missing_routes": 0,
                "imported_files": 0,
            }
