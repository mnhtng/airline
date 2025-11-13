# 🚀 Hướng Dẫn Deploy Website Lên Ubuntu VPS

## 📋 Tổng Quan

Hướng dẫn này sẽ giúp bạn deploy website với:

- **Frontend**: React + Vite (port 5173 → 80/443)
- **Backend**: Python FastAPI (port 8000)
- **Web Server**: Nginx (reverse proxy)
- **Process Manager**: PM2 (frontend), Systemd (backend)
- **Database**: SQL Server (đã có)

---

## 🔧 Bước 1: Chuẩn Bị VPS

### 1.1. SSH vào VPS

```bash
ssh root@YOUR_VPS_IP
# Hoặc nếu dùng username khác:
ssh username@YOUR_VPS_IP
```

### 1.2. Update hệ thống

```bash
sudo apt update && sudo apt upgrade -y
```

### 1.3. Cài đặt các công cụ cần thiết

```bash
# Git
sudo apt install git -y

# Curl
sudo apt install curl -y

# Build essentials
sudo apt install build-essential -y
```

---

## 🐍 Bước 2: Cài Đặt Python & Backend Dependencies

### 2.1. Cài Python 3.11+

```bash
# Kiểm tra version Python hiện tại
python3 --version

# Nếu chưa có Python 3.11+, cài đặt:
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# Cài pip
sudo apt install python3-pip -y
```

### 2.2. Cài ODBC Driver cho SQL Server

```bash
# Download Microsoft GPG key
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -

# Add Microsoft repository
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# Install ODBC Driver
sudo apt update
sudo ACCEPT_EULA=Y apt install -y msodbcsql17 unixodbc-dev

# Verify installation
odbcinst -j
```

Hoặc dùng Docker

```bash
# Remove the broken SQL Server installation
sudo apt-get remove -y mssql-server
sudo rm -rf /opt/mssql

# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Run SQL Server in Docker
sudo docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=tunghpvn123" \
  -p 1433:1433 --name sqlserver --restart always \
  -d mcr.microsoft.com/mssql/server:2022-latest

# Wait a few seconds for SQL Server to start
sleep 10

# Create the flight database
sudo docker exec sqlserver /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U sa -P "tunghpvn123" \
  -Q "CREATE DATABASE flight;"

# Verify it's running
sudo docker ps

# Drop database
sudo docker exec sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "tunghpvn123" -C -Q "DROP DATABASE IF EXISTS flight;"

# Create database using sqlcmd
docker exec sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "tunghpvn123" -C -Q "CREATE DATABASE flight;"

# Run SQL scripts - Option 1: Pipe từ host (khuyến nghị)
echo "Running flight-raw.sql..."
cat /var/www/airline/backend/flight-raw.sql | docker exec -i sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "tunghpvn123" -C -d flight

echo "Running flight-update.sql..."
cat /var/www/airline/backend/flight-update.sql | docker exec -i sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "tunghpvn123" -C -d flight

# Run SQL scripts - Option 2: Copy files vào container
docker cp /var/www/airline/backend/flight-raw.sql sqlserver:/tmp/flight-raw.sql
docker cp /var/www/airline/backend/flight-update.sql sqlserver:/tmp/flight-update.sql
docker exec sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "tunghpvn123" -C -d flight -i /tmp/flight-raw.sql
docker exec sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "tunghpvn123" -C -d flight -i /tmp/flight-update.sql

# Run SQL scripts - Option 3: Dùng script tự động (tốt nhất)
chmod +x /var/www/airline/scripts/init-database.sh
/var/www/airline/scripts/init-database.sh

# Verify tables
docker exec sqlserver /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P "tunghpvn123" -C \
  -d flight \
  -Q "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_NAME;"


```

---

## 📦 Bước 3: Clone & Setup Project

### 3.1. Tạo thư mục và clone project

