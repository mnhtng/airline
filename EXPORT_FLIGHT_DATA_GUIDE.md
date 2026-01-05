# Hướng dẫn Export Flight Data - API `/export-flight-data`

## 📋 Tổng quan

API endpoint `/export-flight-data` cho phép xuất dữ liệu chuyến bay trong khoảng thời gian cụ thể ra file Excel. API này sử dụng một SQL query phức tạp với nhiều CTE (Common Table Expressions) để enrichment dữ liệu từ các bảng reference.

---

## 🔌 API Endpoint

### Endpoint Information

- **URL**: `GET /data-processing/export-flight-data`
- **Method**: `GET`
- **Location**: `backend/routes/data_processing.py` (lines 741-984)

### Query Parameters

| Parameter | Type | Format | Required | Description |
|-----------|------|--------|----------|-------------|
| `start_date` | string | `YYYY-MM-DD HH:mm:ss` | ✅ | Ngày giờ bắt đầu |
| `end_date` | string | `YYYY-MM-DD HH:mm:ss` | ✅ | Ngày giờ kết thúc |

### Response Format

```json
{
    "success": true,
    "message": "Export dữ liệu chuyến bay thành công.",
    "data": [
        {
            "area": "MIỀN BẮC",
            "convert_date": "01/01/2024",
            "flightno": "VN123",
            "route": "SGN-HAN",
            "actype": "A321",
            "totalpax": 180,
            "cgo": 1000,
            "mail": 50,
            "acregno": "VN-A123",
            "source": "flight_data_2024.xlsx",
            "sheet_name": "January",
            "seat": "220",
            "int_dom": "DOM",
            "airline_code": "VN",
            "airlines_name": "Vietnam Airlines",
            "airline_nation": "VIETNAM",
            "airline_nation_code": "VN",
            "departure": "SGN",
            "city_departure": "Ho Chi Minh City",
            "country_departure": "Vietnam",
            "arrives": "HAN",
            "city_arrives": "Hanoi",
            "country_arrives": "Vietnam",
            "country_code": "VN",
            "area_code": "VN",
            "flight_type": 1
        }
    ],
    "total_records": 1234
}
```

---

## 🏗️ Kiến trúc SQL Query

SQL query được chia thành 5 phần chính (CTEs):

### 1. `SECTOR_DOM` - Chuẩn hóa Routes Nội địa

```sql
WITH SECTOR_DOM AS (
    SELECT 
        CASE 
            WHEN LEFT(SECTOR, CHARINDEX('-', SECTOR) - 1) < RIGHT(SECTOR, LEN(SECTOR) - CHARINDEX('-', SECTOR))
                THEN SECTOR
            ELSE RIGHT(SECTOR, LEN(SECTOR) - CHARINDEX('-', SECTOR)) + '-' + LEFT(SECTOR, CHARINDEX('-', SECTOR) - 1)
        END AS ROUTE,
        SECTOR,
        [AREA_LV1],
        [DOM/INT]
    FROM SECTOR_ROUTE_DOM_REF
)
```

**Mục đích**:

- Chuẩn hóa route về dạng `SMALLER_CODE-LARGER_CODE` (ví dụ: `HAN-SGN` → `HAN-SGN` hoặc `SGN-HAN` → `HAN-SGN`)
- Lấy thông tin AREA_LV1 từ bảng reference `SECTOR_ROUTE_DOM_REF`

### 2. `ROUTE_` - Routes Nội địa với Area

```sql
ROUTE_ AS (
    SELECT 
        ROUTE,
        [AREA_LV1] AS AREA
    FROM SECTOR_DOM
    WHERE UPPER(LTRIM(RTRIM([DOM/INT]))) = 'DOM'
    GROUP BY ROUTE, [AREA_LV1]
)
```

**Mục đích**:

- Lọc chỉ lấy domestic routes (DOM)
- Map route với area tương ứng

