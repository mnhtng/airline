# Schema package
##! 1. Xác thực dữ liệu (Validation)
### - Khi client gửi request (POST, PUT, PATCH…), FastAPI sẽ so sánh dữ liệu với schema để kiểm tra xem có hợp lệ không

##! 2. Sinh tài liệu API tự động (OpenAPI / Swagger)
### - FastAPI sẽ tự động sinh ra tài liệu API dựa trên các schema đã định nghĩa
### - Field(description="...") sẽ hiển thị thành mô tả trong Swagger UI

##!  3. Quản lý input/output rõ ràng
### - Có thể định nghĩa riêng schema cho input và schema cho output
####* + Input: Được sử dụng để xác thực dữ liệu khi nhận request từ client (AircraftCreate)
####* + Output: Được sử dụng để định dạng dữ liệu trước khi gửi response về cho client (AircraftResponse)

##! 4. Tự động chuyển đổi dữ liệu (Serialization/Deserialization)
### - FastAPI sẽ tự động chuyển đổi dữ liệu giữa các định dạng khác nhau (ví dụ: từ dict/JSON sang Python object và ngược lại)
### - Điều này giúp:
####* + Dữ liệu request body tự động parse thành object Python
####* + Response trả ra JSON chuẩn
