# 📋 **FLOW XỬ LÝ UPLOAD FILES**

> **Mô tả**: API upload và xử lý multiple Excel files theo logic notebook với complete workflow từ raw data đến clean data và error handling.

---

## 🚀 **Phase 1: INITIALIZATION & SETUP**

### **1.1 Request Reception**

```http
POST: /data-processing/upload-files
Content-Type: multipart/form-data
Files: List[UploadFile] (Excel files .xlsx/.xls)
```

### **1.2 Service Initialization**

```python
processor = ExcelBatchProcessor(db)
results = {
    "processed_files": 0,     # Số file đã xử lý thành công
    "total_rows": 0,          # Tổng số rows đã insert
    "skipped_files": 0,       # Số file đã import trước đó
    "errors": [],             # Danh sách lỗi
    "file_details": [],       # Chi tiết từng file
    "processing_summary": {}, # Thống kê sau khi process
}
```

### **1.3 Temporary Directory Setup**

```python
with tempfile.TemporaryDirectory() as temp_dir:
    # Tạo thư mục tạm để lưu uploaded files
    # Auto cleanup khi exit
```

---

## 📂 **Phase 2: FILE PROCESSING LOOP**

### **2.1 File Validation & Save**

#### **Validation Logic:**

```python
for file in files:
    # ✅ Kiểm tra extension
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        results["errors"].append(f"File {file.filename} không phải là Excel file")
        continue
```

#### **File Save:**

```python
# 💾 Save file to temp directory
file_path = os.path.join(temp_dir, file.filename)
with open(file_path, "wb") as buffer:
    content = await file.read()
    buffer.write(content)
```

### **2.2 Duplicate Check**

```python
# 🔍 Check import log table
if processor.is_file_imported(file.filename):
    print(f"⏭️ File {file.filename} đã được import trước đó")
    results["skipped_files"] += 1
    continue
```

**SQL Query:**

```sql
SELECT 1 FROM import_log WHERE file_name = :file_name
```

### **2.3 File Type Classification**

#### **Classification Logic (theo notebook):**

```python
file_type = processor.find_matching_key(file.filename)
```

| **File Type** | **Điều kiện** | **Mô tả** |
|---------------|---------------|-----------|
| **MN** (Miền Nam) | Chứa chuỗi `"toan cang"` | Files từ miền Nam |
| **MB** (Miền Bắc) | Bắt đầu với `"NAA"` | Files từ miền Bắc |
| **MT** (Miền Trung) | Bắt đầu với `"CV1"` | Files từ miền Trung |

---

## 📊 **Phase 3: EXCEL DATA EXTRACTION**

### **3.1 Excel File Processing**

```python
df = processor.process_excel_file(file_path, file.filename)
```

### **3.2 Read Excel Sheets**

```python
excel_sheets = pd.read_excel(file_path, sheet_name=None)
# Đọc tất cả sheets trong file Excel
```

### **3.3 Process theo File Type**

#### **🔸 MN (Miền Nam) Processing:**

```python
for sheet_name, df_sheet in excel_sheets.items():
    if len(sheet_name) >= 1:  # Process tất cả sheets
        # Lowercase column names
        df_sheet.columns = df_sheet.columns.str.lower()
        
        # Add metadata
        df_sheet['source'] = file_name
        df_sheet['sheet_name'] = sheet_name  # Sử dụng sheet name gốc
        
        # Data processing...
```

#### **🔸 MB (Miền Bắc) Processing:**

```python
for sheet_name, df_sheet in excel_sheets.items():
    # Special logic: sheet_name từ route column
    df_sheet['sheet_name'] = df_sheet['route'].apply(
        lambda x: mb_sheet(x, search_list)
    )
    # mb_sheet() tìm airport codes trong route:
    # ["THD", "HPH", "HAN", "VDO", "VDH", "VII", "DIN"]
```

#### **🔸 MT (Miền Trung) Processing:**

```python
for sheet_name, df_sheet in excel_sheets.items():
    df_sheet['sheet_name'] = sheet_name  # Sử dụng sheet name gốc
```

