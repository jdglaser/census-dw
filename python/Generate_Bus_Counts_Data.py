'''
The functions in this script are used to fill data in the census data warehouse.

These functions are used to fill dbo.FACT_Bus_Counts
'''

__author__ = "Jarred Glaser"
__last_updated__ = "2019-11-08"

import requests
import pandas as pd
from sqlalchemy import create_engine

def get_bus_counts(county_fips,state_fips):
    url_zips = "https://api.census.gov/data/2016/cbp?"

    params = {
        "get":"GEO_TTL,NAICS2012,NAICS2012_TTL,EMPSZES,ESTAB",
        "for":"county:" + str(county_fips),
        "in":"state:" + str(state_fips),
        "key":"INSERT API KEY"
    }
    req = requests.get(url_zips,params=params)
    try:
        results = req.json()
    except:
        print(req.text)
        return pd.DataFrame()
    df = pd.DataFrame(results[1:],columns=results[0])
    df = df[(df["NAICS2012"] != "00") & (df["EMPSZES"] != "001")]
    df = df[(df["NAICS2012"].str.len() == 2) | (df["NAICS2012"].str.contains("-"))]
    return df

def loop_bus_data():
    df = pd.read_csv("../data-files/county_loop.csv")
    df["County_Fips_Code"] = df["County_Fips_Code"].astype(str).str.zfill(3)
    df["State_Fips_Code"] = df["State_Fips_Code"].astype(str).str.zfill(2)
    # Get final DF
    final_df = pd.DataFrame()
    for i,r in df.iterrows():
        print(i)
        df1 = get_bus_counts(r["County_Fips_Code"],r["State_Fips_Code"])
        if df1.empty:
            print("Error on {}!".format(i))
            continue
        final_df = pd.concat([final_df,df1],axis=0)
        if i % 500 == 0:
            final_df.to_csv("bus_stats_backup_{}.csv".format(str(i).zfill(3)))
            print(final_df)
    final_df.to_csv("../data-files/bus_stats_final.csv",index=False)

def load_bus_counts(engine):
    df = pd.read_csv("../data-files/bus_stats_final.csv")
    df["state"] = df["state"].astype(str).str.zfill(2)
    df["county"] = df["county"].astype(str).str.zfill(3)
    df["Full_County_Fips_Code"] = df["state"] + df["county"]
    df = df[["Full_County_Fips_Code","NAICS2012","EMPSZES","ESTAB"]]
    df.columns = ["Full_County_Fips_Code","Economic_Sector_Code","CBP_Employee_Size_Code","Businesses"]
    df["CBP_Employee_Size_Code"] = df["CBP_Employee_Size_Code"].astype(str)
    # This next part is cheeky and not the best data practice, I'm too lazy to fix it though, and the end results are the same.
    df["Economic_Sector_Code"] = df["Economic_Sector_Code"].replace("31-33","31")
    df["Economic_Sector_Code"] = df["Economic_Sector_Code"].replace("44-45","44")
    df["Economic_Sector_Code"] = df["Economic_Sector_Code"].replace("48-49","48")
    df["Economic_Sector_Code"] = df["Economic_Sector_Code"].astype(int)
    # Load final data
    df.to_sql("FACT_Bus_Counts",engine,if_exists="append",index=False,chunksize=10000)

if __name__ == "__main__":
    engine = create_engine("INSERT CONNECTION STRING",fast_executemany=True)
    load_bus_counts(engine)
    print("Done")