### 3. `FLIGHT_DATA` - Lọc Flight Data từ FLIGHT_DATA_CHOT

```sql
FLIGHT_DATA AS (
    SELECT 
        *,
        CASE 
            WHEN TOTALPAX = 0 AND (ISNULL(CGO, 0) + ISNULL(MAIL, 0) > 0) THEN 0 
            WHEN TOTALPAX > 0 THEN 1 
        END AS FLIGHT_TYPE  
    FROM FLIGHT_DATA_CHOT
    WHERE TYPE_FILTER > 0 
      AND NOTE IS NULL
      AND CONVERT_DATE >= :start_date
      AND CONVERT_DATE <= :end_date
)
```

**Mục đích**:

- Lọc flight data theo khoảng thời gian (sử dụng `CONVERT_DATE` ở dạng YYYYMMDD)
- Phân loại flight type:
  - `0`: Cargo/mail only flights (không có hành khách)
  - `1`: Passenger flights (có hành khách)
- Chỉ lấy flights hợp lệ (`TYPE_FILTER > 0` và `NOTE IS NULL`)

### 4. `DATA_` - Join với Reference Tables để Enrich Data

```sql
DATA_ AS (
    SELECT
        -- Chuẩn hóa route
        CASE 
            WHEN LEFT(F.ROUTE, CHARINDEX('-', F.ROUTE) - 1) < RIGHT(F.ROUTE, LEN(F.ROUTE) - CHARINDEX('-', F.ROUTE))
                THEN F.ROUTE
            ELSE RIGHT(F.ROUTE, LEN(F.ROUTE) - CHARINDEX('-', F.ROUTE)) + '-' + LEFT(F.ROUTE, CHARINDEX('-', F.ROUTE) - 1)
        END AS ROUTE_SORT,
        F.*,
        LEFT(TRIM(F.FLIGHTNO), 2) AS AIRLINE_CODE,
        A.AIRLINES_NAME,
        A.AIRLINE_NATION,
        LEFT(F.ROUTE, 3) AS DEPARTURE,
        RIGHT(F.ROUTE, 3) AS ARRIVES,
        
        -- Xác định country
        CASE 
            WHEN UPPER(AI.COUNTRY) = 'VIETNAM' AND UPPER(AI1.COUNTRY) = 'VIETNAM' THEN 'VIETNAM'
            WHEN UPPER(AI.COUNTRY) = 'VIETNAM' AND UPPER(AI1.COUNTRY) <> 'VIETNAM' THEN AI1.COUNTRY 
            ELSE AI.COUNTRY
        END AS COUNTRY,
        
        -- Xác định DOM/INT
        CASE 
            WHEN UPPER(AI.COUNTRY) = 'VIETNAM' AND UPPER(AI1.COUNTRY) = 'VIETNAM' THEN 'DOM'
            ELSE 'INT'
        END AS INT_DOM,
        
        -- Xác định country code và area
        CASE 
            WHEN UPPER(C.COUNTRY) = 'VIETNAM' AND UPPER(C1.COUNTRY) = 'VIETNAM' THEN 'VN'
            WHEN UPPER(C.COUNTRY) = 'VIETNAM' AND UPPER(C1.COUNTRY) <> 'VIETNAM' THEN C1.[2_LETTER_CODE]
            ELSE C.[2_LETTER_CODE]
        END AS COUNTRY_CODE,
        
        CASE 
            WHEN UPPER(C.COUNTRY) = 'VIETNAM' AND UPPER(C1.COUNTRY) = 'VIETNAM' THEN 'VN'
            WHEN UPPER(C.COUNTRY) = 'VIETNAM' AND UPPER(C1.COUNTRY) <> 'VIETNAM' THEN C1.[REGION_(VNM)]
            ELSE C.[REGION_(VNM)]
        END AS AREA,
        
        AI.CITY AS CITY_ARRIVES,
        AI.COUNTRY AS COUNTRY_ARRIVES,
        AI1.CITY AS CITY_DEPARTURE,
        AI1.COUNTRY AS COUNTRY_DEPARTURE,
        C2.[2_LETTER_CODE] AS AIRLINE_NATION_CODE
        
    FROM FLIGHT_DATA F
    LEFT JOIN AIRLINE_REF A ON LEFT(F.FLIGHTNO, 2) = A.CARRIER
    LEFT JOIN AIRPORT_REF AI ON AI.IATACODE = RIGHT(F.ROUTE, 3)
    LEFT JOIN AIRPORT_REF AI1 ON AI1.IATACODE = LEFT(F.ROUTE, 3)
    LEFT JOIN COUNTRY_REF C ON AI.COUNTRY = C.COUNTRY
    LEFT JOIN COUNTRY_REF C1 ON AI1.COUNTRY = C1.COUNTRY
    LEFT JOIN COUNTRY_REF C2 ON C2.COUNTRY = A.AIRLINE_NATION
)
```

