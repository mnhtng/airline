# ============================================
# Stage 1: Build Stage
# ============================================
FROM python:3.11-slim AS builder

# 1. ARG - Biến dùng trong quá trình build
ARG APP_ENV=production

# 2. ENV - Tối ưu Python cho container
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 3. WORKDIR - Đặt thư mục làm việc
WORKDIR /app

# 4. RUN - Cài đặt build dependencies cho pyodbc (SQL Server driver)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    unixodbc-dev \
    gcc \
    g++ \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

# 5. COPY - Copy requirements trước để tận dụng Docker cache
COPY requirements.txt .

# 6. RUN - Cài đặt Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ============================================
# Stage 2: Production Stage
# ============================================
FROM python:3.11-slim AS production

# 7. LABEL - Thêm metadata cho image
LABEL maintainer="support@airlineapi.com" \
      version="1.0.0" \
      description="Airline API - FastAPI Backend with SQL Server"

# 8. ENV - Biến môi trường runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production

# 9. WORKDIR
WORKDIR /app

# 10. RUN - Cài đặt ODBC Driver cho SQL Server (runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    unixodbc \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 11. COPY - Copy Python packages từ builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 12. USER - Tạo user không phải root (bảo mật)
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup appuser \
    && mkdir -p /app/logs /app/uploads \
    && chown -R appuser:appgroup /app

# 13. COPY - Copy source code
COPY --chown=appuser:appgroup . .

# 14. USER - Chuyển sang user không phải root
USER appuser

# 15. EXPOSE - Khai báo port
EXPOSE 8000

# 16. VOLUME - Mount points cho logs và uploads
VOLUME ["/app/logs", "/app/uploads"]

# 17. HEALTHCHECK - Kiểm tra sức khỏe container
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/ || exit 1

# 18. ENTRYPOINT + CMD - Lệnh khởi chạy
ENTRYPOINT ["uvicorn"]
CMD ["backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
