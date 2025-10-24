-- Drop old tables
DROP TABLE IF EXISTS Country_Ref;
DROP TABLE IF EXISTS Dim_Country_Ref;
DROP TABLE IF EXISTS Airline_Ref;
DROP TABLE IF EXISTS Dim_Airline_Ref;
DROP TABLE IF EXISTS Airport_Ref;
DROP TABLE IF EXISTS Dim_Airport_Ref;
DROP TABLE IF EXISTS Sector_Route_DOM_Ref;
DROP TABLE IF EXISTS Dim_Sector_Route_DOM_Ref;

-- Add new tables
CREATE TABLE Country_Ref
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    [Country] NVARCHAR(100) NOT NULL,
    [Region] NVARCHAR(100) NOT NULL,
    [Region_(VNM)] NVARCHAR(100),
    [2_Letter_Code] CHAR(2) NOT NULL,
    [3_Letter_Code] CHAR(3) NOT NULL,
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);
GO

CREATE TABLE Dim_Country_Ref
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    [Country] NVARCHAR(100),
    [Region] NVARCHAR(100),
    [Region_(VNM)] NVARCHAR(100),
    [2_Letter_Code] CHAR(2),
    [3_Letter_Code] CHAR(3),
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);
GO

INSERT INTO Country_Ref
    ([Country], [Region], [Region_(VNM)], [2_Letter_Code], [3_Letter_Code], created_at, updated_at)
VALUES
    ('Afghanistan', 'South-Central Asia', N'Nam Á', 'AF', 'AFG', SYSDATETIME(), SYSDATETIME()),
    ('Albania', 'Balkan Peninsula', N'Châu Âu', 'AL', 'ALB', SYSDATETIME(), SYSDATETIME()),
    ('Algeria', 'Northern Africa', N'Châu Phi', 'DZ', 'DZA', SYSDATETIME(), SYSDATETIME()),
    ('American Samoa', 'Polynesia, Oceania', N'Châu Đại Dương', 'AS', 'ASM', SYSDATETIME(), SYSDATETIME()),
    ('Andorra', 'Southern Europe', N'Châu Âu', 'AD', 'AND', SYSDATETIME(), SYSDATETIME()),
    ('Angola', 'Central Africa', N'Châu Phi', 'AO', 'AGO', SYSDATETIME(), SYSDATETIME()),
    ('Anguilla', 'Leeward Islands, Caribbean', N'Caribe', 'AI', 'AIA', SYSDATETIME(), SYSDATETIME()),
    ('Antarctica', 'Antarctica', NULL, 'AQ', 'ATA', SYSDATETIME(), SYSDATETIME()),
    ('Antigua and Barbuda', 'Leeward Islands, Caribbean', N'Caribe', 'AG', 'ATG', SYSDATETIME(), SYSDATETIME()),
    ('Argentina', 'Southern South America', N'Nam Mỹ', 'AR', 'ARG', SYSDATETIME(), SYSDATETIME());
GO


CREATE TABLE Airline_Ref
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    [CARRIER] NVARCHAR(10) NOT NULL,
    [Airline_Nation] NVARCHAR(100) NOT NULL,
    [Airlines_Name] NVARCHAR(150) NOT NULL,
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);
GO

CREATE TABLE Dim_Airline_Ref
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    [CARRIER] NVARCHAR(10),
    [Airline_Nation] NVARCHAR(100),
    [Airlines_Name] NVARCHAR(150),
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);
GO

INSERT INTO Airline_Ref
    ([CARRIER], [Airline_Nation], [Airlines_Name], created_at, updated_at)
VALUES
    ('SF', 'Algeria', 'Tassili Airlines', SYSDATETIME(), SYSDATETIME()),
    ('DT', 'Angola', 'TAAG Angola Airlines', SYSDATETIME(), SYSDATETIME()),
    ('3K', 'Australia', 'Jetstar Asia Airways', SYSDATETIME(), SYSDATETIME()),
    ('JQ', 'Australia', 'Jetstar Airways', SYSDATETIME(), SYSDATETIME()),
    ('QF', 'Australia', 'Qantas', SYSDATETIME(), SYSDATETIME()),
    ('VA', 'Australia', 'Virgin Australia', SYSDATETIME(), SYSDATETIME()),
    ('OS', 'Austria', 'Austrian Airlines', SYSDATETIME(), SYSDATETIME()),
    ('J2', 'Azerbaijan', 'Azerbaijan Airlines', SYSDATETIME(), SYSDATETIME()),
    ('UP', 'Bahamas', 'Bahamasair', SYSDATETIME(), SYSDATETIME()),
    ('GF', 'Bahrain', 'Gulf Air', SYSDATETIME(), SYSDATETIME());