**Bảng Reference được sử dụng**:

- `AIRLINE_REF`: Thông tin hãng bay
- `AIRPORT_REF`: Thông tin sân bay (departure và arrival)
- `COUNTRY_REF`: Thông tin quốc gia và region

### 5. Final SELECT - Lựa chọn AREA logic

```sql
SELECT  
    CASE 
        WHEN S.ROUTE IS NOT NULL THEN S.AREA 
        ELSE D.AREA 
    END AS AREA,
    D.CONVERT_DATE, 
    D.FLIGHTNO, 
    D.ROUTE, 
    D.ACTYPE, 
    D.TOTALPAX, 
    D.CGO, 
    D.MAIL, 
    D.ACREGNO, 
    D.SOURCE, 
    D.SHEET_NAME, 
    D.SEAT, 
    D.INT_DOM,
    D.AIRLINE_CODE, 
    D.AIRLINES_NAME, 
    D.AIRLINE_NATION, 
    D.AIRLINE_NATION_CODE,
    D.DEPARTURE, 
    D.CITY_DEPARTURE, 
    D.COUNTRY_DEPARTURE,
    D.ARRIVES, 
    D.CITY_ARRIVES, 
    D.COUNTRY_ARRIVES,
    D.COUNTRY_CODE, 
    D.AREA AS AREA_CODE,
    D.FLIGHT_TYPE
FROM DATA_ AS D
LEFT JOIN ROUTE_ AS S ON D.ROUTE_SORT = S.ROUTE
ORDER BY D.CONVERT_DATE, D.FLIGHTNO
```

**Logic AREA**:

- Nếu tìm thấy route trong `ROUTE_` (domestic routes từ `SECTOR_ROUTE_DOM_REF`), dùng AREA từ đó
- Ngược lại, dùng AREA tính toán từ `DATA_` CTE

---

## 💻 Backend Implementation

### Backend Location

File: `backend/routes/data_processing.py` (lines 741-984)

### Xử lý Date Parameters

```python
# Parse datetime strings
start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
end = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

# Validate datetime range
if start > end:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Ngày giờ bắt đầu phải trước ngày giờ kết thúc.",
    )

# Convert datetime to YYYYMMDD format (bigint) for CONVERT_DATE comparison
start_yyyymmdd = int(start.strftime("%Y%m%d"))
end_yyyymmdd = int(end.strftime("%Y%m%d"))
```

**Lưu ý**:

- Database lưu `CONVERT_DATE` dưới dạng BIGINT với format YYYYMMDD (ví dụ: 20240115)
- Backend convert từ datetime sang YYYYMMDD để compare

### Xử lý Response

```python
# Convert to list of dictionaries
flight_data = []
for row in rows:
    flight_dict = {
        "area": row.AREA or "",
        "convert_date": (
            row.CONVERT_DATE.strftime("%d/%m/%Y") if row.CONVERT_DATE else ""
        ),
        "flightno": row.FLIGHTNO or "",
        # ... các fields khác
    }
    flight_data.append(flight_dict)
```

