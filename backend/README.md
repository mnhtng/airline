# 📚 Thư viện Python

0. typing: Cung cấp gợi ý kiểu dữ liệu (type hints) cho biến, hàm, class: List[T], Dict[K, V], Set[T], Optional[T] ...
1. pydantic: Data validation, serialization, type hint mạnh (schema cho request/response)
2. uvicorn: ASGI server chạy FastAPI (nhanh, lightweight)
3. sqlalchemy: ORM mạnh, quản lý bảng, quan hệ, transaction
4. python-jose: JWT encode/decode
5. passlib: Hash password an toàn (bcrypt, argon2, pbkdf2)
6. authlib: OAuth2, OpenID Connect (login bằng Google, Facebook, GitHub...)
7. python-multipart: Upload file multipart/form-data
8. webSockets: Dùng WebSocket server/client
9. Socket.IO: Giao tiếp realtime (chat app, dashboard)
10. Redis Pub/Sub: Gửi/nhận message realtime qua Redis
11. numpy: Tính toán số học và ma trận, được tối ưu hiệu năng

# 💻 Create Virtual Python Environment

`Cho phép bạn tạo ra một không gian riêng biệt cho từng dự án Python, giúp quản lý các dependencies và lib version một cách hiệu quả`

1. Ctrl + Shift + P
2. Search: "Python: Create Environment"
3. Select venv
4. Choose version Python you used
5. Trong Terrminal, sử dụng `pip` để tải các lib cần thiết (giống `npm` trong Nodejs)
    - `pip install ...`
6. Run code: `python main.py` / Nhấn Run/Debug

### Hoặc

1. Mở Terminal trong folder cần tạo virtual env (name-project/backend)
2. Create a virtual environment:
    - Mac/Linux: `python3 -m venv venv`
    - Windows: `python -m venv venv`
3. Activate the virtual environment:
    - Mac/Linux: `source .venv/bin/activate`
    - Windows: `.venv\\Scripts\\activate.bat`
    - PowerShell: `.venv\Scripts\Activate.ps1`
    - Terminal: `.venv\Scripts\activate.bat`
4. Install the dependencies: `pip install -r requirements.txt`

Có thể thay thế thao tác thủ công trên với `uv install`

1. Mở Terminal trong folder cần tạo virtual env (name-project/backend)
2. Run: `uv init .`
3. Run: `uv venv` / `uv venv .venv`
4 Run: `uv add ... ...` / `uv pip install -r requirements.txt` / `pip install -r requirements.txt`
    - VD: `uv add fastapi[standard] uvicorn pydantic sqlalchemy pyodbc langchain langchain-openai python-dotenv`
5 Activate the virtual environment:
    - Mac/Linux: `source .venv/bin/activate`
    - Windows: `source .venv/Scripts/activate`
    - PowerShell: `.venv\Scripts\Activate.ps1`
    - Terminal: `.venv\Scripts\activate.bat`
6. Run:
    - `uv run main.py`: Sửa path thành `localhost:port` thành vì 0.0.0.0
    - `fastapi dev main.py`: Sử dụng Server path của FastAPI cung cấp
    - `fastapi run main.py`: Sử dụng trong production

# 🖊️ Note

### 0. Quy tắc đặt tên biến

Tên biến trong Python phải tuân theo các quy tắc sau:

- Tên biến phải bắt đầu bằng một chữ cái hoặc dấu gạch dưới (_).
- Tên biến không được bắt đầu bằng chữ số.
- Tên biến chỉ có thể chứa các ký tự chữ cái, chữ số và dấu gạch dưới (A-z, 0-9, và_).
- Tên biến phân biệt chữ hoa chữ thường.

### 1. Trong Python, các câu lệnh thường được viết trên một dòng. Tuy nhiên, nếu câu lệnh quá dài, bạn có thể chia nó thành nhiều dòng bằng cách sử dụng dấu gạch chéo ngược (\), dấu ngoặc đơn (()), dấu ngoặc vuông ([]), hoặc dấu ngoặc nhọn ({})

```py
# Sử dụng dấu gạch chéo ngược
total = 1 + 2 + 3 + \
        4 + 5 + 6 + \
        7 + 8 + 9

# Sử dụng dấu ngoặc đơn
total = (1 + 2 + 3 +
         4 + 5 + 6 +
         7 + 8 + 9)
```

### 2. Python hỗ trợ cả dấu ngoặc đơn (') và dấu ngoặc kép (") để xác định chuỗi ký tự. Để tạo chuỗi nhiều dòng, bạn có thể sử dụng ba dấu ngoặc đơn (''') hoặc ba dấu ngoặc kép (""")

```py
# Chuỗi một dòng
single_line = 'Hello, World!'
double_line = "Hello, World!"

# Chuỗi nhiều dòng
multi_line = '''This is a
multi-line string.'''
```

### 3. Bạn có thể viết nhiều câu lệnh trên một dòng bằng cách sử dụng dấu chấm phẩy (;)

```py
a = 1; b = 2; c = a + b
print(c)
```

### 4. Tên biến trong Python phân biệt chữ hoa chữ thường. Điều này có nghĩa là a và A là hai biến khác nhau

```py
a = 4
A = "Sally"
print(a)
print(A)
```

### 5. Python cho phép bạn gán giá trị cho nhiều biến trong một dòng

```py
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)
```

### 6. Danh sách Literals

- Int, Float
- String
- Boolean
- List, Tuple
- Dict, Set

### 7. So sánh toán tử `==` và `is`

- Toán tử `==`: so sánh giá trị của 2 biến
- Toán tử `is`: so sánh vị trí bộ nhớ của 2 biến (nếu là các literal - bất biến -> cùng vị trí bộ nhớ nếu cùng giá trị)

### 8. f-string

Cho phép nhúng biến hoặc biểu thức Python trực tiếp vào trong chuỗi bằng cặp `{ }`

```py
# 1. Cơ bản nhất
name = "Tung"
age = 25
print(f"Tôi là {name}, {age} tuổi.") # Tôi là Tung, 25 tuổi.

# 2. Viết code bên trong
a, b = 5, 3
print(f"{a} + {b} = {a+b}") # 5 + 3 = 8

# 3. Định dạng
pi = 3.14159265
print(f"Pi ~ {pi:.2f}") # Pi ~ 3.14

ratio = 0.256
print(f"Tỉ lệ: {ratio:.1%}") # Tỉ lệ: 25.6%

money = 123456789
print(f"Số tiền: {money:,}") # Số tiền: 123,456,789

from datetime import datetime
now = datetime.now()
print(f"Hôm nay: {now:%d-%m-%Y %H:%M}") # Hôm nay: 27-08-2025 12:30

# 4. Căn lề/độ rộng
text = "Hi"
print(f"|{text:<10}|")  # Căn trái
print(f"|{text:>10}|")  # Căn phải
print(f"|{text:^10}|")  # Căn giữa
"""
|Hi        |
|        Hi|
|    Hi    |

"""

# 5. Sử dụng với dict/obj
person = {"name": "Linh", "age": 20}
print(f"{person['name']} - {person['age']} tuổi") # Linh - 20 tuổi

class Car:
    def __init__(self, brand, seats):
        self.brand = brand
        self.seats = seats

car = Car("Airbus A320", 180)
print(f"{car.brand} có {car.seats} ghế") # Airbus A320 có 180 ghế

# 6. Multi-line string 
name = "Boeing 747"
seats = 366
print(f"""
Máy bay: {name}
Số ghế: {seats}
""")

# 7. Debug
user = "admin"
count = 5
print(f"{user=}, {count=}") # user='admin', count=5

```
