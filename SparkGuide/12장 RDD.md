## 12장 RDD
```commandline
- 저수준 API는 RDD, SparkContext, 브로드캐스트 변수, 분산형 공유변수를 의미
- 대부분 고수준 API (DataFrame, Dataset)을 사용하는 것이 좋음
- DataFrame, Dataset 실행 시 RDD로 컴파일 됨
```
<br/>

### 12.1 저수준 API란
```commandline
- 언제 사용할까?
  - 클러스터의 물리적 데이터의 배치를 아주 세밀하게 제어하는 상황
  - RDD를 사용해 개발된 기존 코드를 유지하는 경우
  - 사용자가 정의한 공유 변수를 다뤄야 하는 경우 (14장 참조)

- 어떻게 사용할까?
  - 저수준 API 진입점인 SparkContext 사용
  - spark.sparkContext
```
<br/>

### 12.2 RDD 개요
```commandline
- RDD는 불변성을 가지고 병렬로 처리할 수 있는 파티셔닝된 레코드 모음
  - DataFrame의 레코드는 스키마를 가지는 필드로 구성된 구조화된 로우
  - RDD의 레코드는 자바나 파이썬의 객체
  
- 구조적 API는 자동으로 데이터를 최적화하고 압축된 바이너리 포맷으로 저장하지만 RDD는 이를 수동으로 지정해야 함

- 내부적으로 5가지 주요 속성으로 구분 됨
  - 파티션의 목록
  - 각 조각을 연산하는 함수
  - 다른 RDD와의 의존성 목록
  - 부가적으로 key-value RDD를 위한 Partitioner ( Hash Partitioning )
  - 부가적으로 각 조각을 연산하기 위한 기본 위치 목록 ( HDFS file block path )

- 파이썬로 RDD를 다룰 때 높은 오버헤드가 생기므로 파이썬에선 구조적 API 사용   
```
<br/>

### 12.3 RDD 생성하기
```commandline
- 기존에 사용하던 DataFrame, Dateset으로 rdd 메서드 호출
- rdd 메서드는 Row 타입을 가진 RDD를 생성
spark.range(10).toDF("id").rdd.map(lambda row: row[0])

- RDD를 사용해 DataFrame 생성
spark.range(10).rdd.toDF()

- 로컬 컬렉션으로 RDD 생성
- sparkContext의 parallelize 메서드 호출, 단일 노드에 있는 컬렉션을 병렬 컬렉션으로 전환
- 2개의 파티션을 가진 병렬 컬렉션 객체 생성
myCollection = "Spark The Definitive Guide : Big Data Processing Made Simple".split(" ")
words = spark.sparkContext.parallelize(myCollection, 2)
```
<br/>

### 12.5 트랜스포메이션
```commandline
- distinct
words.distinct().count()

- filter 
def startsWithS(individual):
  return individual.startswith("S")
words.filter(lambda word: startsWithS(word)).collect()
>>> ['Spark', 'Simple']

- map
words2 = words.map(lambda word: (word, word[0], word.startswith("S")))
words2.take(5)
>>> [('Spark', 'S', True), ('The', 'T', False), ...]
```
<br/>

### 12.6 액선
```commandline
- DataFrame과 동이랗게 지정된 트랜스포메이션 연산을 시작하려면 액션을 사용

- reduce ( RDD의 모든 값을 하나의 값으로 생성 )
spark.sparkContext.parallelize(range(1, 5)).reduce(lambda x, y: x + y)
>>> 10

- first ( 데이터셋의 첫 번째 값을 반환 )
words.first()
>>> 'Spark'

- max
spark.sparkContext.parallelize(range(1,30)).max()
>> 29

- take
words.take(5)
>>> ['Spark', 'The', 'Definitive', 'Guide', ':']
words.takeOrdered(5)
>>> [':', 'Big', 'Data', 'Definitive', 'Guide']
words.top(5)
>>> ['The', 'Spark', 'Simple', 'Processing', 'Made']
```
<br/>

### 12.7 파일 저장하기
```commandline
words.saveAsTextFile("file:/tmp/path")
```
<br/>

### 12.8
```commandline
- 캐싱 
- 메모리에 있는 데이터를 대상으로 함
words.cache()
```
<br/>

### 12.9 체크포인팅
```commandline
- DataFrame API에서 사용할 수 없는 기능
- RDD를 디스크에 저장하여 나중에 RDD를 참조할 때 RDD를 생성하지 않고 디스크에서 파티션 참조
spark.sparkContext.setCheckpointDir("/some/path")
words.checkpoint()
```
<br/>