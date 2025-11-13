USE [flight];
GO

INSERT INTO TempActypeImport
    (Actype)
VALUES
    ('A320'),
    ('B777'),
    ('A380'),
    ('B747'),
    ('B737'),
    ('A330'),
    ('B787'),
    ('A321'),
    ('B777-300'),
    ('A350');
GO

-- ===================================================================
-- UPDATE TABLE
-- ===================================================================

/* ===================== Airport_Information ===================== */
IF COL_LENGTH('Airport_Information', 'created_at') IS NULL
    ALTER TABLE Airport_Information ADD created_at datetime2 DEFAULT SYSDATETIME();

IF COL_LENGTH('Airport_Information', 'updated_at') IS NULL
    ALTER TABLE Airport_Information ADD updated_at datetime2 DEFAULT SYSDATETIME();

IF EXISTS (
    SELECT 1
FROM sys.indexes
WHERE name = 'ix_Airport_Information_index'
    AND object_id = OBJECT_ID('Airport_Information')
)
    DROP INDEX ix_Airport_Information_index ON Airport_Information;

IF COL_LENGTH('Airport_Information', 'index') IS NULL
    ALTER TABLE Airport_Information ADD [index] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== Airline_Route_Details ===================== */
IF COL_LENGTH('Airline_Route_Details', 'created_at') IS NULL
    ALTER TABLE Airline_Route_Details ADD created_at datetime2 DEFAULT SYSDATETIME();

IF COL_LENGTH('Airline_Route_Details', 'updated_at') IS NULL
    ALTER TABLE Airline_Route_Details ADD updated_at datetime2 DEFAULT SYSDATETIME();

IF EXISTS (
    SELECT 1
FROM sys.indexes
WHERE name = 'ix_Airline_Route_Details_index'
    AND object_id = OBJECT_ID('Airline_Route_Details')
)
    DROP INDEX ix_Airline_Route_Details_index ON Airline_Route_Details;

IF COL_LENGTH('Airline_Route_Details', 'index') IS NULL
    ALTER TABLE Airline_Route_Details ADD [index] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== Region ===================== */
IF COL_LENGTH('Region', 'created_at') IS NULL
    ALTER TABLE Region ADD created_at datetime2 DEFAULT SYSDATETIME();

IF COL_LENGTH('Region', 'updated_at') IS NULL
    ALTER TABLE Region ADD updated_at datetime2 DEFAULT SYSDATETIME();

IF EXISTS (
    SELECT 1
FROM sys.indexes
WHERE name = 'ix_Region_index'
    AND object_id = OBJECT_ID('Region')
)
    DROP INDEX ix_Region_index ON Region;

IF COL_LENGTH('Region', 'index') IS NULL
    ALTER TABLE Region ADD [index] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== Airline_Details ===================== */
IF COL_LENGTH('Airline_Details', 'created_at') IS NULL
    ALTER TABLE Airline_Details ADD created_at datetime2 DEFAULT SYSDATETIME();

IF COL_LENGTH('Airline_Details', 'updated_at') IS NULL
    ALTER TABLE Airline_Details ADD updated_at datetime2 DEFAULT SYSDATETIME();

IF EXISTS (
    SELECT 1
FROM sys.indexes
WHERE name = 'ix_Airline_Details_index'
    AND object_id = OBJECT_ID('Airline_Details')
)
    DROP INDEX ix_Airline_Details_index ON Airline_Details;

IF COL_LENGTH('Airline_Details', 'index') IS NULL
    ALTER TABLE Airline_Details ADD [index] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== Route ===================== */
IF COL_LENGTH('Route', 'created_at') IS NULL
    ALTER TABLE [Route] ADD created_at datetime2 DEFAULT SYSDATETIME();

IF COL_LENGTH('Route', 'updated_at') IS NULL
    ALTER TABLE [Route] ADD updated_at datetime2 DEFAULT SYSDATETIME();

IF EXISTS (
    SELECT 1
FROM sys.indexes
WHERE name = 'ix_Route_index'
    AND object_id = OBJECT_ID('Route')
)
    DROP INDEX ix_Route_index ON [Route];