GO


CREATE TABLE Airport_Ref
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    [IATACode] NVARCHAR(10) NOT NULL,
    [Airport_Name] NVARCHAR(200) NOT NULL,
    [City] NVARCHAR(100) NOT NULL,
    [Country] NVARCHAR(100) NOT NULL,
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);
GO

CREATE TABLE Dim_Airport_Ref
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    [IATACode] NVARCHAR(10),
    [Airport_Name] NVARCHAR(200),
    [City] NVARCHAR(100),
    [Country] NVARCHAR(100),
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);
GO

INSERT INTO Airport_Ref
    ([IATACode], [Airport_Name], [City], [Country], created_at, updated_at)
VALUES
    ('VPS', 'Destin–Fort Walton Beach Airport', 'Valparaiso', 'United States', SYSDATETIME(), SYSDATETIME()),
    ('DLF', 'Laughlin Afb', 'Del Rio', 'United States', SYSDATETIME(), SYSDATETIME()),
    ('MGE', 'Dobbins Air Reserve Base', 'Marietta', 'United States', SYSDATETIME(), SYSDATETIME()),
    ('DOV', 'Sde Dov Airport', 'Tel Aviv', 'United States', SYSDATETIME(), SYSDATETIME()),
    ('DBQ', 'Dubuque Regional Airport', 'Dubuque', 'United States', SYSDATETIME(), SYSDATETIME()),
    ('DLH', 'Duluth International Airport', 'Duluth', 'United States', SYSDATETIME(), SYSDATETIME()),
    ('DYS', 'DYESS AFB Airport', 'Abilene', 'United States', SYSDATETIME(), SYSDATETIME()),
    ('EDW', 'Edwards Air Force Base', 'California', 'United States', SYSDATETIME(), SYSDATETIME()),
    ('ERI', 'Erie International Airport Tom Ridge Field', 'Erie', 'United States', SYSDATETIME(), SYSDATETIME()),
    ('SKA', 'Fairchild Air Force Base', 'Washington', 'United States', SYSDATETIME(), SYSDATETIME());
GO


CREATE TABLE Sector_Route_DOM_Ref
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    [Sector] NVARCHAR(20) NOT NULL,
    [Area_Lv1] NVARCHAR(100) NOT NULL,
    [DOM/INT] NVARCHAR(10) NOT NULL,
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);
GO

CREATE TABLE Dim_Sector_Route_DOM_Ref
(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    [Sector] NVARCHAR(20),
    [Area_Lv1] NVARCHAR(100),
    [DOM/INT] NVARCHAR(10),
    created_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL,
    updated_at DATETIME2 DEFAULT SYSDATETIME() NOT NULL
);
GO

INSERT INTO Sector_Route_DOM_Ref
    ([Sector], [Area_Lv1], [DOM/INT], created_at, updated_at)
VALUES
    ('BMV-PQC', N'Du lịch', 'DOM', SYSDATETIME(), SYSDATETIME()),
    ('PQC-BMV', N'Du lịch', 'DOM', SYSDATETIME(), SYSDATETIME()),
    ('PQC-CXR', N'Du lịch', 'DOM', SYSDATETIME(), SYSDATETIME()),
    ('CXR-PQC', N'Du lịch', 'DOM', SYSDATETIME(), SYSDATETIME()),
    ('VCA-CXR', N'Địa phương_2', 'DOM', SYSDATETIME(), SYSDATETIME()),
    ('CXR-VCA', N'Địa phương_2', 'DOM', SYSDATETIME(), SYSDATETIME()),
    ('DAD-BMV', N'Địa phương_2', 'DOM', SYSDATETIME(), SYSDATETIME()),
    ('BMV-DAD', N'Địa phương_2', 'DOM', SYSDATETIME(), SYSDATETIME()),
    ('DAD-CXR', N'Địa phương_2', 'DOM', SYSDATETIME(), SYSDATETIME()),
    ('CXR-DAD', N'Địa phương_2', 'DOM', SYSDATETIME(), SYSDATETIME());
GO
