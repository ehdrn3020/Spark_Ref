## 13장 RDD 고급개념
```commandline
핵심주제
- 집계와 키-값 형태의 RDD
- 사용자 정의 파티셔닝
- RDD 조인
```
<br/>

### 13.1 키-값 형태의 기초
```commandline
words.map(lambda word: (word.lower(), 1)).take(5)
>>> [('spark', 1), ('the', 1), ('definitive', 1), ('guide', 1), (':', 1)]


- [1] key-value 구조로 만들기 ( 튜플 )
keyword = words.keyBy(lambda word: word.lower()[0])
>>> [('s', 'Spark'), ('t', 'The'), ('d', 'Definitive'), ('g', 'Guide'), (':', ':')]


- [2] key, value 값 추출하기
keyword.keys().collect()
keyword.values().collect()


- [3] lookup
- 특정 키에 관한 결과를 찾음 ( 하나의 키만 찾는 메소드는 없음 )
keyword.lookup("s")
```
<br/>

### 13.2 집계
```commandline
chars = words.flatMap(lambda word: word.lower())
KVcharacters = chars.map(lambda letter: (letter, 1))
KVcharacters.take(5)
>>> [('s', 1), ('p', 1), ('a', 1), ('r', 1), ('k', 1)]


- [1] countByKey 메서드는 각 키의 아이텀 수를 구함
KVcharacters.countByKey()
>>> defaultdict(<class 'int'>, {'s': 4, 'p': 3, 'a': 4, 'r'....})


- [2] groupByKey 
from functools import reduce
def addFunc(left, right):
  return left + right
  
KVcharacters.groupByKey().map(lambda row: (row[0], reduce(addFunc, row[1]))).collect()
>>> [('p', 3), ('t', 3), ('d', 4), ('g', 3), ('b', 1), ('o', 1) ...]
```
<br/>

### 13.4 조인
```commandline
- 구조적 API와 동일한 조인 방식이지만, RDD를 사용하면 사용자가 많은 부분에 관여해야 함
- inner join
import random
distinctChars = words.flatMap(lambda word: word.lower()).distinct()
keyedChars = distinctChars.map(lambda c: (c, random.random()))
>>> [('p', 0.07471830168125726), ('t', 0.5281442744239391), ('d', 0.6968018446068369)...]
KVcharacters.join(keyedChars).count()
KVcharacters.join(keyedChars, outputPartitions).count()
>>> 51
```
<br/>

### 13.5 파티션 제어하기
```commandline
- RDD를 사용하면 데이터가 클러스터 전체에 물리적으로 정확히 분산되는 방식을 정의할 수 있음

- [1] coalesce
- 파티션을 재분배 할 때 데이터 셔플을 방지하기 위해 동일한 워커에 존재하는 파티션을 합치는 메서드
words.coalesce(1).getNumPartitions() # 1


- [2] repartition
- 파티션 수를 늘리거나 줄일 수 있고, 노드 간의 셔플이 발생 함
words.repartitions(10) # 10개의 파티션 생성


- [3] 사용자 정의 파티션
- 페이지랭크(PageRank)는 사용자 정의 파티셔닝을 이용해 클러스터 전체의 데이터를 균등하게 분배
- 과정은, 구조적API로 RDD를 얻고 사용자 정의 파티셔너를 적용하고 다시 구조적API로 변환
- 사용자정의 파티셔너를 사용하려면 Partitioner 클래스 통해 구현  

- 예제 1) 기본 제공 HashPartitioner, RangePartitioner
df = spark.read.option("header", "true").option("inferSchema", "true")\
  .csv("/data/retail-data/all/")
rdd = df.coalesce(10).rdd


- 예제 2) 17850, 12583 고객의 데이터가 커서 따로 나누어 처리 
def partitionFunc(key):
  import random
  if key == 17850 or key == 12583:
    return 0
  else:
    return random.randint(1,2)
    
keyedRDD = rdd.keyBy(lambda row: row[6])
keyedRDD\
  .partitionBy(3, partitionFunc)\
  .map(lambda x: x[0])\
  .glom()\
  .map(lambda x: len(set(x)))\
  .take(5)
```