IF COL_LENGTH('Route', 'index') IS NULL
    ALTER TABLE [Route] ADD [index] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== actype_seat ===================== */
IF COL_LENGTH('actype_seat', 'created_at') IS NULL
    ALTER TABLE actype_seat ADD created_at datetime2 DEFAULT SYSDATETIME();

IF COL_LENGTH('actype_seat', 'updated_at') IS NULL
    ALTER TABLE actype_seat ADD updated_at datetime2 DEFAULT SYSDATETIME();

IF COL_LENGTH('actype_seat', 'index') IS NULL
    ALTER TABLE actype_seat ADD [index] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== seat_by_AC_type ===================== */
IF COL_LENGTH('seat_by_AC_type', 'created_at') IS NULL
    ALTER TABLE seat_by_AC_type ADD created_at datetime2 DEFAULT SYSDATETIME();

IF COL_LENGTH('seat_by_AC_type', 'updated_at') IS NULL
    ALTER TABLE seat_by_AC_type ADD updated_at datetime2 DEFAULT SYSDATETIME();

DECLARE @pk1 NVARCHAR(200);
SELECT @pk1 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('seat_by_AC_type') AND type = 'PK';
IF @pk1 IS NOT NULL EXEC('ALTER TABLE seat_by_AC_type DROP CONSTRAINT ' + @pk1);

IF COL_LENGTH('seat_by_AC_type', 'id') IS NULL
    ALTER TABLE seat_by_AC_type ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== flight_raw ===================== */
IF COL_LENGTH('flight_raw', 'created_at') IS NULL
    ALTER TABLE flight_raw ADD created_at datetime2 DEFAULT SYSDATETIME();

DECLARE @pk2 NVARCHAR(200);
SELECT @pk2 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('flight_raw') AND type = 'PK';
IF @pk2 IS NOT NULL EXEC('ALTER TABLE flight_raw DROP CONSTRAINT ' + @pk2);

IF COL_LENGTH('flight_raw', 'id') IS NULL
    ALTER TABLE flight_raw ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== flight_data_chot ===================== */
IF COL_LENGTH('flight_data_chot', 'created_at') IS NULL
    ALTER TABLE flight_data_chot ADD created_at datetime2 DEFAULT SYSDATETIME();

IF COL_LENGTH('flight_data_chot', 'updated_at') IS NULL
    ALTER TABLE flight_data_chot ADD updated_at datetime2 DEFAULT SYSDATETIME();

DECLARE @pk3 NVARCHAR(200);
SELECT @pk3 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('flight_data_chot') AND type = 'PK';
IF @pk3 IS NOT NULL EXEC('ALTER TABLE flight_data_chot DROP CONSTRAINT ' + @pk3);

IF COL_LENGTH('flight_data_chot', 'id') IS NULL
    ALTER TABLE flight_data_chot ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== flight_analyze ===================== */
IF COL_LENGTH('flight_analyze', 'created_at') IS NULL
    ALTER TABLE flight_analyze ADD created_at datetime2 DEFAULT SYSDATETIME();

IF COL_LENGTH('flight_analyze', 'updated_at') IS NULL
    ALTER TABLE flight_analyze ADD updated_at datetime2 DEFAULT SYSDATETIME();

DECLARE @pk4 NVARCHAR(200);
SELECT @pk4 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('flight_analyze') AND type = 'PK';
IF @pk4 IS NOT NULL EXEC('ALTER TABLE flight_analyze DROP CONSTRAINT ' + @pk4);

IF COL_LENGTH('flight_analyze', 'id') IS NULL
    ALTER TABLE flight_analyze ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== qua_dem ===================== */
IF COL_LENGTH('qua_dem', 'created_at') IS NULL
    ALTER TABLE qua_dem ADD created_at datetime2 DEFAULT SYSDATETIME();

DECLARE @pk5 NVARCHAR(200);
SELECT @pk5 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('qua_dem') AND type = 'PK';
IF @pk5 IS NOT NULL EXEC('ALTER TABLE qua_dem DROP CONSTRAINT ' + @pk5);

IF COL_LENGTH('qua_dem', 'id') IS NULL
    ALTER TABLE qua_dem ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== error_table ===================== */
