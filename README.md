# Airline Data Processing System

Hệ thống xử lý dữ liệu hàng không với khả năng import, làm sạch và làm giàu dữ liệu từ file Excel theo logic nghiệp vụ phức tạp.

## 🚀 Tính năng chính

### 📊 Xử lý dữ liệu Excel

- **Phân loại tự động**: Hệ thống tự động phân loại file Excel theo miền:
    - **MN** (Miền Nam): File chứa "toan cang"
    - **MB** (Miền Bắc): File bắt đầu với "NAA"
    - **MT** (Miền Trung): File bắt đầu với "CV1"

- **Làm sạch dữ liệu**:
    - Chuyển đổi kiểu dữ liệu tự động
    - Xử lý giá trị thiếu (NaN/None)
    - Chuẩn hóa định dạng số

- **Làm giàu dữ liệu**:
    - Tự động gán sheet_name dựa trên route (đối với MB)
    - Điền thông tin thiếu từ dòng trên (ffill)
    - Xử lý đặc biệt cho từng miền

### 🔍 Theo dõi chất lượng dữ liệu

- Phát hiện missing dimensions (actype, route)
- Thống kê xử lý dữ liệu real-time
- Log chi tiết quá trình import

### 🛠️ Stored Procedures

- `usp_ProcessFlightData`: Xử lý và phát hiện dữ liệu thiếu
- `usp_ImportAndUpdateMissingDimensions`: Import thông tin bổ sung

## 📋 Yêu cầu hệ thống

### Database

- SQL Server 2019+
- Database name: `airline`

### Backend (Python/FastAPI)

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pandas
- PyODBC

### Frontend (React/TypeScript)

- Node.js 18+
- React 18+
- TypeScript
- Tailwind CSS

## 🛠️ Cài đặt và chạy

### 1. Chuẩn bị Database

```sql
-- Tạo database
CREATE DATABASE airline;
GO

-- Chạy script tạo bảng và stored procedures
-- File: backend/airline.sql
```

### 2. Backend Setup

```bash
cd Project/airline/backend

# Tạo virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Tạo file .env
cp .env.example .env

# Cấu hình DATABASE_URL trong .env
DATABASE_URL=mssql+pyodbc://@localhost/airline?driver=ODBC+Driver+17+for+SQL+Server

# Chạy server
python main.py
```

Backend sẽ chạy tại: <http://localhost:8000>

### 3. Frontend Setup

```bash
cd Project/airline/frontend

# Install dependencies
npm install

# Chạy development server
npm run dev
```

Frontend sẽ chạy tại: <http://localhost:5173>

### 4. Test hệ thống

```bash
cd Project/airline/backend

# Chạy test pipeline (Backend phải đang chạy)
python test_data_pipeline.py
```

## 📖 Hướng dẫn sử dụng

### 1. Import dữ liệu Excel

1. Truy cập trang chủ: <http://localhost:5173>
2. Kéo thả file Excel vào vùng upload
3. Click "Xử lý dữ liệu" để chạy pipeline
4. Hệ thống sẽ:
   - Phân loại file theo miền
   - Làm sạch dữ liệu
   - Lưu vào database
   - Chạy stored procedure làm giàu dữ liệu

### 2. Theo dõi trạng thái

1. Truy cập "Trạng thái dữ liệu": <http://localhost:5173/data-status>
2. Xem thống kê:
   - Tổng số chuyến bay
   - Dữ liệu thiếu (actype, route)
   - Lịch sử import

### 3. Bổ sung dữ liệu thiếu

Khi có missing dimensions, tạo file Excel với format:

**Actype (Loại máy bay):**

```
actype | seat
A320   | 180
A321   | 220
```

**Route (Tuyến bay):**

```
route   | country | flight_hour | distance_km
HAN-SGN | VN-VN   | 2.5         | 1200
```

## 🔧 API Endpoints

### Data Processing

- `POST /api/v1/data-processing/process-excel` - Xử lý dữ liệu Excel
- `GET /api/v1/data-processing/stats` - Thống kê xử lý
- `GET /api/v1/data-processing/missing-dimensions` - Dữ liệu thiếu
- `GET /api/v1/data-processing/flight-data` - Dữ liệu chuyến bay
- `POST /api/v1/data-processing/run-stored-procedure` - Chạy SP

### Management

- `GET /api/v1/aircrafts` - Quản lý máy bay
- `GET /api/v1/airways` - Quản lý đường bay

API Docs: <http://localhost:8000/docs>

## 📊 Database Schema

### Core Tables

- `flight_raw` - Dữ liệu thô từ Excel
- `aircrafts` / `aircraft_drafts` - Thông tin máy bay
- `airways` / `airway_drafts` - Thông tin đường bay

### Processing Tables

- `actype_seat` - Thông tin số ghế theo loại máy bay
- `route_details` - Chi tiết tuyến bay
- `missing_dimensions_log` - Log dữ liệu thiếu
- `import_log` - Lịch sử import

### Temp Tables

- `temp_actype_import` - Import tạm actype
- `temp_route_import` - Import tạm route

## 🧪 Logic xử lý theo miền

### Miền Nam (MN)

- File chứa "toan cang"
- Sheet name mặc định: "MN"
- Xử lý toàn bộ sheet

### Miền Bắc (MB)

- File bắt đầu "NAA"
- Tự động phân tích route để xác định sheet_name
- Mapping: THD, HPH, HAN, VDO, VDH, VII, DIN

### Miền Trung (MT)

- File bắt đầu "CV1"
- Sheet name mặc định: "MT"
- Xử lý đặc biệt cho numeric columns

## 🐛 Troubleshooting

### Lỗi kết nối Database

- Kiểm tra SQL Server đang chạy
- Verify connection string trong .env
- Đảm bảo có ODBC Driver 17 for SQL Server

### Lỗi import Excel

- Kiểm tra format file (.xlsx, .xls)
- Đảm bảo có đúng columns cần thiết
- Xem log errors trong response

### Frontend không load được

- Kiểm tra backend đang chạy port 8000
- Verify CORS settings
- Check browser console cho errors

## 📝 Development Notes

### Thêm rule xử lý mới

1. Update `DataProcessor.process_excel_data()`
2. Modify `json_data` mapping
3. Add business logic cho region mới

### Thêm stored procedure

1. Add SP vào `airline.sql`
2. Create endpoint trong `data_processing.py`
3. Update frontend nếu cần

### Database migrations

- Backup database trước khi chạy script mới
- Test trên development environment trước
- Document các thay đổi schema

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

Private project - All rights reserved