---

## 🎨 Frontend Implementation

### Frontend Location

File: `frontend/src/pages/Index.tsx` (lines 516-656)

### Date Range Selection

Frontend sử dụng date picker component để chọn khoảng thời gian:

```typescript
const [dateRange, setDateRange] = useState<DateRange | null>(null)

// Trong UI
<CalendarDate 
    label="Chọn khoảng thời gian xuất dữ liệu"
    value={dateRange}
    onChange={setDateRange}
/>
```

### API Call

```typescript
// Format dates for API call
const startDate = new Date(
    dateRange.start.year,
    dateRange.start.month - 1,
    dateRange.start.day
)
const endDate = new Date(
    dateRange.end.year,
    dateRange.end.month - 1,
    dateRange.end.day,
    23, 59, 59
)

const startDateStr = format(startDate, "yyyy-MM-dd HH:mm:ss")
const endDateStr = format(endDate, "yyyy-MM-dd HH:mm:ss")

// Encode URL parameters
const encodedStartDate = encodeURIComponent(startDateStr)
const encodedEndDate = encodeURIComponent(endDateStr)

const response = await fetch(
    `${import.meta.env.VITE_API_URL}/data-processing/export-flight-data?start_date=${encodedStartDate}&end_date=${encodedEndDate}`,
    {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }
)
```

### Export to Excel

Frontend sử dụng thư viện `xlsx` để tạo file Excel:

```typescript
// Parse JSON response
const result = await response.json() as ExportFlightDataResponse

// Export to Excel
const XLSX = await import("xlsx")
const excelData = result.data.map((flight: FlightExportData, index: number) => ({
    STT: index + 1,
    "Area": flight.area || "",
    "Convert Date": flight.convert_date || "",
    "Flight No": flight.flightno || "",
    "Route": flight.route || "",
    "Aircraft Type": flight.actype || "",
    "Total Pax": flight.totalpax || 0,
    "Cargo": flight.cgo || 0,
    "Mail": flight.mail || 0,
    "Aircraft Registration": flight.acregno || "",
    "Source": flight.source || "",
    "Sheet Name": flight.sheet_name || "",
    "Seat": flight.seat || "",
    "Int/Dom": flight.int_dom || "",
    "Airline Code": flight.airline_code || "",
    "Airlines Name": flight.airlines_name || "",
    "Airline Nation": flight.airline_nation || "",
    "Airline Nation Code": flight.airline_nation_code || "",
    "Departure": flight.departure || "",
    "City Departure": flight.city_departure || "",
    "Country Departure": flight.country_departure || "",
    "Arrives": flight.arrives || "",
    "City Arrives": flight.city_arrives || "",
    "Country Arrives": flight.country_arrives || "",
    "Country Code": flight.country_code || "",
    "Area Code": flight.area_code || "",
    "Flight Type": flight.flight_type !== "" ? flight.flight_type : "",
}))

const ws = XLSX.utils.json_to_sheet(excelData)
const wb = XLSX.utils.book_new()
XLSX.utils.book_append_sheet(wb, ws, "Flight Report")

// Generate filename based on date range
const fileName = `flight_report_${format(startDate, "yyyy-MM-dd")}_to_${format(endDate, "yyyy-MM-dd")}.xlsx`

XLSX.writeFile(wb, fileName)
```

---

## 🔧 Hướng dẫn Chỉnh sửa Query

Khi cần thay đổi query để xuất dữ liệu khác, cần thực hiện các bước sau:

### 1️⃣ Chỉnh sửa Backend SQL Query

**Location**: `backend/routes/data_processing.py` (lines 794-915)

#### A. Thêm/Xóa Columns trong Final SELECT

Ví dụ: Thêm column `BLOCK_HOUR` từ bảng `Route`:

