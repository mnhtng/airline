-- Add new tables
CREATE TABLE Countries
(
    id INT IDENTITY (1,1) PRIMARY KEY,
    [Country] NVARCHAR (100) NOT NULL,
    [Region] NVARCHAR (100),
    [Region VNM] NVARCHAR (100),
    [2 Letter Code] CHAR(2) NOT NULL,
    [3 Letter Code] CHAR(3) NOT NULL,
    created_at DATETIME2 (3) DEFAULT SYSUTCDATETIME (),
    updated_at DATETIME2 (3) DEFAULT SYSUTCDATETIME ()
);

INSERT INTO Countries
    ([Country], [Region], [Region VNM], [2 Letter Code], [3 Letter Code], created_at, updated_at)
VALUES
    ('Afghanistan', 'South-Central Asia', N'Nam Á', 'AF', 'AFG', '2025-10-08 23:38:11.000', '2025-10-08 23:38:11.000'),
    ('Albania', 'Balkan Peninsula', N'Châu Âu', 'AL', 'ALB', '2025-10-08 23:38:11.000', '2025-10-08 23:38:11.000'),
    ('Algeria', 'Northern Africa', N'Châu Phi', 'DZ', 'DZA', '2025-10-08 23:38:11.000', '2025-10-08 23:38:11.000'),
    ('American Samoa', 'Polynesia, Oceania', N'Châu Đại Dương', 'AS', 'ASM', '2025-10-08 23:38:11.000', '2025-10-08 23:38:11.000'),
    ('Andorra', 'Southern Europe', N'Châu Âu', 'AD', 'AND', '2025-10-08 23:38:11.000', '2025-10-08 23:38:11.000'),
    ('Angola', 'Central Africa', N'Châu Phi', 'AO', 'AGO', '2025-10-08 23:38:11.000', '2025-10-08 23:38:11.000'),
    ('Anguilla', 'Leeward Islands, Caribbean', N'Caribe', 'AI', 'AIA', '2025-10-08 23:38:11.000', '2025-10-08 23:38:11.000'),
    ('Antarctica', 'Antarctica', NULL, 'AQ', 'ATA', '2025-10-08 23:38:11.000', '2025-10-08 23:38:11.000'),
    ('Antigua and Barbuda', 'Leeward Islands, Caribbean', N'Caribe', 'AG', 'ATG', '2025-10-08 23:38:11.000', '2025-10-08 23:38:11.000'),
    ('Argentina', 'Southern South America', N'Nam Mỹ', 'AR', 'ARG', '2025-10-08 23:38:11.000', '2025-10-08 23:38:11.000');


CREATE TABLE Airlines
(
    id INT IDENTITY(1,1) PRIMARY KEY,
    [Carrier] NVARCHAR(10) NOT NULL,
    [Airline Nation] NVARCHAR(100) NOT NULL,
    [Airlines Name] NVARCHAR(150) NOT NULL,
    created_at DATETIME2(3) DEFAULT SYSDATETIME(),
    updated_at DATETIME2(3) DEFAULT SYSDATETIME()
);

INSERT INTO Airlines
    ([Carrier], [Airline Nation], [Airlines Name], created_at, updated_at)
VALUES
    ('SF', 'Algeria', 'Tassili Airlines', '2025-10-08 23:36:08', '2025-10-08 23:36:08'),
    ('DT', 'Angola', 'TAAG Angola Airlines', '2025-10-08 23:36:08', '2025-10-08 23:36:08'),
    ('3K', 'Australia', 'Jetstar Asia Airways', '2025-10-08 23:36:08', '2025-10-08 23:36:08'),
    ('JQ', 'Australia', 'Jetstar Airways', '2025-10-08 23:36:08', '2025-10-08 23:36:08'),
    ('QF', 'Australia', 'Qantas', '2025-10-08 23:36:08', '2025-10-08 23:36:08'),
    ('VA', 'Australia', 'Virgin Australia', '2025-10-08 23:36:08', '2025-10-08 23:36:08'),
    ('OS', 'Austria', 'Austrian Airlines', '2025-10-08 23:36:08', '2025-10-08 23:36:08'),
    ('J2', 'Azerbaijan', 'Azerbaijan Airlines', '2025-10-08 23:36:08', '2025-10-08 23:36:08'),
    ('UP', 'Bahamas', 'Bahamasair', '2025-10-08 23:36:08', '2025-10-08 23:36:08'),
    ('GF', 'Bahrain', 'Gulf Air', '2025-10-08 23:36:08', '2025-10-08 23:36:08');


