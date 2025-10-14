USE [flight];
GO

-- ===================================================================
-- CORE MASTER DATA TABLES
-- ===================================================================

-- Airport Information - Master data for all airports
-- Contains IATA codes, names, cities and countries for airports worldwide
CREATE TABLE Airport_Information
(
    [index] BIGINT IDENTITY(1,1) PRIMARY KEY,
    IATACode NVARCHAR(10) NOT NULL,
    -- 3-letter IATA airport code (e.g., SGN, HAN)
    [Airport Name] NVARCHAR(255) NULL,
    -- Full airport name
    City NVARCHAR(100) NULL,
    -- City where airport is located
    Country NVARCHAR(100) NULL,
    -- Country where airport is located
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_Airport_Information_IATACode ON Airport_Information(IATACode);
CREATE INDEX IX_Airport_Information_Country ON Airport_Information(Country);
GO

-- Airline Route Details - Information about flight routes and sectors
-- Contains route data including distances, countries, and domestic/international classification
CREATE TABLE Airline_Route_Details
(
    [index] BIGINT IDENTITY(1,1) PRIMARY KEY,
    Sector NVARCHAR(20) NOT NULL,
    -- Route sector code (e.g., SGNHAN)
    [Distance mile GDS] BIGINT NULL,
    -- Distance in miles from GDS
    [Distance km GDS] FLOAT NULL,
    -- Distance in kilometers from GDS
    Sector_2 NVARCHAR(20) NULL,
    -- Alternative sector format
    Route NVARCHAR(100) NULL,
    -- Route description
    [Country 1] NVARCHAR(100) NULL,
    -- Origin country
    [Country 2] NVARCHAR(100) NULL,
    -- Destination country
    Country NVARCHAR(100) NULL,
    -- Primary country for route classification
    [DOM/INT] NVARCHAR(10) NULL,
    -- Domestic (DOM) or International (INT)
    Area NVARCHAR(100) NULL,
    -- Geographic area/region
    inserted_time DATETIME DEFAULT GETDATE() NOT NULL,
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_Airline_Route_Details_Sector ON Airline_Route_Details(Sector);
CREATE INDEX IX_Airline_Route_Details_Route ON Airline_Route_Details(Route);
CREATE INDEX IX_Airline_Route_Details_Country ON Airline_Route_Details(Country);
GO

-- Region Information - Geographic regions for countries
-- Maps countries to their respective regions for reporting purposes
CREATE TABLE Region
(
    [index] BIGINT IDENTITY(1,1) PRIMARY KEY,
    Country NVARCHAR(100) NOT NULL,
    -- Country name
    Region NVARCHAR(100) NOT NULL,
    -- Geographic region
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_Region_Country ON Region(Country);
CREATE INDEX IX_Region_Region ON Region(Region);
GO

-- Airline Details - Information about airline carriers
-- Contains airline codes, names and related information
CREATE TABLE Airline_Details
(
    [index] BIGINT IDENTITY(1,1) PRIMARY KEY,
    CARRIER NVARCHAR(10) NOT NULL,
    -- 2-letter airline code (e.g., VN, VJ)
    QG NVARCHAR(10) NULL,
    -- Country code for airline
    [Airlines name] NVARCHAR(255) NULL,
    -- Full airline name
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_Airline_Details_CARRIER ON Airline_Details(CARRIER);
GO

-- Route Master Data - Detailed route information including flight times and distances
-- Complete route database with operational details
CREATE TABLE Route
(
    [index] BIGINT IDENTITY(1,1) PRIMARY KEY,
    [ROUTE] NVARCHAR(20) NOT NULL,
    -- Route code
    [AC] NVARCHAR(20) NULL,
    -- Aircraft type for route
    [Route_ID] NVARCHAR(50) NULL,
    -- Unique route identifier
    [FH (THEO GIỜ)] TIME(7) NULL,
    -- Flight hours (time format)
    [FLIGHT HOUR] FLOAT NULL,
    -- Flight hours (decimal)
    [TAXI] FLOAT NULL,
    -- Taxi time in hours
    [BLOCK HOUR] FLOAT NULL,
    -- Total block time
    [DISTANCE KM] FLOAT NULL,
    -- Distance in kilometers
    [Loại] NVARCHAR(50) NULL,
    -- Route type in Vietnamese
    [Type] NVARCHAR(50) NULL,
    -- Route type in English
    [Country] NVARCHAR(100) NULL,
    -- Country classification
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_Route_ROUTE ON Route([ROUTE]);
CREATE INDEX IX_Route_Country ON Route([Country]);
GO

-- ===================================================================
-- AIRCRAFT AND SEAT CONFIGURATION TABLES
-- ===================================================================

-- Aircraft Type Seat Configuration
-- Maps aircraft types to their standard seat capacity
CREATE TABLE actype_seat
(
    [index] BIGINT IDENTITY(1,1) PRIMARY KEY,
    actype NVARCHAR(50) NOT NULL UNIQUE,
    -- Aircraft type code (e.g., A320, B777)
    seat BIGINT NOT NULL,
    -- Standard seat capacity
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_actype_seat_actype ON actype_seat(actype);
GO

-- Aircraft Registration Details
-- Individual aircraft registration and seat configuration
CREATE TABLE seat_by_AC_type
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    ACRegNo NVARCHAR(20) NOT NULL,
    -- Aircraft registration number
    Brand NVARCHAR(50) NULL,
    -- Aircraft manufacturer
    AC_Type NVARCHAR(50) NULL,
    -- Aircraft type
    Seat BIGINT NULL,
    -- Actual seat count for this aircraft
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_seat_by_AC_type_ACRegNo ON seat_by_AC_type(ACRegNo);
CREATE INDEX IX_seat_by_AC_type_AC_Type ON seat_by_AC_type(AC_Type);
GO

-- ===================================================================
-- FLIGHT DATA TABLES
-- ===================================================================

-- Flight Raw Data - Initial data import from Excel files
-- Stores raw flight data before processing and validation
CREATE TABLE flight_raw
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    flightdate NVARCHAR(255) NULL,
    -- Flight date (various formats from Excel)
    flightno NVARCHAR(50) NULL,
    -- Flight number
    route NVARCHAR(100) NULL,
    -- Route (e.g., SGN-HAN)
    actype NVARCHAR(50) NULL,
    -- Aircraft type
    seat BIGINT NULL,
    -- Seat capacity
    adl FLOAT NULL,
    -- Adult passengers
    chd FLOAT NULL,
    -- Child passengers
    cgo FLOAT NULL,
    -- Cargo weight
    mail FLOAT NULL,
    -- Mail weight
    totalpax FLOAT NULL,
    -- Total passengers (calculated)
    source NVARCHAR(500) NULL,
    -- Source file name
    acregno NVARCHAR(50) NULL,
    -- Aircraft registration
    sheet_name NVARCHAR(255) NULL,
    -- Excel sheet name
    int_dom NVARCHAR(10) NULL,
    -- Domestic/International flag
    [Is_InvalidFlightDate] INT NULL,
    -- Validation flags
    [Is_InvalidPassengerCargo] INT NULL,
    -- Validation flags
    [Is_InvalidRoute] INT NULL,
    -- Validation flags
    [Is_InvalidActypeSeat] INT NULL,
    -- Validation flags
    ErrorReason NVARCHAR(MAX) NULL,
    -- Description of errors
    TotalErrors INT NULL,
    -- Total error count
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_flight_raw_flightdate ON flight_raw(flightdate);
CREATE INDEX IX_flight_raw_route ON flight_raw(route);
CREATE INDEX IX_flight_raw_source ON flight_raw(source);
GO

-- Flight Data Main - Processed and validated flight data
-- Primary table for clean flight data after validation
CREATE TABLE flight_data_chot
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    convert_date BIGINT NULL,
    -- Flight date in YYYYMMDD format
    flightno NVARCHAR(50) NULL,
    -- Flight number
    route NVARCHAR(100) NULL,
    -- Route
    actype NVARCHAR(50) NULL,
    -- Aircraft type
    totalpax FLOAT NULL,
    -- Total passengers
    cgo FLOAT NULL,
    -- Cargo weight
    mail FLOAT NULL,
    -- Mail weight
    acregno NVARCHAR(50) NULL,
    -- Aircraft registration
    source NVARCHAR(500) NULL,
    -- Source file
    sheet_name NVARCHAR(255) NULL,
    -- Source sheet
    region_type INT NOT NULL DEFAULT 0,
    -- Region classification
    seat BIGINT NULL,
    -- Seat capacity
    week_number INT NULL,
    -- Week number
    year_number INT NULL,
    -- Year
    note NVARCHAR(255) NULL,
    -- Notes
    type_filter INT NULL,
    -- Flight type filter
    inserted_time DATETIME DEFAULT GETDATE() NOT NULL,
    int_dom_ NVARCHAR(10) NULL,
    -- Domestic/International
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_flight_data_chot_convert_date ON flight_data_chot(convert_date);
CREATE INDEX IX_flight_data_chot_route ON flight_data_chot(route);
CREATE INDEX IX_flight_data_chot_type_filter ON flight_data_chot(type_filter);
CREATE INDEX IX_flight_data_chot_flightno ON flight_data_chot(flightno);
CREATE INDEX IX_flight_data_chot_actype ON flight_data_chot(actype);
CREATE INDEX IX_flight_data_chot_source ON flight_data_chot(source);
CREATE INDEX IX_flight_data_chot_sheet_name ON flight_data_chot(sheet_name);
GO

-- Flight Analysis Table - Enhanced flight data with additional calculations
-- Contains processed flight data with geographic and operational analysis
CREATE TABLE flight_analyze
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    [FLIGHT_DATE] NVARCHAR(50) NULL,
    -- Original flight date
    [FLIGHT_DATE_FORMAT] DATE NULL,
    -- Standardized flight date
    [FLIGHT_NO] NVARCHAR(50) NULL,
    -- Flight number
    [ACTYPE] NVARCHAR(50) NULL,
    -- Aircraft type
    [SECTOR] NVARCHAR(20) NULL,
    -- Route sector
    [TOTAL_PAX] FLOAT NULL,
    -- Total passengers
    [CGO] FLOAT NULL,
    -- Cargo
    [MAIL] FLOAT NULL,
    -- Mail
    [SEAT] BIGINT NULL,
    -- Seat capacity
    [DEPARTURE] NVARCHAR(10) NULL,
    -- Departure airport code
    [ARRIVES] NVARCHAR(10) NULL,
    -- Arrival airport code
    [AIRLINES NAME] NVARCHAR(255) NULL,
    -- Airline name
    [COUNTRY] NVARCHAR(100) NULL,
    -- Route country
    [DOM/INT] NVARCHAR(10) NULL,
    -- Domestic/International
    [COM] NVARCHAR(1) NOT NULL DEFAULT '',
    -- Commercial flag
    [REGION] NVARCHAR(100) NULL,
    -- Geographic region
    [CITY_ARRIVES] NVARCHAR(100) NULL,
    -- Arrival city
    [COUNTRY_ARRIVES] NVARCHAR(100) NULL,
    -- Arrival country
    [CITY_DEPARTURE] NVARCHAR(100) NULL,
    -- Departure city
    [COUNTRY_DEPARTURE] NVARCHAR(100) NULL,
    -- Departure country
    [source] NVARCHAR(500) NULL,
    -- Data source
    [rnk_sg] INT NOT NULL DEFAULT 0,
    -- Ranking
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_flight_analyze_FLIGHT_DATE_FORMAT ON flight_analyze([FLIGHT_DATE_FORMAT]);
CREATE INDEX IX_flight_analyze_FLIGHT_NO ON flight_analyze([FLIGHT_NO]);
CREATE INDEX IX_flight_analyze_SECTOR ON flight_analyze([SECTOR]);
CREATE INDEX IX_flight_analyze_COM ON flight_analyze([COM]);
CREATE INDEX IX_flight_analyze_REGION ON flight_analyze([REGION]);
GO

-- Overnight Flights - Special tracking for overnight flight patterns
-- Tracks flights that require overnight stays or connections
CREATE TABLE qua_dem
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    flight_date_format DATE NULL,
    -- First flight date
    source NVARCHAR(500) NULL,
    -- Source airport
    sortedroute NVARCHAR(20) NULL,
    -- Standardized route
    flight_no NVARCHAR(50) NULL,
    -- Flight number
    flight_date_format_ DATE NULL,
    -- Second flight date
    source_ NVARCHAR(500) NULL,
    -- Destination airport
    sortedroute_ NVARCHAR(20) NULL,
    -- Return route
    flight_no_ NVARCHAR(50) NULL,
    -- Return flight number
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_qua_dem_flight_date_format ON qua_dem(flight_date_format);
CREATE INDEX IX_qua_dem_flight_no ON qua_dem(flight_no);
GO

-- ===================================================================
-- DATA VALIDATION AND ERROR HANDLING
-- ===================================================================

-- Error Table - Stores records that failed validation
-- Contains flight data that couldn't be processed due to validation errors
CREATE TABLE error_table
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    flightdate NVARCHAR(255) NULL,
    -- Original flight date
    flightno NVARCHAR(50) NULL,
    -- Flight number
    route NVARCHAR(100) NULL,
    -- Route
    actype NVARCHAR(50) NULL,
    -- Aircraft type
    seat BIGINT NULL,
    -- Seat capacity
    adl FLOAT NULL,
    -- Adult passengers
    chd FLOAT NULL,
    -- Child passengers
    cgo FLOAT NULL,
    -- Cargo
    mail FLOAT NULL,
    -- Mail
    source NVARCHAR(500) NULL,
    -- Source file
    acregno NVARCHAR(50) NULL,
    -- Aircraft registration
    sheet_name NVARCHAR(255) NULL,
    -- Sheet name
    totalpax FLOAT NULL,
    -- Total passengers
    int_dom NVARCHAR(10) NULL,
    -- Domestic/International
    Is_InvalidFlightDate INT NULL,
    -- Date validation flag
    Is_InvalidPassengerCargo INT NULL,
    -- Passenger/cargo validation flag
    Is_InvalidRoute INT NULL,
    -- Route validation flag
    Is_InvalidActypeSeat INT NULL,
    -- Aircraft type validation flag
    ErrorReason NVARCHAR(MAX) NULL,
    -- Description of errors
    TotalErrors INT NULL,
    -- Total error count
    time_import DATETIME NOT NULL DEFAULT GETDATE(),
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_error_table_TotalErrors ON error_table(TotalErrors);
CREATE INDEX IX_error_table_source ON error_table(source);
CREATE INDEX IX_error_table_flightno ON error_table(flightno);
CREATE INDEX IX_error_table_route ON error_table(route);
CREATE INDEX IX_error_table_actype ON error_table(actype);
GO

-- Flight Clean Data Staging - Temporary table for data processing
-- Used during the data cleaning and validation process
CREATE TABLE flight_clean_data_stg
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    flightdate NVARCHAR(255) NULL,
    -- Flight date
    flightno NVARCHAR(50) NULL,
    -- Flight number
    route NVARCHAR(100) NULL,
    -- Route
    actype NVARCHAR(50) NULL,
    -- Aircraft type
    seat BIGINT NULL,
    -- Seat capacity
    adl FLOAT NULL,
    -- Adult passengers
    chd FLOAT NULL,
    -- Child passengers
    cgo FLOAT NULL,
    -- Cargo
    mail FLOAT NULL,
    -- Mail
    source NVARCHAR(500) NULL,
    -- Source file
    acregno NVARCHAR(50) NULL,
    -- Aircraft registration
    sheet_name NVARCHAR(255) NULL,
    -- Sheet name
    totalpax FLOAT NULL,
    -- Total passengers
    int_dom NVARCHAR(10) NULL,
    -- Domestic/International
    Is_InvalidFlightDate INT NULL,
    -- Validation flags
    Is_InvalidPassengerCargo INT NULL,
    Is_InvalidRoute INT NULL,
    Is_InvalidActypeSeat INT NULL,
    ErrorReason NVARCHAR(MAX) NULL,
    -- Error description
    TotalErrors INT NULL,
    -- Error count
    inserted_time DATETIME DEFAULT GETDATE() NOT NULL,
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_flight_clean_data_stg_source ON flight_clean_data_stg(source);
GO

-- ===================================================================
-- IMPORT AND LOGGING TABLES
-- ===================================================================

-- Import Log - Tracks file import history and status
-- Maintains record of all file imports with metadata
CREATE TABLE import_log
(
    id INT IDENTITY(1,1) PRIMARY KEY,
    file_name NVARCHAR(255) NOT NULL,
    -- Name of imported file
    import_date DATETIME DEFAULT GETDATE() NOT NULL,
    -- Import timestamp
    source_type NVARCHAR(50) NULL,
    -- Type of source (MN, MB, MT, etc.)
    status NVARCHAR(20) DEFAULT 'imported' NOT NULL,
    -- Import status
    row_count INT NULL,
    -- Number of rows imported
    clean_data INT NULL,
    -- Flag for cleaned data
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_import_log_file_name ON import_log(file_name);
CREATE INDEX IX_import_log_import_date ON import_log(import_date);
GO

-- Missing Dimensions Log - Tracks missing reference data
-- Logs aircraft types and routes that are missing from master data
CREATE TABLE Missing_Dimensions_Log
(
    ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [Type] NVARCHAR(50) NULL,
    -- Type of missing data (ACTYPE/ROUTE)
    [Value] NVARCHAR(255) NULL,
    -- Missing value
    SourceSheet NVARCHAR(255) NULL,
    -- Source sheet where missing data found
    CreatedAt DATETIME NULL DEFAULT GETDATE(),
    -- When missing data was logged
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);

CREATE INDEX IX_Missing_Dimensions_Log_Type ON Missing_Dimensions_Log([Type]);
CREATE INDEX IX_Missing_Dimensions_Log_Value ON Missing_Dimensions_Log([Value]);
GO

-- ===================================================================
-- TEMPORARY IMPORT TABLES
-- ===================================================================

-- Temporary Aircraft Type Import - For bulk importing aircraft data
-- Used when importing aircraft type and seat configuration data
CREATE TABLE TempActypeImport
(
    Actype NVARCHAR(255) NOT NULL PRIMARY KEY,
    -- Aircraft type code
    Seat INT NULL,
    -- Seat capacity
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);
GO

-- Temporary Route Import - For bulk importing route data
-- Used when importing route and flight time data
CREATE TABLE TempRouteImport
(
    Route NVARCHAR(255) NOT NULL PRIMARY KEY,
    -- Route code
    AC NVARCHAR(50) NULL,
    -- Aircraft type
    Route_ID NVARCHAR(50) NULL,
    -- Route identifier
    [FH (THEO GIỜ)] DECIMAL(10, 2) NULL,
    -- Flight hours
    [FLIGHT HOUR] DECIMAL(10, 2) NULL,
    -- Flight duration
    TAXI DECIMAL(10, 2) NULL,
    -- Taxi time
    [BLOCK HOUR] DECIMAL(10, 2) NULL,
    -- Block time
    [DISTANCE KM] INT NULL,
    -- Distance in kilometers
    [Loại] NVARCHAR(50) NULL,
    -- Route type (Vietnamese)
    [Type] NVARCHAR(50) NULL,
    -- Route type (English)
    Country NVARCHAR(100) NULL,
    -- Country classification
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);
GO

-- ===================================================================
-- VIEWS FOR BUSINESS INTELLIGENCE
-- ===================================================================

-- Final Source View for Power BI - Comprehensive flight data view
-- Combines domestic, international, and overnight flights for reporting
CREATE VIEW source_pbi_final
AS
    WITH
        flight_data
        AS
        (
            SELECT *,
                CASE 
            WHEN totalpax = 0 AND (ISNULL(cgo,0) + ISNULL(mail,0) > 0) THEN 0 
            WHEN totalpax > 0 THEN 1 
        END AS Flight_type
            FROM flight_data_chot
            WHERE type_filter > 0
                AND note IS NULL
                AND type_filter > 0
        )
    SELECT
        f.*,
        LEFT(F.ROUTE, 3) AS DEPARTURE, -- Departure airport code
        RIGHT(F.ROUTE, 3) AS ARRIVES, -- Arrival airport code
        A1.[AIRLINES NAME], -- Airline name
        A.COUNTRY, -- Route country
        A.[DOM/INT], -- Domestic/International classification                             
        CASE 
        WHEN R.COUNTRY = 'VIETNAM' THEN A.AREA 
        ELSE ISNULL(R.REGION, r.Country)
    END AS REGION, -- Geographic region
        AI.CITY AS CITY_ARRIVES, -- Arrival city
        AI.COUNTRY AS COUNTRY_ARRIVES, -- Arrival country
        AI1.CITY AS CITY_DEPARTURE, -- Departure city
        AI1.COUNTRY AS COUNTRY_DEPARTURE
    -- Departure country
    FROM
        flight_data F
        LEFT JOIN
        AIRLINE_DETAILS A1
        ON LEFT(F.FLIGHTNO, 2) = A1.CARRIER -- Join with airline info
        LEFT JOIN
        AIRLINE_ROUTE_DETAILS A
        ON A.SECTOR = REPLACE(F.ROUTE, '-', '') -- Join with route info
        LEFT JOIN
        REGION R
        ON R.COUNTRY = A.COUNTRY -- Join with region info
        LEFT JOIN
        AIRPORT_INFORMATION AI
        ON AI.IATACODE = RIGHT(F.ROUTE, 3) -- Join arrival airport info
        LEFT JOIN
        AIRPORT_INFORMATION AI1
        ON AI1.IATACODE = LEFT(F.ROUTE, 3);           -- Join departure airport info
GO

-- ===================================================================
-- STORED PROCEDURES FOR DATA PROCESSING
-- ===================================================================

-- Main Data Cleaning and Processing Procedure
-- Processes raw flight data through validation and loads into main tables
CREATE OR ALTER PROCEDURE usp_CleanAndProcessFlightData
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
       
        ------------------------------------------------------------------------------------
        -- 1. PREPARE RAW DATA (Initial totalpax calculation)
        -- Sets totalpax in flight_raw based on adl+chd if available, otherwise keeps existing totalpax.
        ------------------------------------------------------------------------------------
        PRINT '1. Preparing raw data in flight_raw...';

        ------------------------------------------------------------------------------------
        -- 2. LOAD DATA FROM RAW TO STAGING
        -- Inserts data from flight_raw into flight_clean_data_stg for files
        -- that haven't been processed yet (clean_data IS NULL in import_log).
        ------------------------------------------------------------------------------------
        PRINT '2. Loading data from flight_raw to flight_clean_data_stg...';

        INSERT INTO flight_clean_data_stg
        (
        flightdate, flightno, route, actype, seat, adl, chd, cgo, mail,
        source, acregno, sheet_name, totalpax, int_dom,
        Is_InvalidFlightDate, Is_InvalidPassengerCargo, Is_InvalidRoute,
        Is_InvalidActypeSeat, ErrorReason, TotalErrors
        )
    SELECT
        flightdate, flightno, route, actype, seat, adl, chd, cgo, mail,
        source, acregno, sheet_name, totalpax, int_dom,
        0, 0, 0, 0, NULL, 0
    -- Initialize error flags and counts
    FROM flight_raw
    WHERE source IN (SELECT file_name
    FROM import_log
    WHERE file_name NOT IN (
                                                                                                                                                                    SELECT DISTINCT source
        FROM flight_clean_data_stg
    UNION
        SELECT DISTINCT source
        FROM flight_data_chot
        ));

        ------------------------------------------------------------------------------------
        -- 3. ENRICH DATA IN STAGING TABLE (flight_clean_data_stg)
        ------------------------------------------------------------------------------------
        PRINT '3. Enriching data in flight_clean_data_stg...';

        -- 3.1. Update totalpax (again, consistent with original script)
        -- This ensures totalpax is based on adl+chd if present, even if it was pre-filled.
        UPDATE flight_clean_data_stg
        SET totalpax = CASE
                         WHEN ISNULL(adl, 0) + ISNULL(chd, 0) > 0 THEN ISNULL(adl, 0) + ISNULL(chd, 0)
                         ELSE ISNULL(totalpax, 0)
                       END;

        -- 3.2. Update int_dom (International/Domestic)
        -- Determines if a flight is DOM (Domestic) or INT (International) based on airport countries.
        -- Assumes route is 'XXX-YYY' where XXX is departure and YYY is arrival.
        UPDATE fcs
        SET fcs.int_dom =
            CASE
                WHEN dep.Country = 'Vietnam' AND arr.Country = 'Vietnam' THEN 'DOM'
                WHEN dep.Country IS NOT NULL AND arr.Country IS NOT NULL AND (dep.Country != 'Vietnam' OR arr.Country != 'Vietnam') THEN 'INT'
                ELSE NULL -- If airport country information is missing
            END
        FROM flight_clean_data_stg fcs
        LEFT JOIN Airport_Information dep ON LEFT(TRIM(fcs.route), 3) = dep.IATACode
        LEFT JOIN Airport_Information arr ON RIGHT(TRIM(fcs.route), 3) = arr.IATACode
        WHERE fcs.int_dom IS NULL; -- Only update if not already set

        -- 3.3. Update seat capacity
        -- Fills missing seat counts from the actype_seat table.
        UPDATE fcs
        SET fcs.seat = COALESCE(fcs.seat, s.seat) -- Use existing seat if not null, otherwise lookup
        FROM flight_clean_data_stg fcs
        LEFT JOIN actype_seat s ON LOWER(TRIM(fcs.actype)) = LOWER(TRIM(s.actype));

        ------------------------------------------------------------------------------------
        -- 4. VALIDATE DATA IN STAGING TABLE (flight_clean_data_stg)
        ------------------------------------------------------------------------------------
        PRINT '4. Validating data in flight_clean_data_stg...';
        UPDATE fcs
        SET
            -- 4.1. Validate Flight Date Format and Convertibility
            Is_InvalidFlightDate = CAST(CASE
                WHEN fcs.flightdate IS NULL THEN 1 -- Null date is invalid
                WHEN -- Attempt to parse various common date formats
                    CASE
						WHEN ISNUMERIC(fcs.flightdate) = 1 THEN DATEADD(DAY, CAST(fcs.flightdate AS INT), '1899-12-30')
						WHEN fcs.flightdate LIKE '__/_/____' THEN TRY_CONVERT(DATE, fcs.flightdate, 103)
                        WHEN fcs.flightdate LIKE '__/__/____' THEN TRY_CONVERT(DATE, fcs.flightdate, 103) -- dd/MM/yyyy
                        WHEN fcs.flightdate LIKE '____-__-__ %' THEN TRY_CONVERT(DATE, LEFT(fcs.flightdate, 10), 120) -- yyyy-MM-dd HH:mm:ss
                        WHEN fcs.flightdate LIKE '____/__/__' THEN TRY_CONVERT(DATE, fcs.flightdate, 111) -- yyyy/MM/dd
                        WHEN LEN(TRIM(fcs.flightdate)) = 8 AND ISNUMERIC(TRIM(fcs.flightdate)) = 1 THEN TRY_CONVERT(DATE, TRIM(fcs.flightdate), 112) -- yyyyMMdd
                        WHEN TRY_CONVERT(DATETIME, fcs.flightdate) IS NOT NULL THEN CONVERT(DATE, fcs.flightdate) -- General datetime string
                        ELSE NULL
                    END IS NULL
                THEN 1 ELSE 0 END AS BIT),

            -- 4.2. Validate Passenger + Cargo Load
            -- Checks if total payload (passengers + cargo + mail) is zero or less.
            Is_InvalidPassengerCargo = CAST(CASE
                WHEN ISNULL(fcs.totalpax, 0) + ISNULL(fcs.cgo, 0) + ISNULL(fcs.mail, 0) <= 0
                THEN 1 ELSE 0 END AS BIT),

            -- 4.3. Validate Route
            -- Checks if the route exists in AIRLINE_ROUTE_DETAILS.
            -- Normalizes route to 'SMALLER_CODE-LARGER_CODE' for lookup.
            Is_InvalidRoute = CAST(CASE 
                WHEN NOT EXISTS (
                    SELECT 1
    FROM Airline_Route_Details ARD
    WHERE ARD.SECTOR = (
                        CASE
                            WHEN LEN(TRIM(fcs.route)) = 7 AND CHARINDEX('-', fcs.route) > 0 THEN
                                CASE
                                    WHEN LEFT(fcs.route, 3) < RIGHT(fcs.route, 3) 
                                        THEN CONCAT(LEFT(fcs.route, 3), RIGHT(fcs.route, 3))
                                    ELSE CONCAT(RIGHT(fcs.route, 3), LEFT(fcs.route, 3))
                                END
                            ELSE NULL
                        END
                    )
                ) THEN 1 ELSE 0 END AS BIT),

            -- 4.4. Validate Actype (Aircraft Type) and Seat
            -- Checks if actype exists in actype_seat, unless it's a pure cargo/mail flight.
            Is_InvalidActypeSeat = CAST(CASE
                WHEN (ISNULL(fcs.cgo, 0) + ISNULL(fcs.mail, 0) > 0 AND ISNULL(fcs.totalpax,0) = 0) THEN 0 -- If it's a cargo/mail only flight
                WHEN NOT EXISTS (
                    SELECT 1
    FROM actype_seat ATS
    WHERE LOWER(TRIM(ATS.actype)) = LOWER(TRIM(fcs.actype))
                ) THEN 1 ELSE 0 END AS BIT)
        FROM flight_clean_data_stg fcs;

        -- 4.5. Compile Error Reasons and Total Errors
        UPDATE flight_clean_data_stg
        SET
            ErrorReason = STUFF(
                COALESCE(CASE WHEN Is_InvalidFlightDate = 1 THEN N', flightdate không hợp lệ' ELSE N'' END, N'') +
                COALESCE(CASE WHEN Is_InvalidPassengerCargo = 1 THEN N', tổng số khách + hàng hóa <= 0' ELSE N'' END, N'') +
                COALESCE(CASE WHEN Is_InvalidRoute = 1 THEN N', route không tồn tại trong AIRLINE_ROUTE_DETAILS' ELSE N'' END, N'') +
                COALESCE(CASE WHEN Is_InvalidActypeSeat = 1 THEN N', actype không tồn tại trong actype_seat hoặc không phải chuyến bay chở hàng' ELSE N'' END, N''),
                1, 2, N'' -- Removes leading ', '
            ),
            TotalErrors =
                ISNULL(Is_InvalidFlightDate, 0) +
                ISNULL(Is_InvalidPassengerCargo, 0) +
                ISNULL(Is_InvalidRoute, 0) +
                ISNULL(Is_InvalidActypeSeat, 0);

        ------------------------------------------------------------------------------------
        -- 5. MOVE CLEAN DATA TO FINAL TABLE (flight_data_chot)
        ------------------------------------------------------------------------------------
        PRINT '5. Moving clean data from staging to flight_data_chot...';
        INSERT INTO flight_data_chot
        (
        convert_date, flightno, route, actype, totalpax, cgo, mail,
        acregno, source, sheet_name, seat, region_type, int_dom_
        )
    SELECT
        FORMAT( -- Standardizes the date to 'yyyyMMdd' string
                CASE
                    WHEN fcs.flightdate LIKE '__/__/____' THEN TRY_CONVERT(DATE, fcs.flightdate, 103)
                    WHEN fcs.flightdate LIKE '____-__-__ %' THEN TRY_CONVERT(DATE, LEFT(fcs.flightdate, 10), 120)
                    WHEN fcs.flightdate LIKE '____/__/__' THEN TRY_CONVERT(DATE, fcs.flightdate, 111)
                    WHEN LEN(TRIM(fcs.flightdate)) = 8 AND ISNUMERIC(TRIM(fcs.flightdate)) = 1 THEN TRY_CONVERT(DATE, TRIM(fcs.flightdate), 112)
                    WHEN TRY_CONVERT(DATETIME, fcs.flightdate) IS NOT NULL THEN CONVERT(DATE, fcs.flightdate)
                    ELSE NULL
                END,
            'yyyyMMdd') AS convert_date,
        fcs.flightno, fcs.route, fcs.actype, fcs.totalpax, fcs.cgo, fcs.mail,
        fcs.acregno, fcs.source, fcs.sheet_name, fcs.seat,
        10 AS region_type, -- Static value
        int_dom
    FROM flight_clean_data_stg fcs
    WHERE fcs.TotalErrors = 0;

        -- Remove clean data from staging
        DELETE FROM flight_clean_data_stg WHERE TotalErrors = 0;

        ------------------------------------------------------------------------------------
        -- 6. MOVE ERRORED DATA FROM STAGING TO ERROR TABLE (error_table)
        ------------------------------------------------------------------------------------
        PRINT '6. Moving errored data from staging to error_table...';
        INSERT INTO error_table
        (
        flightdate, flightno, route, actype, seat, adl, chd, cgo, mail,
        source, acregno, sheet_name, totalpax, int_dom, Is_InvalidFlightDate,
        Is_InvalidPassengerCargo, Is_InvalidRoute, Is_InvalidActypeSeat,
        ErrorReason, TotalErrors
        )
    SELECT
        flightdate, flightno, route, actype, seat, adl, chd, cgo, mail,
        source, acregno, sheet_name, totalpax, int_dom, Is_InvalidFlightDate,
        Is_InvalidPassengerCargo, Is_InvalidRoute, Is_InvalidActypeSeat,
        ErrorReason, TotalErrors
    FROM flight_clean_data_stg; -- All remaining records have TotalErrors > 0

        -- Clear staging table completely
        DELETE FROM flight_clean_data_stg;

        -- Update type_filter for new records
		UPDATE flight_data_chot
		SET type_filter = CASE 
			WHEN CHARINDEX('SGN', route) > 1 AND sheet_name != 'SGN' THEN 0 
			WHEN sheet_name = 'SGN' THEN 1 
			WHEN int_dom_ = 'INT' THEN 2 
			WHEN sheet_name = LEFT(route,3) THEN 3 
			ELSE -1 
		END 
		WHERE inserted_time >= DATEADD(MINUTE, -5, GETDATE())
        AND type_filter IS NULL;

    END TRY
	BEGIN CATCH
        PRINT '*** ERROR OCCURRED ***';
        PRINT 'Error Number: ' + CAST(ERROR_NUMBER() AS VARCHAR);
        PRINT 'Error Message: ' + ERROR_MESSAGE();
        PRINT 'Error Line: ' + CAST(ERROR_LINE() AS VARCHAR);
        PRINT 'Error Procedure: ' + ISNULL(ERROR_PROCEDURE(), 'N/A');
        PRINT 'Error Severity: ' + CAST(ERROR_SEVERITY() AS VARCHAR);
        PRINT 'Error State: ' + CAST(ERROR_STATE() AS VARCHAR);

        -- Optional: Rethrow the error if needed
        -- THROW; -- Uncomment if you want the calling process to receive the error
    END CATCH
END;
GO

-- Clean and Validate Flight Data Procedure
-- Re-validates data in error_table and moves valid records back to main table
CREATE OR ALTER PROCEDURE usp_CleanAndValidateFlightData
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;

        ------------------------------------------------------------------------------------
        PRINT '7. Re-validating data in error_table...';
        ------------------------------------------------------------------------------------

        UPDATE et
        SET
            Is_InvalidFlightDate = CAST(CASE
                WHEN et.flightdate IS NULL THEN 1
                WHEN
                    CASE
						WHEN ISNUMERIC(et.flightdate) = 1 THEN DATEADD(DAY, CAST(et.flightdate AS INT), '1899-12-30')
						WHEN et.flightdate LIKE '__/_/____' THEN TRY_CONVERT(DATE, et.flightdate, 103)
                        WHEN et.flightdate LIKE '__/__/____' THEN TRY_CONVERT(DATE, et.flightdate, 103)
                        WHEN et.flightdate LIKE '____-__-__ %' THEN TRY_CONVERT(DATE, LEFT(et.flightdate, 10), 120)
                        WHEN et.flightdate LIKE '____/__/__' THEN TRY_CONVERT(DATE, et.flightdate, 111)
                        WHEN LEN(TRIM(et.flightdate)) = 8 AND ISNUMERIC(TRIM(et.flightdate)) = 1 THEN TRY_CONVERT(DATE, TRIM(et.flightdate), 112)
                        WHEN TRY_CONVERT(DATETIME, et.flightdate) IS NOT NULL THEN CONVERT(DATE, et.flightdate)
                        ELSE NULL
                    END IS NULL
                THEN 1 ELSE 0 END AS BIT),

            Is_InvalidPassengerCargo = CAST(CASE
                WHEN ISNULL(et.totalpax, 0) + ISNULL(et.cgo, 0) + ISNULL(et.mail, 0) <= 0 THEN 1 ELSE 0 END AS BIT),

            Is_InvalidRoute = CAST(CASE 
                WHEN NOT EXISTS (
                    SELECT 1
    FROM Airline_Route_Details ARD
    WHERE ARD.SECTOR = (
                        CASE
                            WHEN LEN(TRIM(et.route)) = 7 AND CHARINDEX('-', et.route) > 0 THEN
                                CASE
                                    WHEN LEFT(et.route, 3) < RIGHT(et.route, 3) 
                                        THEN CONCAT(LEFT(et.route, 3), RIGHT(et.route, 3))
                                    ELSE CONCAT(RIGHT(et.route, 3), LEFT(et.route, 3))
                                END
                            ELSE NULL
                        END
                    )
                ) THEN 1 ELSE 0 END AS BIT),

            Is_InvalidActypeSeat = CAST(CASE
                WHEN (ISNULL(et.cgo, 0) + ISNULL(et.mail, 0) > 0 AND ISNULL(et.totalpax, 0) = 0) THEN 0
                WHEN NOT EXISTS (
                    SELECT 1
    FROM actype_seat ATS
    WHERE LOWER(TRIM(ATS.actype)) = LOWER(TRIM(et.actype))
                ) THEN 1 ELSE 0 END AS BIT)
        FROM error_table et;

        ------------------------------------------------------------------------------------
        PRINT 'Updating error reason and total errors...';
        ------------------------------------------------------------------------------------

        UPDATE error_table
        SET
            ErrorReason = STUFF(
                COALESCE(CASE WHEN Is_InvalidFlightDate = 1 THEN N', flightdate không hợp lệ' ELSE N'' END, N'') +
                COALESCE(CASE WHEN Is_InvalidPassengerCargo = 1 THEN N', tổng số khách + hàng hóa <= 0' ELSE N'' END, N'') +
                COALESCE(CASE WHEN Is_InvalidRoute = 1 THEN N', route không tồn tại trong AIRLINE_ROUTE_DETAILS' ELSE N'' END, N'') +
                COALESCE(CASE WHEN Is_InvalidActypeSeat = 1 THEN N', actype không tồn tại trong actype_seat hoặc không phải chuyến bay chở hàng' ELSE N'' END, N''),
                1, 2, N''
            ),
            TotalErrors =
                ISNULL(Is_InvalidFlightDate, 0) +
                ISNULL(Is_InvalidPassengerCargo, 0) +
                ISNULL(Is_InvalidRoute, 0) +
                ISNULL(Is_InvalidActypeSeat, 0);

        ------------------------------------------------------------------------------------
        PRINT '8. Moving newly validated data from error_table to flight_data_chot...';
        ------------------------------------------------------------------------------------

        INSERT INTO flight_data_chot
        (
        convert_date, flightno, route, actype, totalpax, cgo, mail,
        acregno, source, sheet_name, seat, region_type, int_dom_
        )
    SELECT
        FORMAT(
                CASE
                    WHEN et.flightdate LIKE '__/__/____' THEN TRY_CONVERT(DATE, et.flightdate, 103)
                    WHEN et.flightdate LIKE '____-__-__ %' THEN TRY_CONVERT(DATE, LEFT(et.flightdate, 10), 120)
                    WHEN et.flightdate LIKE '____/__/__' THEN TRY_CONVERT(DATE, et.flightdate, 111)
                    WHEN LEN(TRIM(et.flightdate)) = 8 AND ISNUMERIC(TRIM(et.flightdate)) = 1 THEN TRY_CONVERT(DATE, TRIM(et.flightdate), 112)
                    WHEN TRY_CONVERT(DATETIME, et.flightdate) IS NOT NULL THEN CONVERT(DATE, et.flightdate)
                    ELSE NULL
                END,
            'yyyyMMdd') AS convert_date,
        et.flightno, et.route, et.actype, et.totalpax, et.cgo, et.mail,
        et.acregno, et.source, et.sheet_name, et.seat,
        10 AS region_type,
        int_dom
    FROM error_table et
    WHERE et.TotalErrors = 0;

        -- Update type_filter for newly processed records
		UPDATE flight_data_chot
		SET type_filter = CASE 
			WHEN CHARINDEX('SGN', route) > 1 AND sheet_name != 'SGN' THEN 0 
			WHEN sheet_name = 'SGN' THEN 1 
			WHEN int_dom_ = 'INT' THEN 2 
			WHEN sheet_name = LEFT(route,3) THEN 3 
			ELSE -1 
		END 
		WHERE inserted_time >= DATEADD(MINUTE, -5, GETDATE())
        AND type_filter IS NULL;

        ------------------------------------------------------------------------------------
        PRINT 'Deleting validated rows from error_table...';
        ------------------------------------------------------------------------------------

        DELETE FROM error_table WHERE TotalErrors = 0;

        ------------------------------------------------------------------------------------
        PRINT '9. Logging missing dimensions from error_table...';
        ------------------------------------------------------------------------------------

        EXEC usp_LogMissingDimensions;

        ------------------------------------------------------------------------------------
        PRINT '10. Updating import_log...';
        ------------------------------------------------------------------------------------

        UPDATE import_log
        SET clean_data = 1
        WHERE clean_data IS NULL
        AND file_name IN (
                                                                                                                                                                                                                                                  SELECT DISTINCT source
            FROM flight_data_chot
        UNION
            SELECT DISTINCT source
            FROM error_table
          );

        COMMIT TRANSACTION;
        PRINT 'Procedure completed successfully.';
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        PRINT 'Error occurred:';
        PRINT ERROR_MESSAGE();
    END CATCH
END;
GO

-- Import and Update Missing Dimensions Procedure
-- Processes temporary import tables and updates master data
CREATE OR ALTER PROCEDURE usp_ImportAndUpdateMissingDimensions
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;

    BEGIN TRY
        -- 1. Process Aircraft Types
        PRINT 'Processing Actypes...';
        INSERT INTO actype_seat
        (actype, seat)
    SELECT
        tai.Actype,
        tai.Seat
    FROM TempActypeImport tai
    WHERE NOT EXISTS ( -- Only insert if actype doesn't exist in actype_seat
            SELECT 1
        FROM actype_seat acs
        WHERE acs.actype = tai.Actype
        ) AND tai.Actype IS NOT NULL AND tai.Seat IS NOT NULL; -- Ensure valid input data

        -- Remove actypes that were added to actype_seat from Missing_Dimensions_Log
        DELETE mdl
        FROM Missing_Dimensions_Log mdl
        INNER JOIN TempActypeImport tai ON mdl.Value = tai.Actype AND mdl.Type = 'ACTYPE'
        WHERE EXISTS ( -- Only delete if actype was actually added to actype_seat
            SELECT 1
    FROM actype_seat acs
    WHERE acs.actype = tai.Actype
        );

        -- 2. Process Routes
        PRINT 'Processing Routes...';
        INSERT INTO Route
        (
        [ROUTE], [AC], [Route_ID], [FLIGHT HOUR],
        [TAXI], [BLOCK HOUR], [DISTANCE KM], [Loại], [Type], [Country]
        )
    SELECT
        tri.Route, tri.AC, tri.Route_ID, tri.[FLIGHT HOUR],
        tri.TAXI, tri.[BLOCK HOUR], tri.[DISTANCE KM], tri.[Loại], tri.[Type], tri.Country
    FROM TempRouteImport tri
    WHERE NOT EXISTS ( -- Only insert if route doesn't exist
            SELECT 1
        FROM Route r
        WHERE r.[ROUTE] = tri.Route -- Assume ROUTE is the primary/unique key
        ) AND tri.Route IS NOT NULL
        AND Country IS NOT NULL; -- Ensure valid RouteValue

        -- Remove routes that were added to Route table from Missing_Dimensions_Log
        DELETE mdl
        FROM Missing_Dimensions_Log mdl
        INNER JOIN TempRouteImport tri ON mdl.Value = tri.Route AND mdl.Type = 'ROUTE'
        WHERE EXISTS ( -- Only delete if route was actually added to Route table
            SELECT 1
    FROM Route r
    WHERE r.[ROUTE] = tri.Route
        );

        -- Clean up temporary tables
        PRINT 'Clearing temporary tables...';
        TRUNCATE TABLE TempActypeImport;
        TRUNCATE TABLE TempRouteImport;

        COMMIT TRANSACTION;
        PRINT 'Missing dimensions imported and log cleaned successfully.';

    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        PRINT 'Error occurred during import: ' + ERROR_MESSAGE();
        -- Log error if needed
        THROW; -- Throw error so Python can catch it
    END CATCH
END;
GO

-- Log Missing Dimensions Procedure
-- Identifies and logs missing aircraft types and routes from error data
CREATE OR ALTER PROCEDURE usp_LogMissingDimensions
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM Missing_Dimensions_Log;

    -- Log missing routes
    INSERT INTO Missing_Dimensions_Log
        (Type, Value, SourceSheet)
    SELECT DISTINCT
        'ROUTE',
        et.route,
        et.sheet_name
    FROM error_table et
    WHERE et.Is_InvalidRoute = 1
        AND NOT EXISTS (
          SELECT 1
        FROM Missing_Dimensions_Log L
        WHERE L.Type = 'ROUTE' AND L.Value = et.route AND L.SourceSheet = et.sheet_name -- Avoid duplicate log entries for the same route from the same sheet
      );

    -- Log missing actypes
    INSERT INTO Missing_Dimensions_Log
        (Type, Value, SourceSheet)
    SELECT DISTINCT
        'ACTYPE',
        et.actype,
        et.sheet_name
    FROM error_table et
    WHERE et.Is_InvalidActypeSeat = 1
        AND (ISNULL(et.cgo, 0) > 0 OR ISNULL(et.totalpax, 0) > 0) -- Only log if it's a passenger or cargo flight needing an actype
        AND NOT EXISTS (
          SELECT 1
        FROM Missing_Dimensions_Log L
        WHERE L.Type = 'ACTYPE' AND L.Value = et.actype AND L.SourceSheet = et.sheet_name -- Avoid duplicate log entries
      );
END;
GO

-- ===================================================================
-- TRIGGERS FOR AUTOMATIC TIMESTAMP UPDATES
-- ===================================================================

-- Update triggers for automatic timestamp management
CREATE TRIGGER trg_Airport_Information_update
ON Airport_Information
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE a
    SET updated_at = SYSDATETIME()
    FROM Airport_Information a
        INNER JOIN inserted i ON a.[index] = i.[index];
END;
GO

CREATE TRIGGER trg_Airline_Route_Details_update
ON Airline_Route_Details
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE a
    SET updated_at = SYSDATETIME()
    FROM Airline_Route_Details a
        INNER JOIN inserted i ON a.[index] = i.[index];
END;
GO

CREATE TRIGGER trg_actype_seat_update
ON actype_seat
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE a
    SET updated_at = SYSDATETIME()
    FROM actype_seat a
        INNER JOIN inserted i ON a.[index] = i.[index];
END;
GO

-- ===================================================================
-- SAMPLE DATA FOR TESTING
-- ===================================================================

-- Actype
;WITH
    cte
    AS
    (
        SELECT
            [Value],
            [CreatedAt],
            [created_at],
            [ID],
            ROW_NUMBER() OVER (PARTITION BY [Value] ORDER BY [created_at] DESC) AS rn
        FROM [flight].[dbo].[Missing_Dimensions_Log]
        WHERE [type] = 'actype'
    )
INSERT INTO [TempActypeImport]
    ([Actype], [created_at])
SELECT
    [Value],
    [created_at]
FROM cte
WHERE rn = 1;

-- Route
;WITH
    cte
    AS
    (
        SELECT
            [Value],
            [CreatedAt],
            [created_at],
            [ID],
            ROW_NUMBER() OVER (PARTITION BY [Value] ORDER BY [created_at] DESC) AS rn
        FROM [flight].[dbo].[Missing_Dimensions_Log]
        WHERE [type] = 'route'
    )
INSERT INTO [TempRouteImport]
    ([Route], [Route_ID], [created_at])
SELECT
    [Value],
    [ID],
    [created_at]
FROM cte
WHERE rn = 1;

-- ===================================================================
-- END OF AIRLINE DATABASE SCHEMA
-- Total Tables: 17
-- Total Views: 1  
-- Total Stored Procedures: 4
-- Total Triggers: 3
-- ===================================================================


-- ===================================================================
-- UPDATE TABLE
-- ===================================================================

/* ===================== Airport_Information ===================== */
IF COL_LENGTH('Airport_Information', 'created_at') IS NULL
    ALTER TABLE Airport_Information ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

IF COL_LENGTH('Airport_Information', 'updated_at') IS NULL
    ALTER TABLE Airport_Information ADD updated_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

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
    ALTER TABLE Airline_Route_Details ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

IF COL_LENGTH('Airline_Route_Details', 'updated_at') IS NULL
    ALTER TABLE Airline_Route_Details ADD updated_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

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
    ALTER TABLE Region ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

IF COL_LENGTH('Region', 'updated_at') IS NULL
    ALTER TABLE Region ADD updated_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

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
    ALTER TABLE Airline_Details ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

IF COL_LENGTH('Airline_Details', 'updated_at') IS NULL
    ALTER TABLE Airline_Details ADD updated_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

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
    ALTER TABLE [Route] ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

IF COL_LENGTH('Route', 'updated_at') IS NULL
    ALTER TABLE [Route] ADD updated_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

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
    ALTER TABLE actype_seat ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

IF COL_LENGTH('actype_seat', 'updated_at') IS NULL
    ALTER TABLE actype_seat ADD updated_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

IF COL_LENGTH('actype_seat', 'index') IS NULL
    ALTER TABLE actype_seat ADD [index] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== seat_by_AC_type ===================== */
IF COL_LENGTH('seat_by_AC_type', 'created_at') IS NULL
    ALTER TABLE seat_by_AC_type ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

IF COL_LENGTH('seat_by_AC_type', 'updated_at') IS NULL
    ALTER TABLE seat_by_AC_type ADD updated_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

DECLARE @pk1 NVARCHAR(200);
SELECT @pk1 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('seat_by_AC_type') AND type = 'PK';
IF @pk1 IS NOT NULL EXEC('ALTER TABLE seat_by_AC_type DROP CONSTRAINT ' + @pk1);

IF COL_LENGTH('seat_by_AC_type', 'id') IS NULL
    ALTER TABLE seat_by_AC_type ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== flight_raw ===================== */
IF COL_LENGTH('flight_raw', 'created_at') IS NULL
    ALTER TABLE flight_raw ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

DECLARE @pk2 NVARCHAR(200);
SELECT @pk2 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('flight_raw') AND type = 'PK';
IF @pk2 IS NOT NULL EXEC('ALTER TABLE flight_raw DROP CONSTRAINT ' + @pk2);

IF COL_LENGTH('flight_raw', 'id') IS NULL
    ALTER TABLE flight_raw ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== flight_data_chot ===================== */
IF COL_LENGTH('flight_data_chot', 'created_at') IS NULL
    ALTER TABLE flight_data_chot ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

IF COL_LENGTH('flight_data_chot', 'updated_at') IS NULL
    ALTER TABLE flight_data_chot ADD updated_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

DECLARE @pk3 NVARCHAR(200);
SELECT @pk3 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('flight_data_chot') AND type = 'PK';
IF @pk3 IS NOT NULL EXEC('ALTER TABLE flight_data_chot DROP CONSTRAINT ' + @pk3);

IF COL_LENGTH('flight_data_chot', 'id') IS NULL
    ALTER TABLE flight_data_chot ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== flight_analyze ===================== */
IF COL_LENGTH('flight_analyze', 'created_at') IS NULL
    ALTER TABLE flight_analyze ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

IF COL_LENGTH('flight_analyze', 'updated_at') IS NULL
    ALTER TABLE flight_analyze ADD updated_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

DECLARE @pk4 NVARCHAR(200);
SELECT @pk4 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('flight_analyze') AND type = 'PK';
IF @pk4 IS NOT NULL EXEC('ALTER TABLE flight_analyze DROP CONSTRAINT ' + @pk4);

IF COL_LENGTH('flight_analyze', 'id') IS NULL
    ALTER TABLE flight_analyze ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== qua_dem ===================== */
IF COL_LENGTH('qua_dem', 'created_at') IS NULL
    ALTER TABLE qua_dem ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

DECLARE @pk5 NVARCHAR(200);
SELECT @pk5 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('qua_dem') AND type = 'PK';
IF @pk5 IS NOT NULL EXEC('ALTER TABLE qua_dem DROP CONSTRAINT ' + @pk5);

IF COL_LENGTH('qua_dem', 'id') IS NULL
    ALTER TABLE qua_dem ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== error_table ===================== */
IF COL_LENGTH('error_table', 'created_at') IS NULL
    ALTER TABLE error_table ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

DECLARE @pk6 NVARCHAR(200);
SELECT @pk6 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('error_table') AND type = 'PK';
IF @pk6 IS NOT NULL EXEC('ALTER TABLE error_table DROP CONSTRAINT ' + @pk6);

IF COL_LENGTH('error_table', 'id') IS NULL
    ALTER TABLE error_table ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== flight_clean_data_stg ===================== */
IF COL_LENGTH('flight_clean_data_stg', 'created_at') IS NULL
    ALTER TABLE flight_clean_data_stg ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

DECLARE @pk7 NVARCHAR(200);
SELECT @pk7 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('flight_clean_data_stg') AND type = 'PK';
IF @pk7 IS NOT NULL EXEC('ALTER TABLE flight_clean_data_stg DROP CONSTRAINT ' + @pk7);

IF COL_LENGTH('flight_clean_data_stg', 'id') IS NULL
    ALTER TABLE flight_clean_data_stg ADD [id] BIGINT IDENTITY(1,1) PRIMARY KEY;


/* ===================== import_log ===================== */
IF COL_LENGTH('import_log', 'created_at') IS NULL
    ALTER TABLE import_log ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

IF COL_LENGTH('import_log', 'updated_at') IS NULL
    ALTER TABLE import_log ADD updated_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

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
    ALTER TABLE Missing_Dimensions_Log ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

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
    ALTER TABLE TempActypeImport ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

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
    ALTER TABLE TempRouteImport ADD created_at datetime2 DEFAULT SYSDATETIME() NOT NULL;

DECLARE @pk11 NVARCHAR(200);
SELECT @pk11 = name
FROM sys.key_constraints
WHERE parent_object_id = OBJECT_ID('TempRouteImport') AND type = 'PK';
IF @pk11 IS NOT NULL EXEC('ALTER TABLE TempRouteImport DROP CONSTRAINT ' + @pk11);

IF COL_LENGTH('TempRouteImport', 'Route') IS NOT NULL
    ALTER TABLE TempRouteImport DROP COLUMN [Route];

IF COL_LENGTH('TempRouteImport', 'Route') IS NULL
    ALTER TABLE TempRouteImport ADD [Route] NVARCHAR(255) PRIMARY KEY;