```python
# Trong CTE DATA_, thêm JOIN với bảng Route
DATA_ AS (
    SELECT
        ...,
        R.[BLOCK HOUR] AS BLOCK_HOUR,  # ← Thêm dòng này
        ...
    FROM FLIGHT_DATA F
    LEFT JOIN AIRLINE_REF A ON LEFT(F.FLIGHTNO, 2) = A.CARRIER
    LEFT JOIN ROUTE R ON R.[ROUTE] = F.ROUTE  # ← Thêm JOIN này
    ...
)

# Trong Final SELECT, thêm column
SELECT  
    ...,
    D.BLOCK_HOUR,  # ← Thêm dòng này
    ...
FROM DATA_ AS D
```

#### B. Thay đổi Filter Conditions

Ví dụ: Chỉ lấy flights của hãng Vietnam Airlines:

```python
FLIGHT_DATA AS (
    SELECT 
        *,
        CASE 
            WHEN TOTALPAX = 0 AND (ISNULL(CGO, 0) + ISNULL(MAIL, 0) > 0) THEN 0 
            WHEN TOTALPAX > 0 THEN 1 
        END AS FLIGHT_TYPE  
    FROM FLIGHT_DATA_CHOT
    WHERE TYPE_FILTER > 0 
      AND NOTE IS NULL
      AND CONVERT_DATE >= :start_date
      AND CONVERT_DATE <= :end_date
      AND LEFT(FLIGHTNO, 2) = 'VN'  # ← Thêm filter này
)
```

#### C. Thay đổi Logic Tính toán

Ví dụ: Thay đổi logic FLIGHT_TYPE để phân loại chi tiết hơn:

```python
FLIGHT_DATA AS (
    SELECT 
        *,
        CASE 
            WHEN TOTALPAX = 0 AND (ISNULL(CGO, 0) + ISNULL(MAIL, 0) > 0) THEN 'CARGO'
            WHEN TOTALPAX > 0 AND TOTALPAX < 50 THEN 'SMALL_PAX'
            WHEN TOTALPAX >= 50 AND TOTALPAX < 150 THEN 'MEDIUM_PAX'
            WHEN TOTALPAX >= 150 THEN 'LARGE_PAX'
            ELSE 'UNKNOWN'
        END AS FLIGHT_TYPE  
    FROM FLIGHT_DATA_CHOT
    ...
)
```

#### D. ⚠️ Chú ý quan trọng về Date Range Filter

**QUAN TRỌNG**: Khi chỉnh sửa query, **BẮT BUỘC** phải giữ nguyên date range filter trong CTE `FLIGHT_DATA`:

```sql
FLIGHT_DATA AS (
    SELECT 
        *,
        CASE 
            WHEN TOTALPAX = 0 AND (ISNULL(CGO, 0) + ISNULL(MAIL, 0) > 0) THEN 0 
            WHEN TOTALPAX > 0 THEN 1 
        END AS FLIGHT_TYPE  
    FROM FLIGHT_DATA_CHOT
    WHERE TYPE_FILTER > 0 
      AND NOTE IS NULL
      AND CONVERT_DATE >= :start_date  -- ← KHÔNG ĐƯỢC XÓA
      AND CONVERT_DATE <= :end_date    -- ← KHÔNG ĐƯỢC XÓA
)
```

**Lý do:**

1. **Date range parameters** (`:start_date`, `:end_date`) được truyền từ frontend qua API
2. Backend convert sang format `YYYYMMDD` (BIGINT) để so sánh với `CONVERT_DATE`
3. Nếu **thiếu** date range filter:
   - Query sẽ scan **TOÀN BỘ** bảng `FLIGHT_DATA_CHOT` → **Performance rất chậm**
   - Export sẽ trả về **TẤT CẢ** dữ liệu trong database → **File Excel quá lớn**
   - Frontend có thể bị **crash** do quá nhiều data

**Lưu ý khi thêm filter khác:**

