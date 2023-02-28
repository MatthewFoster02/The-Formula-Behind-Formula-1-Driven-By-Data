import pandas as pd
from api.load import GetAPIData

getData = GetAPIData()
df = getData.get_driver_details()
print(df)