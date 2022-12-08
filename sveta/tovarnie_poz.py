import requests
import pandas as pd
from pandas import ExcelWriter
from numba import jit
import json
import time

start_time = time.time()

pyt = 'A:/sveta'
name = 'sku.xlsx'
data_in = '2022-06-01'
data_out = '2022-06-19'

df_sku = xl = pd.read_excel(f"{pyt}/{name}")
sku_list = df_sku[df_sku.columns[0]].values.tolist()
sku_list_unique = list(set(sku_list))

url = "https://mpstats.io/api/wb/get/items/batch"


headers = {
    'X-Mpstats-TOKEN': '62823e9e07c5a9.79473655475660ac88bac1123b10c5693db44735',
    'content-type': "application/json"
}
data_row = '{"ids": [85448528]}'
response = requests.request("POST", url, headers=headers, data=data_row)

df = pd.read_json(response.text)
json_str = df.item[0]
df_all = pd.json_normalize(json_str)
#df_normalize = pd.json_normalize(json.loads(df.to_json(orient='item')))
#df_normalize = pd.json_normalize(response.text, record_path =['students'])
data = json.dumps(json_str) # dict to string
#data = json.loads(data)

print(json_str)
print(df_all)
print(type(data))







df_all_2 = df_all['sizeandstores'][0]
#df_all_3 = pd.json_normalize(df_all_2)
print(type(df_all_2))
df_all_3 = json.loads(df_all_2)
df_all_3 = pd.json_normalize(df_all_3)
#df_all_3['id'] = 23162292

df_all_final = pd.DataFrame()
df_all_final = pd.concat([df_all, df_all_3], axis=1)
df_all_final = df_all_final.drop('sizeandstores', axis=1)
print(df_all_final)

writer = ExcelWriter(f'{pyt}/tovarnie_ostatki_sku.xlsx')
df_all_final.to_excel(writer, 'основное', index = False )
#df_errors.to_excel(writer, 'error_sku', index = False )
writer.save()
print("--- %s seconds ---" % (time.time() - start_time))

#df_normalize = pd.json_normalize(json.loads(df_all_2.to_json()))
#df_normalize = pd.json_normalize(df_all, record_path =['sizeandstores'])
#print(df_normalize)