```sql
-- ✅ ĐÚNG: Giữ date range và thêm filter mới
WHERE TYPE_FILTER > 0 
  AND NOTE IS NULL
  AND CONVERT_DATE >= :start_date
  AND CONVERT_DATE <= :end_date
  AND LEFT(FLIGHTNO, 2) = 'VN'  -- Filter thêm

-- ❌ SAI: Xóa date range filter
WHERE TYPE_FILTER > 0 
  AND NOTE IS NULL
  AND LEFT(FLIGHTNO, 2) = 'VN'  -- Thiếu date range!
```

**Date conversion trong Backend:**

```python
# Frontend gửi: "2024-01-01 00:00:00" đến "2024-01-31 23:59:59"
start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
end = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

# Backend convert thành YYYYMMDD (BIGINT)
start_yyyymmdd = int(start.strftime("%Y%m%d"))  # → 20240101
end_yyyymmdd = int(end.strftime("%Y%m%d"))      # → 20240131

# Truyền vào SQL query
result = db.execute(
    sql_query,
    {
        "start_date": start_yyyymmdd,
        "end_date": end_yyyymmdd,
    },
)
```

### 2️⃣ Cập nhật Backend Response Mapping

**Location**: `backend/routes/data_processing.py` (lines 934-968)

Khi thêm column mới trong SQL query, cần map vào response dictionary:

```python
flight_dict = {
    "area": row.AREA or "",
    "convert_date": (
        row.CONVERT_DATE.strftime("%d/%m/%Y") if row.CONVERT_DATE else ""
    ),
    "flightno": row.FLIGHTNO or "",
    # ... các fields khác ...
    "block_hour": row.BLOCK_HOUR or 0,  # ← Thêm mapping cho column mới
    "flight_type": row.FLIGHT_TYPE if row.FLIGHT_TYPE is not None else "",
}
```

### 3️⃣ Cập nhật Frontend Types

**Location**: `frontend/src/pages/Index.tsx`

#### A. Thêm type definition

Tìm interface `FlightExportData` và thêm field mới:

```typescript
interface FlightExportData {
    area: string
    convert_date: string
    flightno: string
    // ... các fields khác ...
    block_hour: number  // ← Thêm field mới
    flight_type: string | number
}
```

#### B. Cập nhật Excel mapping

```typescript
const excelData = result.data.map((flight: FlightExportData, index: number) => ({
    STT: index + 1,
    "Area": flight.area || "",
    "Convert Date": flight.convert_date || "",
    // ... các fields khác ...
    "Block Hour": flight.block_hour || 0,  // ← Thêm mapping cho Excel
    "Flight Type": flight.flight_type !== "" ? flight.flight_type : "",
}))
```

### 4️⃣ Testing Checklist

Sau khi chỉnh sửa, cần kiểm tra:

- [ ] SQL query chạy được trên database (test bằng SSMS)
- [ ] Backend trả về đúng format JSON
- [ ] Frontend nhận được data và map đúng
- [ ] Excel export có đủ columns và data chính xác
- [ ] Error handling hoạt động đúng (empty data, invalid dates, etc.)

---

## 📊 Bảng Reference Tables được sử dụng

| Table Name | Mục đích | Join Key | Columns quan trọng |
|------------|----------|----------|-------------------|
| `FLIGHT_DATA_CHOT` | Flight data chính | - | CONVERT_DATE, FLIGHTNO, ROUTE, ACTYPE, TOTALPAX, CGO, MAIL |
| `SECTOR_ROUTE_DOM_REF` | Routes nội địa với area | SECTOR | SECTOR, AREA_LV1, DOM/INT |
| `AIRLINE_REF` | Thông tin hãng bay | CARRIER (2 ký tự đầu của FLIGHTNO) | CARRIER, AIRLINES_NAME, AIRLINE_NATION |
| `AIRPORT_REF` | Thông tin sân bay | IATACODE | IATACODE, CITY, COUNTRY |
| `COUNTRY_REF` | Thông tin quốc gia | COUNTRY | COUNTRY, 2_LETTER_CODE, REGION_(VNM) |

