# -*- coding: utf-8 -*-
"""PySpark-Training-SQL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t1u3ghG2V-12tV0Y16XemWQFp_A6y5yX
"""

!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q http://archive.apache.org/dist/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz
!tar xf spark-3.1.1-bin-hadoop3.2.tgz
!pip install -q findspark
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.1.1-bin-hadoop3.2"
import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()
spark

from pyspark.sql.types import *
schema = StructType([
 StructField('id', IntegerType()),
 StructField('first_name', StringType()),
 StructField('last_name', StringType()),
 StructField('gender', StringType()),
 StructField('City', StringType()),
 StructField('JobTitle', StringType()),
 StructField('Salary', StringType()),
 StructField('Latitude', FloatType()),
 StructField('Longitude', FloatType())
])

df = spark.read.csv("original.csv", header=True, schema=schema)
df.show()

df.registerTempTable("original")

query1 = spark.sql('select * from original')
query1.show()

query2 = spark.sql('select concat(first_name," ", last_name) as full_name from original where gender="Female"')
query2.show()

"""Using With Column"""

from pyspark.sql.functions import *
df = df.withColumn('clean_salary', df.Salary.substr(2,1000).cast('float') )
df.show()

df = df.withColumn('monthly_salary', df.clean_salary/12)
df.show()

df = df.withColumn('are they female', when(df.gender =='Female','Yes').otherwise('No'))
df.show()

"""Using GroupBy..."""

from pyspark.sql.functions import *
df = df.withColumn('clean_salary', df.Salary.substr(2,1000).cast('float') )
df.show()

"""GroupBy Gender and Sum """

import pyspark.sql.functions as sqlfunc
df1 = df.groupBy('gender').agg(sqlfunc.sum('clean_salary'))
df1.show()

"""GroupBy Gender """

import pyspark.sql.functions as sqlfunc
df1 = df.groupBy('gender').agg( sqlfunc.sum('clean_salary').alias('Total'),
                                sqlfunc.avg('clean_salary').alias('Average'),
                                sqlfunc.min('clean_salary').alias('Minimum'),
                                sqlfunc.max('clean_salary').alias('Maximum'))
df1.show()

"""GroupBy Gender and City"""

import pyspark.sql.functions as sqlfunc
df1 = df.groupBy('gender','City').agg( sqlfunc.sum('clean_salary').alias('Total'),
                                sqlfunc.avg('clean_salary').alias('Average'),
                                sqlfunc.min('clean_salary').alias('Minimum'),
                                sqlfunc.max('clean_salary').alias('Maximum'))
df1.show()

"""Writing DataFrames to Files"""

df1.write.csv('df1.csv')
df1.write.json('df1.json')
df1.write.parquet('df1.parquet')
