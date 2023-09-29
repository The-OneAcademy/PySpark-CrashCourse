# -*- coding: utf-8 -*-
"""Pyspark-Training-Handle-Null-Duplicates.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UjVwijpJZimFaWywgNcRsVP54i_PXqZ2
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
myschema = StructType([
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

df = spark.read.csv("original.csv", header=True, schema=myschema)
df.show()

df_dropped = df.na.drop()
df_dropped.show()

df_null_jobs = df.filter(df.JobTitle.isNotNull())
df_null_jobs.show()

from pyspark.sql.functions import *
df_handled = df.withColumn("Clean_City", when(df.City.isNull(), 'Unknown').otherwise(df.City))
df_handled.show()

df_no_duplicates = df.dropDuplicates()
df_no_duplicates.show()
