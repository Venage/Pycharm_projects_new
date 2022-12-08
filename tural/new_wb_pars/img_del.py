import os
import glob

image_path = r'C:\PyProjects\poject_1\tural\new_wb_pars\images\phone'

files = glob.glob(image_path+'/*')
for f in files:
    os.remove(f)