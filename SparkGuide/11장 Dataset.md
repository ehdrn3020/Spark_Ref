
## 11장 데이터소스

```commandline
- Dataset은 스칼라와 자바에서만 사용할 수 있음
- 스칼라나 자바를 사용할 때 모든 DataFrame은 Dataset을 의미
```
<br/>

### 11.1 Dataset을 사용할 시기
```commandline
Dataset을 사용해야하는 이유
- DataFrame 기능만으로는 수행할 연산을 표현할 수 없을 때
- 성능 저하를 감수하더라도 타입 안정성(type-safe)을 가진 데이터타입을 사용할 경우

예시)
- 복잡한 비즈니스 로직을 단일 함수로 인코딩해야하는 경우
- 정확도와 방어적 코드가 속도보다 중시될 때 (문자열의 뺄셈의 정의하는 함수)
```
<br/>

### 11.2 Dataset 생성
```commandline
- 정의할 스키마를 미리 알고 있어야 함
- 자바에서 데이터 타입 클래스를 정의한 다음 Dataset<Row> 지정해 인코딩

import org.apache.spark.sql.Encoders;

public class Flight implements Serializable {
    string DEST_COUNTRY_NAME;
    string ORIGIN_COUNTRY_NAME;
    long DEST_COUNTRY_NAME;
}

Dataset<Flight> flights = spark.read.parquet("/data/aaa.parquet/")
    .as(Encoders.bean(Flight.class));
```
<br/>

### 11.4 트랜스포메이션
```commandline
- Dataset의 트랜스포메이션은 DataFrame과 동일

- 필터링
def originIsDestination(flight_row: Flight): Boolean = {
  return flight_row.ORIGIN_COUNTRY_NAME == flight_row.DEST_COUNTRY_NAME
}
flights.filter(flight_row => originIsDestination(flight_row)).first()

매핑 - 트랜스포메이션
val destinations = flights.map(f => f.DEST_COUNTRY_NAME)
```
<br/>

### 11.5 조인
```commandline
- 조인은 DataFrame과동일하지만 joinWith처럼 정교한 메서드 제공
- 각 컬럼은 단일 Dataset 처럼 다룰 수 있어 조인 수행시 더 많은 정보를 다를 수 있음

case class FlightMetadata(count: BigInt, randomData: BigInt)

val flightsMeta = spark.range(500).map(x => (x, scala.util.Random.nextLong))
  .withColumnRenamed("_1", "count").withColumnRenamed("_2", "randomData")
  .as[FlightMetadata]

val flights2 = flights
  .joinWith(flightsMeta, flights.col("count") === flightsMeta.col("count"))
```
<br/>

### 11.6 그룹화 집계
```commandline
- groupBy, rollup, cube 메서드를 여전히 사용 가능

flights.groupByKey(x => x.DEST_COUNTRY_NAME).count()
```
<br/>