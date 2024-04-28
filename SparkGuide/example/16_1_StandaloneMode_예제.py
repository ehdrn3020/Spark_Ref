from __future__ import print_function

if __name__ == '__main__':
    from pyspark.sql import SparkSession
    spark = SparkSession.builder \
        .master("spark://0.0.0.0:7077") \
        .appName("Word Count") \
        .config("spark.eventLog.enabled", "true") \
        .config("spark.eventLog.dir", "file:///opt/homebrew/Cellar/apache-spark/3.5.1/tmp/sparkui/") \
        .getOrCreate()

    df1 = spark.range(2, 10000000, 2)
    df2 = spark.range(2, 10000000, 4)
    step1 = df1.repartition(5)
    step12 = df2.repartition(6)
    step2 = step1.selectExpr("id * 5 as id")
    step3 = step2.join(step12, ["id"])
    step4 = step3.selectExpr("sum(id)")
    step4.collect()

# spark-submit SparkGuide/example/16_1.py