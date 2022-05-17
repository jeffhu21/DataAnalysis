import json
import webbrowser
from datetime import datetime

import DataSource as ds
import pandas as pd

dataList = ds.get_data()
filename = "output" + datetime.today().strftime('%Y%m%d')

res = pd.DataFrame((dataList))
#print(res)
#new_res = res.dropna()
new_res = res.filter(items=['id','style','title','country','community','label','year','genre'])
new_csv = new_res.to_csv(filename+".csv")