IF COL_LENGTH('error_table', 'created_at') IS NULL
    ALTER TABLE error_table ADD created_at datetime2 DEFAULT SYSDATETIME();

DECLARE @pk6 NVARCHAR(200);
SELECT @pk6 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('error_table') AND type = 'PK';
IF @pk6 IS NOT NULL EXEC('ALTER TABLE error_table DROP CONSTRAINT ' + @pk6);

IF COL_LENGTH('error_table', 'id') IS NULL
    ALTER TABLE error_table ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== flight_clean_data_stg ===================== */
IF COL_LENGTH('flight_clean_data_stg', 'created_at') IS NULL
    ALTER TABLE flight_clean_data_stg ADD created_at datetime2 DEFAULT SYSDATETIME();

DECLARE @pk7 NVARCHAR(200);
SELECT @pk7 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('flight_clean_data_stg') AND type = 'PK';
IF @pk7 IS NOT NULL EXEC('ALTER TABLE flight_clean_data_stg DROP CONSTRAINT ' + @pk7);

IF COL_LENGTH('flight_clean_data_stg', 'id') IS NULL
    ALTER TABLE flight_clean_data_stg ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== import_log ===================== */
IF COL_LENGTH('import_log', 'created_at') IS NULL
    ALTER TABLE import_log ADD created_at datetime2 DEFAULT SYSDATETIME();

IF COL_LENGTH('import_log', 'updated_at') IS NULL
    ALTER TABLE import_log ADD updated_at datetime2 DEFAULT SYSDATETIME();

DECLARE @pk8 NVARCHAR(200);
SELECT @pk8 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('import_log') AND type = 'PK';
IF @pk8 IS NOT NULL EXEC('ALTER TABLE import_log DROP CONSTRAINT ' + @pk8);

IF COL_LENGTH('import_log', 'id') IS NOT NULL
    ALTER TABLE import_log DROP COLUMN id;

IF COL_LENGTH('import_log', 'id') IS NULL
    ALTER TABLE import_log ADD [id] INT IDENTITY(1,1) PRIMARY KEY;


/* ===================== Missing_Dimensions_Log ===================== */
IF COL_LENGTH('Missing_Dimensions_Log', 'created_at') IS NULL
    ALTER TABLE Missing_Dimensions_Log ADD created_at datetime2 DEFAULT SYSDATETIME();

DECLARE @pk9 NVARCHAR(200);
SELECT @pk9 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('Missing_Dimensions_Log') AND type = 'PK';
IF @pk9 IS NOT NULL EXEC('ALTER TABLE Missing_Dimensions_Log DROP CONSTRAINT ' + @pk9);

IF COL_LENGTH('Missing_Dimensions_Log', 'ID') IS NOT NULL
    ALTER TABLE Missing_Dimensions_Log DROP COLUMN [ID];

IF COL_LENGTH('Missing_Dimensions_Log', 'ID') IS NULL
    ALTER TABLE Missing_Dimensions_Log ADD [ID] INT IDENTITY(1,1) PRIMARY KEY;


/* ===================== TempActypeImport ===================== */
IF COL_LENGTH('TempActypeImport', 'created_at') IS NULL
    ALTER TABLE TempActypeImport ADD created_at datetime2 DEFAULT SYSDATETIME();

DECLARE @pk10 NVARCHAR(200);
SELECT @pk10 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('TempActypeImport') AND type = 'PK';
IF @pk10 IS NOT NULL EXEC('ALTER TABLE TempActypeImport DROP CONSTRAINT ' + @pk10);

IF COL_LENGTH('TempActypeImport', 'Actype') IS NOT NULL
    ALTER TABLE TempActypeImport DROP COLUMN [Actype];

IF COL_LENGTH('TempActypeImport', 'Actype') IS NULL
    ALTER TABLE TempActypeImport ADD [Actype] NVARCHAR(255) PRIMARY KEY;


/* ===================== TempRouteImport ===================== */
IF COL_LENGTH('TempRouteImport', 'created_at') IS NULL
    ALTER TABLE TempRouteImport ADD created_at datetime2 DEFAULT SYSDATETIME();

