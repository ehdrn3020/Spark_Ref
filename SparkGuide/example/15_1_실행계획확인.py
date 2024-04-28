# Creating a SparkSession in Python
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local").appName("Word Count")\
    .config("spark.some.config.option", "some-value")\
    .getOrCreate()


# COMMAND ----------

df1 = spark.range(2, 10000000, 2)
df2 = spark.range(2, 10000000, 4)
step1 = df1.repartition(5)
step12 = df2.repartition(6)
step2 = step1.selectExpr("id * 5 as id")
step3 = step2.join(step12, ["id"])
step4 = step3.selectExpr("sum(id)")

step4.collect() # 2500000000000

step4.explain() # 실행계획 확인
# +- Exchange SinglePartition, ENSURE_REQUIREMENTS, [plan_id=44]
#       +- HashAggregate(keys=[], functions=[partial_sum(id#8L)])
#          +- Project [id#8L]
#             +- SortMergeJoin [id#8L], [id#2L], Inner
#                :- Sort [id#8L ASC NULLS FIRST], false, 0
#                :  +- Exchange hashpartitioning(id#8L, 200), ENSURE_REQUIREMENTS, [plan_id=36]
#                :     +- Project [(id#0L * 5) AS id#8L]
#                :        +- Exchange RoundRobinPartitioning(5), REPARTITION_BY_NUM, [plan_id=26]
#                :           +- Range (2, 10000000, step=2, splits=10)
#                +- Sort [id#2L ASC NULLS FIRST], false, 0
#                   +- Exchange hashpartitioning(id#2L, 200), ENSURE_REQUIREMENTS, [plan_id=37]
#                      +- Exchange RoundRobinPartitioning(6), REPARTITION_BY_NUM, [plan_id=29]
#                         +- Range (2, 10000000, step=4, splits=10)
