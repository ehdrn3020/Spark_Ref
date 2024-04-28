from pyspark.sql.types import StructField, StructType, StringType, LongType
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local").appName("Word Count")\
    .config("spark.some.config.option", "some-value")\
    .getOrCreate()

myManualSchema = StructType([
    StructField('DEST_COUNTRY_NAME', StringType(), True),
    StructField('ORIGIN_COUNTRY_NAME', StringType(), True),
    StructField('count', LongType(), False, metadata={"hello":"world"})
])

df = spark.read.format("json").schema(myManualSchema).load('/Users/myName/Test/Spark_ref/sparkGuide/data/2015-summary.json')