---

## ⚠️ Lưu ý quan trọng

### Date Format

- **Database**: `CONVERT_DATE` lưu dưới dạng BIGINT format YYYYMMDD (ví dụ: 20240115)
- **API Input**: String format `YYYY-MM-DD HH:mm:ss`
- **API Output**: String format `DD/MM/YYYY`
- **Excel Output**: String format `DD/MM/YYYY`

### Route Normalization

- Routes luôn được chuẩn hóa về dạng `SMALLER_CODE-LARGER_CODE`
- Ví dụ: `SGN-HAN` và `HAN-SGN` đều được chuẩn hóa về `HAN-SGN`

### NULL Handling

- Tất cả fields đều có default value (`""` hoặc `0`) để tránh NULL trong Excel
- Backend sử dụng `or ""` và `or 0` khi map response

### Performance

- Query sử dụng nhiều LEFT JOIN, có thể chậm với dataset lớn
- Có index trên `CONVERT_DATE` để tăng tốc filter theo date range
- Nên limit khoảng thời gian export (không quá 1 tháng)

---

## 🎯 Common Use Cases

### 1. Export theo hãng bay cụ thể

**Backend** - Thêm parameter:

```python
@router.get("/export-flight-data")
async def export_flight_data(
    start_date: str,
    end_date: str,
    airline_code: Optional[str] = None,  # ← Thêm parameter
    db: Session = Depends(get_db),
):
```

**SQL Query** - Thêm filter:

```sql
FLIGHT_DATA AS (
    SELECT ...
    FROM FLIGHT_DATA_CHOT
    WHERE TYPE_FILTER > 0 
      AND NOTE IS NULL
      AND CONVERT_DATE >= :start_date
      AND CONVERT_DATE <= :end_date
      AND (:airline_code IS NULL OR LEFT(FLIGHTNO, 2) = :airline_code)
)
```

### 2. Export theo route cụ thể

**SQL Query** - Thêm filter:

```sql
WHERE ...
  AND (:route IS NULL OR ROUTE = :route)
```

### 3. Export chỉ domestic hoặc international flights

**SQL Query** - Thêm filter trong DATA_CTE sau khi tính INT_DOM:

```sql
-- Trong final SELECT, thêm WHERE clause
SELECT ...
FROM DATA_ AS D
LEFT JOIN ROUTE_ AS S ON D.ROUTE_SORT = S.ROUTE
WHERE (:flight_type IS NULL OR D.INT_DOM = :flight_type)
ORDER BY D.CONVERT_DATE, D.FLIGHTNO
```

---

## 🐛 Troubleshooting

### Lỗi: "Ngày giờ không hợp lệ"

- **Nguyên nhân**: Format date không đúng `YYYY-MM-DD HH:mm:ss`
- **Giải pháp**: Kiểm tra format date từ frontend

### Lỗi: "Không có dữ liệu"

- **Nguyên nhân**:
  - Không có flight trong khoảng thời gian
  - `TYPE_FILTER > 0` và `NOTE IS NULL` filter quá strict
- **Giải pháp**: Kiểm tra dữ liệu trong bảng `FLIGHT_DATA_CHOT`

### Excel export chậm

- **Nguyên nhân**: Dataset quá lớn
- **Giải pháp**:
  - Giới hạn date range
  - Tối ưu SQL query với index
  - Implement pagination

### Missing columns trong Excel

- **Nguyên nhân**: Quên map field trong frontend
- **Giải pháp**: Kiểm tra mapping trong `excelData.map()`

---

## 📚 Tài liệu tham khảo

- **SQL Schema**: `backend/flight.sql`
- **Backend Route**: `backend/routes/data_processing.py`
- **Frontend Component**: `frontend/src/pages/Index.tsx`
- **Database**: SQL Server `flight` database

---

## 📞 Support

Nếu cần hỗ trợ hoặc có câu hỏi, vui lòng liên hệ team development.
