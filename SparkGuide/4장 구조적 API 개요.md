
## 4장 구조적 API 개요

```commandline
구조적 API에는 3가지 분산 컬렉션 API가 있음
- Dataset
- DataFrame
- SQL Table & View

3가지 핵심 개념
- 타입형 / 비타입형 API 개념과 차이점
- 핵심용어
- 스파크가 구조적 API의 데이터 흐름을 해석하고 클러스터에서 실행하는 방식
```

### 4.1 DataFrame과 Dataset
```commandline
- DataFrame과 Dataset은 잘 정의된 로우와 컬럼을 가지는 분산 테이블 형태의 컬렉션
- 값 없음은 null 로 표시
```

### 4.2 스키마
```commandline
- 스키마는 DataFrame의 컬럼명과 데이터 타입을 지정
- 스키마는 데이터소스에서 얻거나 (schema on read) 직접 정의
```

### 4.3 스파크의 구조적 데이터 타입 개요
```commandline
- 데이터 타입 정보를 가지고 있는 카탈리스트(Catalyst) 엔진을 사용
- 스파크는 자체 타입을 지원하는 여러 언어 API와 직접 맵핑되며 각 언어에 대한 맵핑 테이블을 가지고 있음
- 따라서 여러 언어로 Spark 프로그래밍 가능

로우
- 로우는 데이터 레코드이며 SQL, RDD, 데이터소스에서 얻거나 직접 만듬
- Ex. spark.range(2).collect()

스파크 데이터 타입
- 파이썬은 데이터 타입과 관련된 제약사항이 있음
```

### 4.4 구조적 API의 실행 과정
```commandline
단계
1. DataFrame/Dataset/SQL 이용해 코드를 작성 ( 카탈리스트 옵티마이저로 구조적 API
2. 논리적 실행 계획으로 변환
3. 논리적 실행 계획을 물리적 실행 계획으로 변환, 추가적인 최적화를 할 수 있는지 확인
4. 스파크는 클러스터에서 물리적 실행 계획(RDD 처리)를 실행
```

카탈리스트 옵티마이저 
```commandline
- 카탈리스트 옵티마이저(Catalyst Optimizer)는 Apache Spark의 쿼리 실행 엔진
- DataFrame API나 SQL 쿼리를 실행할 때 사용되며, 
- 쿼리의 논리적 및 물리적 실행 계획을 최적화하는 역할


주요 기능

논리적 최적화(Logical Optimization):
- 사용자가 작성한 쿼리나 DataFrame의 연산을 파싱하고 논리적 트리(Logical Plan)로 변환
- 논리적 트리를 분석하여 최적화할 수 있는 방법을 적용
- 예를 들어, 필요하지 않은 연산을 제거하거나 조인 순서를 변경하여 성능을 개선

물리적 최적화(Physical Optimization):
- 논리적 최적화된 트리를 물리적 실행 계획(Physical Plan)으로 변환
- 각 논리적 연산에 대해 가장 효율적인 물리적 연산 방법을 선택
- 예를 들어, 적절한 조인 알고리즘을 선택하거나 인덱스를 활용하여 데이터를 스캔
- 물리적 실행 계획의 각 단계에서 적절한 파티션 수 및 크기를 결정

쿼리 최적화(Query Optimization):
- 다양한 쿼리 최적화 기법을 사용하여 전체 쿼리의 성능을 최적화
- 예를 들어, 필터링 조건을 푸시 다운하거나 불필요한 데이터 이동을 최소화할 수 있습니다.
```
<img src="./image/4-1.png" width="500">