CREATE TABLE Airports
(
    id INT IDENTITY(1,1) PRIMARY KEY,
    [IATACode] NVARCHAR(10) NOT NULL,
    [Airport Name] NVARCHAR(200) NOT NULL,
    [City] NVARCHAR(100) NOT NULL,
    [Country] NVARCHAR(100) NOT NULL,
    created_at DATETIME2(3) DEFAULT SYSDATETIME(),
    updated_at DATETIME2(3) DEFAULT SYSDATETIME()
);

INSERT INTO Airports
    ([IATACode], [Airport Name], [City], [Country], created_at, updated_at)
VALUES
    ('VPS', 'Destin–Fort Walton Beach Airport', 'Valparaiso', 'United States', '2025-10-09 06:22:38', '2025-10-09 06:22:38'),
    ('DLF', 'Laughlin Afb', 'Del Rio', 'United States', '2025-10-09 06:22:38', '2025-10-09 06:22:38'),
    ('MGE', 'Dobbins Air Reserve Base', 'Marietta', 'United States', '2025-10-09 06:22:38', '2025-10-09 06:22:38'),
    ('DOV', 'Sde Dov Airport', 'Tel Aviv', 'United States', '2025-10-09 06:22:38', '2025-10-09 06:22:38'),
    ('DBQ', 'Dubuque Regional Airport', 'Dubuque', 'United States', '2025-10-09 06:22:38', '2025-10-09 06:22:38'),
    ('DLH', 'Duluth International Airport', 'Duluth', 'United States', '2025-10-09 06:22:38', '2025-10-09 06:22:38'),
    ('DYS', 'DYESS AFB Airport', 'Abilene', 'United States', '2025-10-09 06:22:38', '2025-10-09 06:22:38'),
    ('EDW', 'Edwards Air Force Base', 'California', 'United States', '2025-10-09 06:22:38', '2025-10-09 06:22:38'),
    ('ERI', 'Erie International Airport Tom Ridge Field', 'Erie', 'United States', '2025-10-09 06:22:38', '2025-10-09 06:22:38'),
    ('SKA', 'Fairchild Air Force Base', 'Washington', 'United States', '2025-10-09 06:22:38', '2025-10-09 06:22:38');


CREATE TABLE Sectors
(
    id INT IDENTITY(1,1) PRIMARY KEY,
    [Sector] NVARCHAR(20) NOT NULL,
    [Area lv1] NVARCHAR(100) NOT NULL,
    [DOM/INT] NVARCHAR(10) NOT NULL,
    created_at DATETIME2(3) DEFAULT SYSDATETIME(),
    updated_at DATETIME2(3) DEFAULT SYSDATETIME()
);

INSERT INTO Sectors
    ([Sector], [Area lv1], [DOM/INT], created_at, updated_at)
VALUES
    ('BMV-PQC', N'Du lịch', 'DOM', '2025-10-09 06:27:42', '2025-10-09 06:27:42'),
    ('PQC-BMV', N'Du lịch', 'DOM', '2025-10-09 06:27:42', '2025-10-09 06:27:42'),
    ('PQC-CXR', N'Du lịch', 'DOM', '2025-10-09 06:27:42', '2025-10-09 06:27:42'),
    ('CXR-PQC', N'Du lịch', 'DOM', '2025-10-09 06:27:42', '2025-10-09 06:27:42'),
    ('VCA-CXR', N'Địa phương_2', 'DOM', '2025-10-09 06:27:42', '2025-10-09 06:27:42'),
    ('CXR-VCA', N'Địa phương_2', 'DOM', '2025-10-09 06:27:42', '2025-10-09 06:27:42'),
    ('DAD-BMV', N'Địa phương_2', 'DOM', '2025-10-09 06:27:42', '2025-10-09 06:27:42'),
    ('BMV-DAD', N'Địa phương_2', 'DOM', '2025-10-09 06:27:42', '2025-10-09 06:27:42'),
    ('DAD-CXR', N'Địa phương_2', 'DOM', '2025-10-09 06:27:42', '2025-10-09 06:27:42'),
    ('CXR-DAD', N'Địa phương_2', 'DOM', '2025-10-09 06:27:42', '2025-10-09 06:27:42');
