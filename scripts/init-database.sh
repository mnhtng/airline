#!/bin/bash

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SQL_FILE_RAW="$PROJECT_ROOT/backend/flight-raw.sql"
SQL_FILE_UPDATE="$PROJECT_ROOT/backend/flight-update.sql"

echo "🚀 Initializing MSSQL Database..."

# Check if SQL files exist
if [ ! -f "$SQL_FILE_RAW" ]; then
    echo "❌ Error: SQL file not found at $SQL_FILE_RAW"
    exit 1
fi

if [ ! -f "$SQL_FILE_UPDATE" ]; then
    echo "❌ Error: SQL file not found at $SQL_FILE_UPDATE"
    exit 1
fi

# Check if container is running
if ! docker ps | grep -q sqlserver; then
    echo "❌ Error: SQL Server container is not running"
    echo "Start it with: docker start sqlserver"
    exit 1
fi

# Wait for SQL Server to be ready
echo "⏳ Waiting for SQL Server to be ready..."
for i in {1..30}; do
    if docker exec sqlserver /opt/mssql-tools18/bin/sqlcmd \
        -S localhost -U sa -P "tunghpvn123" -C \
        -Q "SELECT 1" &> /dev/null; then
        echo "✅ SQL Server is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Timeout waiting for SQL Server"
        exit 1
    fi
    echo "Waiting... ($i/30)"
    sleep 2
done

# Create database if not exists
echo "🗄️ Creating database 'flight' if not exists..."
docker exec sqlserver /opt/mssql-tools18/bin/sqlcmd \
    -S localhost -U sa -P "tunghpvn123" -C \
    -Q "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'flight') CREATE DATABASE flight;"

# Run SQL scripts
echo "📜 Step 1/2: Running $SQL_FILE_RAW..."
cat "$SQL_FILE_RAW" | docker exec -i sqlserver /opt/mssql-tools18/bin/sqlcmd \
    -S localhost -U sa -P "tunghpvn123" -C -d flight

if [ $? -eq 0 ]; then
    echo "✅ flight-raw.sql executed successfully"
else
    echo "❌ Error executing flight-raw.sql"
    exit 1
fi

echo ""
echo "📜 Step 2/2: Running $SQL_FILE_UPDATE..."
cat "$SQL_FILE_UPDATE" | docker exec -i sqlserver /opt/mssql-tools18/bin/sqlcmd \
    -S localhost -U sa -P "tunghpvn123" -C -d flight

if [ $? -eq 0 ]; then
    echo "✅ flight-update.sql executed successfully"
else
    echo "❌ Error executing flight-update.sql"
    exit 1
fi

# Verify tables
echo "✅ Verifying tables..."
docker exec sqlserver /opt/mssql-tools18/bin/sqlcmd \
    -S localhost -U sa -P "tunghpvn123" -C \
    -d flight \
    -Q "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES ORDER BY TABLE_NAME;"

echo "🎉 Database initialization completed!"
