'''
The functions in this script are used to fill data in the census data warehouse.

These functions are used to fill dbo.DIM_NAICS_2012
'''

__author__ = "Jarred Glaser"
__last_updated__ = "2019-11-08"

import requests
import pandas as pd
from sqlalchemy import create_engine

def interpolate(row):
    nums = row["2012 NAICS Code"].split("-")
    return ','.join([str(x) for x in list(range(int(nums[0]),int(nums[1])+1))])

def generate_naics_2012():
    # Read in File
    df = pd.read_excel("../data-files/2012_NAICS.xlsx")
    df["NAICS Len"] = df["2012 NAICS Code"].astype(str).str.len()
    # Format the dashed NAICS 2 Digit Codes
    df.loc[df["2012 NAICS Code"].astype(str).str.contains("-"),"2012 NAICS Code"] = df[df["2012 NAICS Code"].astype(str).str.contains("-")].apply(interpolate,axis=1)
    new_df = pd.DataFrame(df["2012 NAICS Code"].astype(str).str.split(',').tolist(), index=df["2012 NAICS US Title"]).stack()
    new_df = new_df.reset_index()
    new_df = new_df.iloc[:,[2,0]]
    new_df.columns = ["NAICS_Code","NAICS_Description"]
    new_df["NAICS_Code"] = new_df["NAICS_Code"].astype(str)
    # Join to create main DF
    six = new_df.loc[new_df["NAICS_Code"].str.len()==6,:]
    six.columns = ["National_Industry_Code","National_Industry_Description"]
    six["Industry_Code"] = six["National_Industry_Code"].str[0:5]
    six["Industry_Group_Code"] = six["National_Industry_Code"].str[0:4]
    six["Subsector_Code"] = six["National_Industry_Code"].str[0:3]
    six["Economic_Sector_Code"] = six["National_Industry_Code"].str[0:2]
    # Merge
    six = six.merge(new_df,how="inner",left_on="Economic_Sector_Code",right_on="NAICS_Code").rename({"NAICS_Description":"Economic_Sector_Description"},axis=1)
    six = six.merge(new_df,how="inner",left_on="Subsector_Code",right_on="NAICS_Code").rename({"NAICS_Description":"Subsector_Description"},axis=1)
    six = six.merge(new_df,how="inner",left_on="Industry_Group_Code",right_on="NAICS_Code").rename({"NAICS_Description":"Industry_Group_Description"},axis=1)
    six = six.merge(new_df,how="inner",left_on="Industry_Code",right_on="NAICS_Code").rename({"NAICS_Description":"Industry_Description"},axis=1)
    six = six[['National_Industry_Code','National_Industry_Description','Industry_Code','Industry_Description','Industry_Group_Code','Industry_Group_Description',
    'Subsector_Code','Subsector_Description','Economic_Sector_Code','Economic_Sector_Description']]
    return six

def load_naics_2012(engine):
    naics_2012 = generate_naics_2012()
    naics_2012.to_sql("DIM_NAICS_2012",engine,if_exists="append",index=False)

if __name__ == "__main__":
    engine = create_engine("INSERT CONNECTION STRING",fast_executemany=True)
    load_naics_2012(engine)
    print("Done")