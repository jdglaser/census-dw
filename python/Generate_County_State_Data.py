'''
The functions in this script are used to fill data in the census data warehouse.

These functions are used to fill dbo.DIM_County_State_Fips_2016
'''

__author__ = "Jarred Glaser"
__last_updated__ = "2019-11-08"

import requests
import pandas as pd
from sqlalchemy import create_engine

def generate_county_state():
    df_county = pd.read_excel("../data-files/all-geocodes-v2016.xlsx")
    df1 = df_county[df_county["Summary Level"] == 50].iloc[:,[1,2,6]].rename({"Area Name":"County"},axis=1)
    df2 = df_county[df_county["Summary Level"] == 40].iloc[:,[1,6]].rename({"Area Name":"State"},axis=1)
    county_state = df1.merge(df2,on="State Code")
    county_state["State Code"] = county_state["State Code"].astype(str).str.zfill(2)
    county_state["County Code"] = county_state["County Code"].astype(str).str.zfill(3)
    return county_state

def load_county_state(engine):
    county_state = generate_county_state()
    county_state["Full_County_Fips_Code"] = county_state["State Code"] + county_state["County Code"]
    county_state.columns = ["State_Fips_Code","County_Fips_Code","County","State","Full_County_Fips_Code"]
    county_state = county_state[["Full_County_Fips_Code","County_Fips_Code","County","State_Fips_Code","State"]]
    county_state.to_sql("DIM_County_State_Fips_2016",engine,if_exists="append",index=False)

if __name__ == "__main__":
    engine = create_engine("INSERT CONNECTION STRING",fast_executemany=True)
    load_county_state(engine)
    print("Done")