DECLARE @pk11 NVARCHAR(200);
SELECT @pk11 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('TempRouteImport') AND type = 'PK';
IF @pk11 IS NOT NULL EXEC('ALTER TABLE TempRouteImport DROP CONSTRAINT ' + @pk11);

IF COL_LENGTH('TempRouteImport', 'Route') IS NOT NULL
    ALTER TABLE TempRouteImport DROP COLUMN [Route];

IF COL_LENGTH('TempRouteImport', 'Route') IS NULL
    ALTER TABLE TempRouteImport ADD [Route] NVARCHAR(255) PRIMARY KEY;



-- ===================================================================
-- TRIGGERS FOR AUDIT COLUMNS (created_at, updated_at)
-- ===================================================================

-- ===================== Airport_Information =====================
GO
CREATE OR ALTER TRIGGER trg_Airport_Information_Insert
ON Airport_Information AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM Airport_Information t
   JOIN inserted i ON t.[index] = i.[index]
   WHERE t.created_at IS NULL;
GO

CREATE OR ALTER TRIGGER trg_Airport_Information_Update
ON Airport_Information AFTER UPDATE
AS UPDATE t SET t.updated_at = SYSDATETIME()
   FROM Airport_Information t
   JOIN inserted i ON t.[index] = i.[index];
GO


-- ===================== Airline_Route_Details =====================
GO
CREATE OR ALTER TRIGGER trg_Airline_Route_Details_Insert
ON Airline_Route_Details AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM Airline_Route_Details t
   JOIN inserted i ON t.[index] = i.[index]
   WHERE t.created_at IS NULL;
GO

CREATE OR ALTER TRIGGER trg_Airline_Route_Details_Update
ON Airline_Route_Details AFTER UPDATE
AS UPDATE t SET t.updated_at = SYSDATETIME()
   FROM Airline_Route_Details t
   JOIN inserted i ON t.[index] = i.[index];
GO


-- ===================== Region =====================
GO
CREATE OR ALTER TRIGGER trg_Region_Insert
ON Region AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM Region t
   JOIN inserted i ON t.[index] = i.[index]
   WHERE t.created_at IS NULL;
GO

CREATE OR ALTER TRIGGER trg_Region_Update
ON Region AFTER UPDATE
AS UPDATE t SET t.updated_at = SYSDATETIME()
   FROM Region t
   JOIN inserted i ON t.[index] = i.[index];
GO


-- ===================== Airline_Details =====================
GO
CREATE OR ALTER TRIGGER trg_Airline_Details_Insert
ON Airline_Details AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM Airline_Details t
   JOIN inserted i ON t.[index] = i.[index]
   WHERE t.created_at IS NULL;
GO

CREATE OR ALTER TRIGGER trg_Airline_Details_Update
ON Airline_Details AFTER UPDATE
AS UPDATE t SET t.updated_at = SYSDATETIME()
   FROM Airline_Details t
   JOIN inserted i ON t.[index] = i.[index];
GO


-- ===================== Route =====================
GO
CREATE OR ALTER TRIGGER trg_Route_Insert
ON [Route] AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM [Route] t
   JOIN inserted i ON t.[index] = i.[index]
   WHERE t.created_at IS NULL;
GO

CREATE OR ALTER TRIGGER trg_Route_Update
ON [Route] AFTER UPDATE
AS UPDATE t SET t.updated_at = SYSDATETIME()
   FROM [Route] t
   JOIN inserted i ON t.[index] = i.[index];
GO


-- ===================== actype_seat =====================
GO
CREATE OR ALTER TRIGGER trg_actype_seat_Insert
ON actype_seat AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM actype_seat t
   JOIN inserted i ON t.[index] = i.[index]
   WHERE t.created_at IS NULL;
GO

CREATE OR ALTER TRIGGER trg_actype_seat_Update
ON actype_seat AFTER UPDATE
AS UPDATE t SET t.updated_at = SYSDATETIME()
   FROM actype_seat t
   JOIN inserted i ON t.[index] = i.[index];
GO