### **3.4 Column Processing**

#### **Ensure Required Columns:**

```python
columns_to_extract = [
    'flightdate', 'flightno', 'actype', 'route',
    'cgo', 'mail', 'seat', 'adl', 'chd', 'totalpax',
    'acregno', 'source', 'sheet_name'
]

# Add missing columns với NaN
for col in columns_to_extract:
    if col not in df_sheet.columns:
        df_sheet[col] = pd.NA
```

#### **Data Type Handling:**

```python
# Handle specific data types
df_sheet['flightdate'] = df_sheet['flightdate'].ffill()  # Forward fill
df_sheet['flightno'] = df_sheet['flightno'].fillna('').astype(str)
df_sheet['actype'] = df_sheet['actype'].fillna('').astype(str)
df_sheet['route'] = df_sheet['route'].fillna('').astype(str)
```

#### **Numeric Conversion:**

```python
numeric_columns = ['cgo', 'mail', 'adl', 'chd', 'seat', 'totalpax']

for col in numeric_columns:
    # Custom conversion function
    df_sheet[col] = df_sheet[col].apply(convert_to_float)
    df_sheet[col] = df_sheet[col].fillna(0)
```

**`convert_to_float()` Function:**

```python
def convert_to_float(value):
    try:
        if isinstance(value, str):
            value = value.replace(",", ".")  # Handle European decimal format
        return float(value) if pd.notnull(value) else 0.0
    except (ValueError, TypeError):
        return 0.0
```

### **3.5 Final Data Extraction**

```python
# Extract only required columns
extracted_df = df_sheet[columns_to_extract].copy()
combined_data.append(extracted_df)

# Combine all sheets
final_df = pd.concat(combined_data, ignore_index=True)
return final_df
```

---

## 💾 **Phase 4: DATABASE OPERATIONS**

### **4.1 Save to flight_raw Table**

```python
processor._save_to_database(df)
```

#### **Database Insert Logic:**

```python
# Convert DataFrame to SQL
df.to_sql(
    'flight_raw', 
    con=self.db.bind, 
    if_exists='append', 
    index=False,
    dtype={
        col: UnicodeText 
        for col in df.select_dtypes(include=['object']).columns
    }
)
```

#### **SQL Structure:**

```sql
INSERT INTO flight_raw (
    flightdate, flightno, route, actype, seat, adl, chd, 
    cgo, mail, totalpax, source, acregno, sheet_name, 
    int_dom, created_at
) VALUES (
    '2024-01-15', 'VN123', 'SGN-HAN', 'A321', 180, 150, 10,
    2.5, 0.8, 160, 'file1.xlsx', 'VN-A123', 'SGN', NULL, SYSDATETIME()
)
```

### **4.2 Mark File as Imported**

```python
processor.mark_file_imported(file.filename, file_type, row_count)
```

#### **Import Log Entry:**

```sql
INSERT INTO import_log (file_name, source_type, row_count, import_date)
VALUES ('filename.xlsx', 'MN', 1500, SYSDATETIME())
```

### **4.3 Update Processing Results**

```python
results["processed_files"] += 1
results["total_rows"] += row_count
results["file_details"].append({
    "file_name": file.filename,
    "file_type": file_type,  # MN/MB/MT
    "rows": row_count,
})

print(f"✅ Đã lưu {row_count} bản ghi từ file {file.filename}")
```

---

## 🧹 **Phase 5: DATA CLEANING & PROCESSING**

### **5.1 Commit Raw Data**

```python
db.commit()
print(f"💾 Đã commit {results['total_rows']} bản ghi raw data")
```

### **5.2 Run Stored Procedures** *(nếu có files được processed)*

#### **Step 5.2.1: usp_CleanAndProcessFlightData**

```python
print("1️⃣ Chạy stored procedure: usp_CleanAndProcessFlightData")
processor.run_data_cleaning_stored_procedure()
```

**Stored Procedure Tasks:**

