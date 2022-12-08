import requests as r
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



def zapros(sku,data_in, data_out):
    #url = f'https://mpstats.io/api/wb/get/item/{sku}/sales?d1={data_in}&d2={data_out}'
    url = f'https://mpstats.io/api/wb/get/item/{sku}/orders_by_size?d1={data_in}&d2={data_out}'

    headers = {'X-Mpstats-TOKEN': '62823e9e07c5a9.79473655475660ac88bac1123b10c5693db44735','content-type': 'application/json'}

    data = r.request('get', url, headers=headers)
    df = pd.read_json(data.text).T

    df.columns = df.columns.str.replace(" ", "_")
    df_normalize = pd.json_normalize(json.loads(df.to_json(orient='records')))
    df_normalize.insert(0, "sku", sku)

    dates =  pd.date_range(data_in,data_out).strftime('%Y-%m-%d').tolist()
    df_normalize.insert(0, "data", dates)
    return df_normalize



def join_tables(df_all, sku):
    if df_all.empty:
        df_new = zapros(sku, data_in, data_out)
    else:
        df_new = pd.concat([df_all,zapros(sku, data_in, data_out)])
    return df_new




df_all = pd.DataFrame()
errors_list = []

for sku in sku_list_unique:
    try:
        df_all = join_tables(df_all, sku)
    except:
        errors_list.append(sku)

df_errors = pd.DataFrame(data = errors_list, columns={'errors'})

writer = ExcelWriter(f'{pyt}/info_po_sku_ostatki.xlsx')
df_all.to_excel(writer, 'основное', index = False )
df_errors.to_excel(writer, 'error_sku', index = False )
writer.save()



print(errors_list)
print("--- %s seconds ---" % (time.time() - start_time))