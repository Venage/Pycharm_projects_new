import pyspark
from pyspark.sql import SparkSession
import pandas as pd
#from sklearn.model_selection import train_test_split

spark = SparkSession.builder.appName('Practise').getOrCreate()

df = pd.read_excel(r'A:\tural\parsing_4.xlsx')
spark_df = spark.createDataFrame(df)

spark_df.show()