| **Step** | **Action** | **Description** |
|----------|------------|-----------------|
| 1 | **Prepare Raw Data** | Update `totalpax = adl + chd` trong `flight_raw` |
| 2 | **Load to Staging** | Insert từ `flight_raw` → `flight_clean_data_stg` |
| 3 | **Date Validation** | Validate và format `flightdate` |
| 4 | **Business Validation** | Check passengers, cargo, routes, actypes |
| 5 | **Load to Main** | Insert clean data → `flight_data_chot` |
| 6 | **Error Handling** | Move invalid data → `error_table` |
| 7 | **Missing Dimensions** | Log missing actypes/routes → `Missing_Dimensions_Log` |

#### **Step 5.2.2: usp_CleanAndValidateFlightData**

```python
print("2️⃣ Chạy stored procedure: usp_CleanAndValidateFlightData")
from sqlalchemy import text
db.execute(text("EXEC usp_CleanAndValidateFlightData"))
db.commit()
```

**Validation Tasks:**

- **Re-validate error data**: Check lại data trong `error_table`
- **Move valid data back**: Chuyển valid records từ `error_table` → `flight_data_chot`
- **Update error flags**: Cập nhật validation flags

### **5.3 Get Processing Summary**

```python
results["processing_summary"] = processor.get_processing_summary()
```

#### **Summary Queries:**

```sql
-- Raw records count
SELECT COUNT(*) FROM flight_raw

-- Processed records count  
SELECT COUNT(*) FROM flight_data_chot

-- Error records count
SELECT COUNT(*) FROM error_table

-- Missing actypes count
SELECT COUNT(*) FROM Missing_Dimensions_Log WHERE Type = 'ACTYPE'

-- Missing routes count
SELECT COUNT(*) FROM Missing_Dimensions_Log WHERE Type = 'ROUTE'

-- Imported files count
SELECT COUNT(DISTINCT file_name) FROM import_log
```

---

## 📤 **Phase 6: RESPONSE PREPARATION**

### **6.1 Success Message Construction**

```python
success_message = f"Đã xử lý thành công {results['processed_files']} file với tổng {results['total_rows']} bản ghi"

if results["skipped_files"] > 0:
    success_message += f" (bỏ qua {results['skipped_files']} file đã import)"

print(f"🎉 {success_message}")
```

### **6.2 Final API Response**

```json
{
    "success": true,
    "message": "Đã xử lý thành công 3 file với tổng 1500 bản ghi (bỏ qua 1 file đã import)",
    "processed_files": 3,
    "total_rows": 1500,
    "skipped_files": 1,
    "errors": [],
    "file_details": [
        {
            "file_name": "MN_toan_cang_data.xlsx",
            "file_type": "MN", 
            "rows": 500
        },
        {
            "file_name": "NAA_flight_data.xlsx",
            "file_type": "MB",
            "rows": 600
        },
        {
            "file_name": "CV1_central_data.xlsx", 
            "file_type": "MT",
            "rows": 400
        }
    ],
    "processing_summary": {
        "raw_records": 1500,
        "processed_records": 1400,
        "error_records": 100,
        "missing_actypes": 5,
        "missing_routes": 3,
        "imported_files": 4
    }
}
```

---

## 🚨 **Error Handling & Edge Cases**

### **Global Error Handling**

```python
try:
    # ... entire workflow ...
except Exception as e:
    db.rollback()  # Rollback tất cả database changes
    error_msg = f"Lỗi upload files: {str(e)}"
    print(f"💥 {error_msg}")
    logging.error(error_msg)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=error_msg
    )
```

### **File-level Error Scenarios**

| **Scenario** | **Action** | **Impact** |
|--------------|------------|------------|
| **Non-Excel File** | Add to `errors`, continue | Không dừng process |
| **File đã Import** | Tăng `skipped_files`, continue | Không re-process |
| **Unknown File Type** | Add to `errors`, continue | File không được xử lý |
| **Excel Read Error** | Add to `errors`, continue | File bị corrupt/format sai |
| **Database Error** | Add to `errors`, continue | Lỗi constraint/data |
| **Stored Procedure Error** | Add to `errors`, return success | Không fail toàn bộ |

