-- Create View for County Business Stats --
CREATE VIEW County_Business_Counts AS
SELECT cs.County,
	cs.State,
	nes.Economic_Sector_Description AS Economic_Sector,
	es.Short_Description AS Employees,
	bc.[Businesses]
FROM [Gov_Business_Stats_DW].[dbo].[FACT_Bus_Counts] bc
JOIN DIM_County_State_Fips_2016 cs
ON cs.Full_County_Fips_Code = bc.Full_County_Fips_Code
JOIN DIM_CBP_Employee_Sizes es
ON es.CBP_Employee_Size_Code = bc.CBP_Employee_Size_Code
JOIN DIM_NAICS_2012_Economic_Sector nes
ON nes.Economic_Sector_Code = bc.Economic_Sector_Code