-- ===================== seat_by_AC_type =====================
GO
CREATE OR ALTER TRIGGER trg_seat_by_AC_type_Insert
ON seat_by_AC_type AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM seat_by_AC_type t
   JOIN inserted i ON t.id = i.id
   WHERE t.created_at IS NULL;
GO

CREATE OR ALTER TRIGGER trg_seat_by_AC_type_Update
ON seat_by_AC_type AFTER UPDATE
AS UPDATE t SET t.updated_at = SYSDATETIME()
   FROM seat_by_AC_type t
   JOIN inserted i ON t.id = i.id;
GO


-- ===================== flight_raw =====================
GO
CREATE OR ALTER TRIGGER trg_flight_raw_Insert
ON flight_raw AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM flight_raw t
   JOIN inserted i ON t.id = i.id
   WHERE t.created_at IS NULL;
GO


-- ===================== flight_data_chot =====================
GO
CREATE OR ALTER TRIGGER trg_flight_data_chot_Insert
ON flight_data_chot AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM flight_data_chot t
   JOIN inserted i ON t.id = i.id
   WHERE t.created_at IS NULL;
GO

CREATE OR ALTER TRIGGER trg_flight_data_chot_Update
ON flight_data_chot AFTER UPDATE
AS UPDATE t SET t.updated_at = SYSDATETIME()
   FROM flight_data_chot t
   JOIN inserted i ON t.id = i.id;
GO


-- ===================== flight_analyze =====================
GO
CREATE OR ALTER TRIGGER trg_flight_analyze_Insert
ON flight_analyze AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM flight_analyze t
   JOIN inserted i ON t.id = i.id
   WHERE t.created_at IS NULL;
GO

CREATE OR ALTER TRIGGER trg_flight_analyze_Update
ON flight_analyze AFTER UPDATE
AS UPDATE t SET t.updated_at = SYSDATETIME()
   FROM flight_analyze t
   JOIN inserted i ON t.id = i.id;
GO


-- ===================== qua_dem =====================
GO
CREATE OR ALTER TRIGGER trg_qua_dem_Insert
ON qua_dem AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM qua_dem t
   JOIN inserted i ON t.id = i.id
   WHERE t.created_at IS NULL;
GO


-- ===================== error_table =====================
GO
CREATE OR ALTER TRIGGER trg_error_table_Insert
ON error_table AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM error_table t
   JOIN inserted i ON t.id = i.id
   WHERE t.created_at IS NULL;
GO


-- ===================== flight_clean_data_stg =====================
GO
CREATE OR ALTER TRIGGER trg_flight_clean_data_stg_Insert
ON flight_clean_data_stg AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM flight_clean_data_stg t
   JOIN inserted i ON t.id = i.id
   WHERE t.created_at IS NULL;
GO


-- ===================== import_log =====================
GO
CREATE OR ALTER TRIGGER trg_import_log_Insert
ON import_log AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM import_log t
   JOIN inserted i ON t.id = i.id
   WHERE t.created_at IS NULL;
GO

CREATE OR ALTER TRIGGER trg_import_log_Update
ON import_log AFTER UPDATE
AS UPDATE t SET t.updated_at = SYSDATETIME()
   FROM import_log t
   JOIN inserted i ON t.id = i.id;
GO


-- ===================== Missing_Dimensions_Log =====================
GO
CREATE OR ALTER TRIGGER trg_Missing_Dimensions_Log_Insert
ON Missing_Dimensions_Log AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM Missing_Dimensions_Log t
   JOIN inserted i ON t.ID = i.ID
   WHERE t.created_at IS NULL;
GO


-- ===================== TempActypeImport =====================
GO
CREATE OR ALTER TRIGGER trg_TempActypeImport_Insert
ON TempActypeImport AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM TempActypeImport t
   JOIN inserted i ON t.Actype = i.Actype
   WHERE t.created_at IS NULL;
GO


-- ===================== TempRouteImport =====================
GO
CREATE OR ALTER TRIGGER trg_TempRouteImport_Insert
ON TempRouteImport AFTER INSERT
AS UPDATE t SET t.created_at = SYSDATETIME()
   FROM TempRouteImport t
   JOIN inserted i ON t.[Route] = i.[Route]
   WHERE t.created_at IS NULL;
GO
