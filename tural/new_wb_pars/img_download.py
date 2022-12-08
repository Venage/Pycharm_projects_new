import requests
"""
img_data = requests.get('https://images.wbstatic.net/big/new/13610000/13615125-1.jpg').content
with open('image_name.jpg', 'wb') as handler:
    handler.write(img_data)
"""
import pandas as pd

global filename, image_path
filename = r'C:\PyProjects\poject_1\tural\new_wb_pars\wildberries_data.xlsx'
image_path = r'C:\PyProjects\poject_1\tural\new_wb_pars\images\phone'

def download_img():
    df_img = pd.read_excel(filename)
    img_list = df_img['url_img'].to_list()
    j = 0
    print(img_list)
    for i in img_list:
        j += 1
        img_data = requests.get(i).content
        with open(image_path+'\image_name_'+str(j)+'.jpg', 'wb') as handler:
            handler.write(img_data)
    print('ok')

download_img()