```bash
# Tạo thư mục cho application
sudo mkdir -p /var/www
cd /var/www

# Clone repository (thay YOUR_REPO_URL)
sudo git clone YOUR_REPO_URL airline
cd airline

# Phân quyền
sudo chown -R $USER:$USER /var/www/airline
```

### 3.2. Setup Backend

```bash
cd /var/www/airline/backend

# Tạo virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 3.3. Configure Backend Environment

```bash
# Copy và edit file .env
cp .env.example .env
nano .env
```

**Cập nhật nội dung file `.env`:**

```env
# Database Connection (BẮT BUỘC)
DATABASE_URL=mssql+pyodbc://sa:your_password@localhost:1433/flight?driver=ODBC+Driver+17+for+SQL+Server

# API Settings
API_PREFIX=/api/v1
DEBUG=False

# CORS - Cho phép frontend truy cập (BẮT BUỘC)
ALLOWED_ORIGINS=http://YOUR_VPS_IP,http://localhost:5173

# OpenAI API Key (OPTIONAL - có thể bỏ qua nếu không dùng)
# OPENAI_API_KEY=sk-your-openai-key-here
```

**Thay đổi:**

- `your_password` → Mật khẩu SQL Server của bạn
- `YOUR_VPS_IP` → IP public của VPS (ví dụ: `123.45.67.89`)

**Lưu file**: `Ctrl + O`, `Enter`, `Ctrl + X`

### 3.4. Test Backend

```bash
# Quay về thư mục gốc airline (QUAN TRỌNG!)
cd /var/www/airline

# Activate virtual environment
source backend/.venv/bin/activate

# Test chạy backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Hoặc dùng fastapi dev
fastapi dev backend/main.py

# Nếu chạy thành công, bạn sẽ thấy:
# INFO:     Uvicorn running on http://0.0.0.0:8000

# Test từ browser hoặc curl:
curl http://YOUR_VPS_IP:8000/api/v1/

# Dừng server: Ctrl + C
```

---

## 🔄 Bước 4: Setup Systemd Service cho Backend

### 4.1. Tạo service file

```bash
sudo nano /etc/systemd/system/airline-backend.service
```

**Nội dung file:**

```ini
[Unit]
Description=Airline FastAPI Backend
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/var/www/airline
Environment="PATH=/var/www/airline/backend/.venv/bin"
ExecStart=/var/www/airline/backend/.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Thay `YOUR_USERNAME`** bằng username Linux của bạn (chạy `whoami` để xem).

### 4.2. Enable và start service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (tự động chạy khi reboot)
sudo systemctl enable airline-backend

# Start service
sudo systemctl start airline-backend

# Check status
sudo systemctl status airline-backend

# Xem logs
sudo journalctl -u airline-backend -f
```

**Các lệnh hữu ích:**

```bash
# Restart service
sudo systemctl restart airline-backend

# Stop service
sudo systemctl stop airline-backend

# Xem logs
sudo journalctl -u airline-backend --no-pager -n 100
```

**Khi đã enable service:**

```bash
sudo systemctl daemon-reload
sudo systemctl restart airline-backend
sudo systemctl status airline-backend
```

---

## 🌐 Bước 5: Cài Đặt Node.js & Setup Frontend

### 5.1. Cài Node.js (v18+)

```bash
# Cài NVM (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Load NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Cài Node.js LTS
nvm install --lts
nvm use --lts

# Verify
node --version
npm --version
```

### 5.2. Cài PM2 (Process Manager)

```bash
npm install -g pm2

# Enable PM2 startup
pm2 startup
# Copy và chạy lệnh mà PM2 output ra
```

### 5.3. Setup Frontend

```bash
cd /var/www/airline/frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
nano .env
```

**Cập nhật file `.env`:**

```env
# Sử dụng IP VPS hoặc domain
VITE_API_URL=http://YOUR_VPS_IP:8000/api/v1
# Hoặc nếu có domain:
# VITE_API_URL=https://yourdomain.com/api/v1

VITE_DEBUG=false
```

### 5.4. Build Frontend

```bash
# Build production
npm run build

