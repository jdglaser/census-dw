-- DIM_NAICS_2012 --
CREATE TABLE [Gov_Business_Stats_DW].[dbo].[DIM_NAICS_2012] (
	[National_Industry_Code]		INT				PRIMARY KEY,
    [National_Industry_Description]	VARCHAR(255)	NOT NULL,
    [Industry_Code]					INT				NOT NULL,
    [Industry_Description]			VARCHAR(255)	NOT NULL,
    [Industry_Group_Code]			INT				NOT NULL,
    [Industry_Group_Description]	VARCHAR(255)	NOT NULL,
    [Subsector_Code]				INT				NOT NULL,
    [Subsector_Description]			VARCHAR(255)	NOT NULL,
    [Economic_Sector_Code]			INT				NOT NULL,
    [Economic_Sector_Description]	VARCHAR(255)	NOT NULL
);

-- DIM_NAICS_2012_Economic_Sector --
CREATE TABLE [Gov_Business_Stats_DW].[dbo].[DIM_NAICS_2012_Economic_Sector] (
    [Economic_Sector_Code]			INT				PRIMARY KEY,
    [Economic_Sector_Description]	VARCHAR(255)	NOT NULL
);

-- DIM_County_State_Fips_2016 --
CREATE TABLE [Gov_Business_Stats_DW].[dbo].[DIM_County_State_Fips_2016] (
	[Full_County_Fips_Code]	VARCHAR(5)		PRIMARY KEY,
	[County_Fips_Code]		VARCHAR(3)		NOT NULL,
	[County]				VARCHAR(150)	NOT NULL,
	[State_Fips_Code]		VARCHAR(2)		NOT NULL,
	[State]					VARCHAR(100)	NOT NULL
);

-- DIM_CBP_Employee_Sizes --
CREATE TABLE dbo.DIM_CBP_Employee_Sizes (
	CBP_Employee_Size_Code	VARCHAR(5)		PRIMARY KEY,
	Long_Description		VARCHAR(300)	NOT NULL,
	Short_Description		VARCHAR(200)	NOT NULL
);

-- FACT_Bus_Counts --
CREATE TABLE dbo.FACT_Bus_Counts (
	Full_County_Fips_Code	VARCHAR(5)	FOREIGN KEY REFERENCES dbo.DIM_County_State_Fips_2016(Full_County_Fips_Code),
	Economic_Sector_Code	INT			FOREIGN KEY REFERENCES dbo.DIM_NAICS_2012_Economic_Sector(Economic_Sector_Code),
	CBP_Employee_Size_Code	VARCHAR(5)	FOREIGN KEY REFERENCES dbo.DIM_CBP_Employee_Sizes(CBP_Employee_Size_Code),
	Businesses				INT
	PRIMARY KEY (Full_County_Fips_Code,Economic_Sector_Code,CBP_Employee_Size_Code)
);
