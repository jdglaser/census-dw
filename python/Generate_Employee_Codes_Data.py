'''
The functions in this script are used to fill data in the census data warehouse.

These functions are used to fill dbo.DIM_CBP_Employee_Sizes
'''

__author__ = "Jarred Glaser"
__last_updated__ = "2019-11-08"

import pandas as pd 
from sqlalchemy import create_engine

values = {
      "001": "All establishments",
      "204": "Establishments with no paid employees",
      "205": "Establishments with paid employees",
      "207": "Establishments with less than 10 employees",
      "209": "Establishments with less than 20 employees",
      "210": "Establishments with less than 5 employees",
      "211": "Establishments with less than 4 employees",
      "212": "Establishments with 1 to 4 employees",
      "213": "Establishments with 1 employee",
      "214": "Establishments with 2 employees",
      "215": "Establishments with 3 or 4 employees",
      "219": "Establishments with 0 to 4 employees",
      "220": "Establishments with 5 to 9 employees",
      "221": "Establishments with 5 or 6 employees",
      "222": "Establishments with 7 to 9 employees",
      "223": "Establishments with 10 to 14 employees",
      "230": "Establishments with 10 to 19 employees",
      "231": "Establishments with 10 to 14 employees",
      "232": "Establishments with 15 to 19 employees",
      "235": "Establishments with 20 or more employees",
      "240": "Establishments with 20 to 99 employees",
      "241": "Establishments with 20 to 49 employees",
      "242": "Establishments with 50 to 99 employees",
      "243": "Establishments with 50 employees or more",
      "249": "Establishments with 100 to 499 employees",
      "250": "Establishments with 100 or more employees",
      "251": "Establishments with 100 to 249 employees",
      "252": "Establishments with 250 to 499 employees",
      "253": "Establishments with 500 employees or more",
      "254": "Establishments with 500 to 999 employees",
      "260": "Establishments with 1,000 employees or more",
      "261": "Establishments with 1,000 to 2,499 employees",
      "262": "Establishments with 1,000 to 1,499 employees",
      "263": "Establishments with 1,500 to 2,499 employees",
      "270": "Establishments with 2,500 employees or more",
      "271": "Establishments with 2,500 to 4,999 employees",
      "272": "Establishments with 5,000 to 9,999 employees",
      "273": "Establishments with 5,000 employees or more",
      "280": "Establishments with 10,000 employees or more",
      "281": "Establishments with 10,000 to 24,999 employees",
      "282": "Establishments with 25,000 to 49,999 employees",
      "283": "Establishments with 50,000 to 99,999 employees",
      "290": "Establishments with 100,000 employees or more",
      "298": "Covered by administrative records"
}

def load_employee_codes(engine):
      df = pd.DataFrame({"CBP_Employee_Size_Code":list(values.keys()),"Long_Description":list(values.values())})
      df["Short_Description"] = df["Long_Description"].str.replace("Establishments with ","").str.replace(" to ","-").str.title()
      df.to_sql("DIM_CBP_Employee_Sizes",engine,if_exists="append",index=False)

if __name__ == "__main__":
    engine = create_engine('INSERT CONNECTION STRING',fast_executemany=True)
    print("Done")