# Kiểm tra thư mục dist đã được tạo
ls -la dist/
```

---

## 🌍 Bước 6: Cài Đặt & Cấu Hình Nginx

### 6.1. Cài Nginx

```bash
sudo apt install nginx -y

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx
```

### 6.2. Cấu hình Nginx cho website

```bash
# Tạo config file
sudo nano /etc/nginx/sites-available/airline
```

**Nội dung file (chỉ dùng IP):**

```nginx
server {
    listen 80;
    server_name YOUR_VPS_IP;

    # Frontend - React Build
    location / {
        root /var/www/airline/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/v1 {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Docs
    location /docs {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /redoc {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # OpenAPI JSON
    location /openapi.json {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Nếu có domain, thay `YOUR_VPS_IP` bằng `yourdomain.com`**

**Flow:**

```sh
┌─────────────────┐
│   User Browser  │
│   (Internet)    │
└────────┬────────┘
         │ ① Request: http://123.45.123.123/api/v1/users
         ↓
┌─────────────────────────────────┐
│      Nginx (Port 80)            │
│  Listening on: 0.0.0.0:80       │
│  (Public IP: 123.45.123.123)    │
└────────┬────────────────────────┘
         │ ② Proxy Pass: http://127.0.0.1:8000/api/v1/users
         ↓
┌─────────────────────────────────┐
│   FastAPI Backend (Port 8000)   │
│   Listening on: 127.0.0.1:8000  │
│   (Localhost only)              │
└─────────────────────────────────┘
```

### 6.3. Enable config và restart Nginx

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/airline /etc/nginx/sites-enabled/

# Remove default config
sudo rm /etc/nginx/sites-enabled/default

# Test config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

---

## 🔥 Bước 7: Cấu Hình Firewall

```bash
# Allow SSH (quan trọng!)
sudo ufw allow 22/tcp

# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS (nếu dùng SSL)
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

---

## 🔒 Bước 8: Cài SSL Certificate (Nếu Có Domain)

### 8.1. Cài Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 8.2. Lấy SSL certificate

```bash
# Thay yourdomain.com bằng domain thật
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Follow prompts và nhập email
```

### 8.3. Auto-renew SSL

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot sẽ tự động renew qua cron job
```

### 8.4. Update Frontend .env với HTTPS

```bash
cd /var/www/airline/frontend
nano .env
```

```env
VITE_API_URL=https://yourdomain.com/api/v1
VITE_DEBUG=false
```

```bash
# Rebuild frontend
npm run build

# Restart Nginx
sudo systemctl restart nginx
```

---

## 🔄 Bước 9: Update Code & Xử Lý Conflict

### 9.1. Pull code cơ bản

```bash
cd /var/www/airline

# Kiểm tra trạng thái
git status

# Pull code mới
git pull origin main
```

### 9.2. Pull khi có thay đổi local

```bash
# Cách 1: Stash (khuyến nghị)
git stash
git pull origin main
git stash pop

# Cách 2: Commit trước
git add .
git commit -m "Local changes"
git pull origin main
```

### 9.3. Xử lý conflict

**Khi có conflict:**

```bash
# Xem files bị conflict
git status

# Xem chi tiết conflict
git diff <file>

# Chọn version remote (khuyến nghị cho deployment)
git checkout --theirs <file>
git add <file>

# Hoặc chọn version local
git checkout --ours <file>
git add <file>

# Hoặc sửa thủ công và mark resolved
nano <file>  # Xóa các dòng <<<<<<, =======, >>>>>>>
git add <file>

# Hoàn tất merge
git commit -m "Resolved merge conflicts"
```

**Hủy merge nếu cần:**

```bash
git merge --abort
```

### 9.4. Script tự động update

Tạo file `deploy.sh`:

```bash
cd /var/www/airline
nano deploy.sh
```

**Nội dung:**

```bash
#!/bin/bash

echo "🚀 Starting deployment..."

# Pull latest code
echo "📥 Pulling latest code..."
git pull origin main

# Backend
echo "🐍 Updating backend..."
cd backend
source .venv/bin/activate
pip install -r requirements.txt --upgrade
deactivate
cd ..

# Restart backend service
echo "♻️ Restarting backend service..."
sudo systemctl restart airline-backend

# Frontend
echo "🌐 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Restart Nginx
echo "♻️ Restarting Nginx..."
sudo systemctl restart nginx

echo "✅ Deployment completed!"
```

**Phân quyền:**

```bash
chmod +x deploy.sh
```

**Chạy khi cần update:**

```bash
cd /var/www/airline
./deploy.sh
```

---

## 📊 Bước 10: Monitoring & Logs

### 10.1. Check Backend Logs

```bash
# Real-time logs
sudo journalctl -u airline-backend -f

# Last 100 lines
sudo journalctl -u airline-backend -n 100 --no-pager

# Logs since today
sudo journalctl -u airline-backend --since today
```

### 10.2. Check Nginx Logs

```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log
```

### 10.3. Check System Resources

```bash
# CPU & Memory
top
# hoặc
htop  # (cài: sudo apt install htop)

# Disk usage
df -h

# Check port usage
sudo netstat -tulpn | grep LISTEN
```

---

## 🛠️ Troubleshooting

### Backend không start

```bash
# Check logs
sudo journalctl -u airline-backend -n 50

# Check port 8000
sudo netstat -tulpn | grep 8000

# Restart service
sudo systemctl restart airline-backend
```

### Frontend không hiển thị

```bash
# Check Nginx config
sudo nginx -t

# Check file permissions
ls -la /var/www/airline/frontend/dist/

# Rebuild frontend
cd /var/www/airline/frontend
npm run build

# Restart Nginx
sudo systemctl restart nginx
```

### CORS errors

- Kiểm tra `ALLOWED_ORIGINS` trong `backend/.env`
- Đảm bảo có domain/IP của frontend
- Restart backend sau khi thay đổi

### Database connection errors

```bash
# Test ODBC connection
odbcinst -j

# Check DATABASE_URL trong .env
cd /var/www/airline/backend
cat .env | grep DATABASE_URL
```

---

## 📝 Checklist Hoàn Thành

- [ ] VPS đã update và cài đủ dependencies
- [ ] Python 3.11+ và ODBC Driver đã cài
- [ ] Backend service chạy thành công (`systemctl status airline-backend`)
- [ ] Node.js và npm đã cài
- [ ] Frontend đã build (`npm run build` thành công)
- [ ] Nginx đã cài và config đúng (`nginx -t` pass)
- [ ] Firewall đã config (UFW allow 80, 443, 22)
- [ ] Website truy cập được qua `http://YOUR_VPS_IP`
- [ ] Backend API test OK: `http://YOUR_VPS_IP/api/v1/`
- [ ] API Docs: `http://YOUR_VPS_IP/docs`
- [ ] (Optional) SSL certificate đã setup nếu có domain

---

## 🎯 URLs Sau Khi Deploy

- **Frontend**: `http://YOUR_VPS_IP` hoặc `https://yourdomain.com`
- **Backend API**: `http://YOUR_VPS_IP/api/v1` hoặc `https://yourdomain.com/api/v1`
- **API Docs**: `http://YOUR_VPS_IP/docs` hoặc `https://yourdomain.com/docs`
- **API ReDoc**: `http://YOUR_VPS_IP/redoc` hoặc `https://yourdomain.com/redoc`

---

## 💡 Tips

1. **Backup định kỳ**: Setup cronjob backup database
2. **Monitor resources**: Cài monitoring tools (htop, netdata)
3. **Security**: Đổi SSH port, disable root login, use SSH keys
4. **Auto-update**: Setup GitHub Actions/webhooks cho auto-deploy
5. **CDN**: Sử dụng Cloudflare cho caching và security

---

**Chúc bạn deploy thành công! 🎉**