### **Error Response Example**

```json
{
    "success": true,
    "message": "Đã xử lý thành công 2 file với tổng 1000 bản ghi",
    "processed_files": 2,
    "total_rows": 1000,
    "skipped_files": 1,
    "errors": [
        "File report.pdf không phải là Excel file",
        "Không thể xác định loại file: unknown_format.xlsx",
        "Lỗi xử lý file corrupted.xlsx: File không đọc được",
        "Lỗi stored procedure: Missing foreign key constraint"
    ],
    "file_details": [...],
    "processing_summary": {...}
}
```

---

## 🔗 **Database Tables Flow**

### **Data Flow Diagram**

```
📤 Upload Files
    ↓
📊 Excel Processing  
    ↓
🗄️ flight_raw (Raw data storage)
    ↓
📝 import_log (File tracking)
    ↓
🧹 usp_CleanAndProcessFlightData
    ↓
🗂️ flight_clean_data_stg (Staging)
    ↓
✅ flight_data_chot (Clean data) 
❌ error_table (Invalid data)
⚠️ Missing_Dimensions_Log (Missing refs)
    ↓
🔄 usp_CleanAndValidateFlightData
    ↓
📊 Processing Summary
```

### **Tables Involved**

| **Table** | **Purpose** | **Usage** |
|-----------|-------------|-----------|
| `flight_raw` | Raw Excel data storage | Insert phase |
| `import_log` | File import tracking | Duplicate prevention |
| `flight_clean_data_stg` | Staging for validation | Temp processing |
| `flight_data_chot` | Main clean data table | Final validated data |
| `error_table` | Invalid data storage | Error records |
| `Missing_Dimensions_Log` | Missing references log | Data quality tracking |

---

## ⚡ **Performance Considerations**

### **Optimizations Implemented**

- ✅ **Batch Processing**: Multiple files trong single transaction
- ✅ **Temp Directory**: Auto cleanup để tránh disk space issues  
- ✅ **Duplicate Prevention**: Check `import_log` trước khi process
- ✅ **Error Isolation**: Lỗi 1 file không ảnh hưởng files khác
- ✅ **Transaction Management**: Commit theo phases để tránh long locks
- ✅ **Pandas Optimization**: `to_sql()` với proper dtypes

### **Scalability Notes**

- **Memory**: Large Excel files có thể consume significant memory
- **Transaction Size**: Very large batches có thể cause timeout
- **Disk Space**: Temp files cần sufficient disk space
- **Database Locks**: Long-running transactions có thể block other operations

---

## 🎯 **Success Criteria**

### **Complete Success**

- ✅ Tất cả files processed successfully
- ✅ Không có errors
- ✅ Processing summary có data đầy đủ
- ✅ Stored procedures chạy thành công

### **Partial Success**

- ✅ Một số files processed successfully
- ⚠️ Có errors nhưng không critical
- ✅ Processing summary reflective of actual data
- ⚠️ Stored procedures có thể có warnings

### **Failure Scenarios**

- ❌ Database connection issues
- ❌ Permissions problems
- ❌ Disk space insufficient
- ❌ Critical stored procedure failures

---

## 📚 **Related Endpoints**

### **Follow-up Actions**

- **`/export-missing-dimensions`**: Tạo Excel file cho missing data
- **`/import-missing-dimensions`**: Import data đã bổ sung
- **`/revalidate-error-data`**: Re-process error records
- **`/processing-summary`**: Get latest processing stats
- **`/complete-workflow`**: Full workflow với missing data handling

### **Monitoring & Management**

- **`/stats`**: Overall system statistics
- **`/flight-data`**: Query processed flight data
- **`/missing-dimensions`**: List missing references
- **`/clear-flight-data`**: Reset data (development only)

---

*Tài liệu này mô tả complete flow của API `/upload-files` theo implementation thực tế và logic từ notebook MSSQL_Airline.ipynb.*
