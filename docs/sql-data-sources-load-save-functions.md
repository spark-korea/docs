---
layout: global
title: Generic Load/Save Functions
displayTitle: Generic Load/Save Functions
---


# **일반 불러오기/저장하기 함수**



* [옵션 명시하기](#heading=h.3uxn3fu94adv)
* [파일 내에서 SQL 바로 실행하기](#heading=h.b7erx88romzu)
* [저장 모드](#heading=h.u0rwa1z5skeu)
* [지속 테이블에 저장하기](#heading=h.3n9dj4nf090w)
* [버케팅, 정렬, 분할](#heading=h.c2zuz2t3c96d)

가장 간단한 형태로, 모든 연산에서는 기본 데이터 소스(`spark.sql.sources.default`값이 따로 설정되지 않았을 경우 기본값은 `parquet`)가 사용됩니다. 



*   **Scala**


```
val usersDF = spark.read.load("examples/src/main/resources/users.parquet")
usersDF.select("name", "favorite_color").write.save("namesAndFavColors.parquet")
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala"에서 전체 예제 코드를 볼 수 있습니다.



*   **Python**


```
df = spark.read.load("examples/src/main/resources/users.parquet")
df.select("name", "favorite_color").write.save("namesAndFavColors.parquet")
```


스파크 저장소의 "examples/src/main/python/sql/datasource.py"에서 전체 예제 코드를 볼 수 있습니다.


### **옵션 명시하기**

사용될 데이터 소스와 여기에 추가할 옵션을 직접 명시할 수 있습니다. 데이터 소스는 각 전체 이름(예: `org.apache.spark.sql.parquet`)으로 명시되어야 하지만 내장된 데이터 소스의 경우 축약된 이름(`json`, `parquet`, `jdbc`, `orc`, `libsvm`, `csv`, `text`)만으로도 사용할 수 있습니다. 임의의 데이터 소스 타입에서 불러온 DataFrame을 다른 타입으로 변환하려면 아래와 같이 할 수 있습니다.

 \
JSON 파일을 로드하려면 아래와 같이 할 수 있습니다:



*   **Scala**


```
val peopleDF = spark.read.format("json").load("examples/src/main/resources/people.json")
peopleDF.select("name", "age").write.format("parquet").save("namesAndAges.parquet")
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala"에서 전체 예제 코드를 볼 수 있습니다.

 \
CSV 파일을 로드하려면 아래와 같이 할 수 있습니다:



*   **Python**


```
df = spark.read.load("examples/src/main/resources/people.json", format="json")
df.select("name", "age").write.save("namesAndAges.parquet", format="parquet")
```


CSV 파일을 로드하려면 아래와 같이 할 수 있습니다:



*   **Scala**


```
val peopleDFCsv = spark.read.format("csv")
  .option("sep", ";")
  .option("inferSchema", "true")
  .option("header", "true")
  .load("examples/src/main/resources/people.csv")
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala"에서 전체 예제 코드를 볼 수 있습니다.

쓰기 동작에서도 별도의 옵션을 사용할 수 있습니다. 예를 들어 ORC 데이터 소스에 블룸 필터(bloom filters)를 사용하거나 사전식 인코딩(dictionary encodings)을 사용할 수 있습니다. 아래 ORC 예제에서는 `favorite_color`라는 블룸 필터를 생성하고 `name`과 `favorite_color`에 사전식 인코딩을 사용합니다. Parquet에서는 `parquet.enable.dictionary`를 사용할 수 있습니다. ORC/Parquet에 대한 추가 옵션에 대한 내용을 더 자세히 알고 싶다면 아파치 ORC/Parquet 프로젝트의 공식 웹사이트를 참조하세요.



*   **Python**


```
df = spark.read.load("examples/src/main/resources/people.csv",
                     format="csv", sep=":", inferSchema="true", header="true")
```


스파크 저장소의 "examples/src/main/python/sql/datasource.py"에서 전체 예제 코드를 볼 수 있습니다.

쓰기 동작에서도 추가 옵션을 사용할 수 있습니다. 예를 들어 ORC 데이터 소스에 블룸 필터를 사용하거나 사전식 인코딩을 사용할 수 있습니다. 아래 ORC 예제에서는 `favorite_color`라는 블룸 필터를 생성하고 각 `name`을 `favorite_color`에 사전식으로 인코딩할 것입니다. Parquet에서는 `parquet.enable.dictionary`를 사용할 수 있습니다. ORC/Parquet에 대한 추가 옵션에 대한 내용을 더 자세히 알고 싶다면 공식 아파치(Apache) ORC/Parquet 웹사이트를 방문하세요.



*   **Scala**


```
usersDF.write.format("orc")
  .option("orc.bloom.filter.columns", "favorite_color")
  .option("orc.dictionary.key.threshold", "1.0")
  .save("users_with_options.orc")
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala"에서 전체 예제 코드를 볼 수 있습니다.



*   **Python**


```
df = spark.read.orc("examples/src/main/resources/users.orc")
(df.write.format("orc")
    .option("orc.bloom.filter.columns", "favorite_color")
    .option("orc.dictionary.key.threshold", "1.0")
    .save("users_with_options.orc"))
```


스파크 저장소의 "examples/src/main/python/sql/datasource.py"에서 전체 예제 코드를 볼 수 있습니다.


### **파일 내에서 SQL 바로 실행하기**

읽기 API를 사용하여 파일을 DataFrame으로 로드하고 쿼리하는 대신, 파일 내에서 바로 SQL을 실행할 수 있습니다.



*   **Scala**


```
val sqlDF = spark.sql("SELECT * FROM parquet.`examples/src/main/resources/users.parquet`")
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala"에서 전체 예제 코드를 볼 수 있습니다.



*   **Python**


```
df = spark.sql("SELECT * FROM parquet.`examples/src/main/resources/users.parquet`")
```


스파크 저장소의 "examples/src/main/python/sql/datasource.py"에서 전체 예제 코드를 볼 수 있습니다.


### **저장 모드**

저장 동작에서는 기존의 데이터를 어떻게 처리할지 명시하는 `SaveMode `옵션을 사용할 수 있습니다. 이 저장 모드는 원자적(atomic)이지 않거나 락이 걸려있지 않은 경우에는 사용할 수 없다는 점을 꼭 알아두어야 합니다. 또한, `Overwrite`를 수행할 때는 새로운 데이터를 쓰기 이전에 기존의 데이터가 먼저 지워집니다. \



<table>
  <tr>
   <td><strong>Scala/Java</strong>
   </td>
   <td><strong>다른 언어</strong>
   </td>
   <td><strong>의미</strong>
   </td>
  </tr>
  <tr>
   <td><code>SaveMode.ErrorIfExists</code>(기본값)
   </td>
   <td><code>"error" 또는 "errorifexists"</code>(기본값)
   </td>
   <td>DataFrame을 데이터 소스로 저장할 때 데이터가 이미 존재한다면 예외를 발생시킵니다. \

   </td>
  </tr>
  <tr>
   <td><code>SaveMode.Append</code>
   </td>
   <td><code>"append"</code>
   </td>
   <td>DataFrame을 데이터 소스에 저장할 때 데이터/테이블이 이미 존재한다면 DataFrame의 내용을 기존의 데이터에 추가합니다. \

   </td>
  </tr>
  <tr>
   <td><code>SaveMode.Overwrite</code>
   </td>
   <td><code>"overwrite"</code>
   </td>
   <td>덮어쓰기 모드는 DataFrame을 데이터 소스에 저장할 때 데이터/테이블이 이미 존재한다면 DataFrame의 내용으로 덮어쓰기합니다.  \

   </td>
  </tr>
  <tr>
   <td><code>SaveMode.Ignore</code>
   </td>
   <td><code>"ignore"</code>
   </td>
   <td>건너뛰기(ignore) 모드는 DataFrame을 데이터 소스에 저장할 때 데이터가 이미 존재한다면 DataFrame의 저장 동작을 수행하지 않고 기존의 데이터를 변경하지 않습니다. SQL의 <code>CREATE TABLE IF NOT EXISTS</code>과 유사합니다. \

   </td>
  </tr>
</table>



### **지속(Persistent) 테이블에 저장하기**

`saveAsTable`명령어를 사용하면 `DataFrame`을 Hive 메타스토어에 지속 테이블로 저장할 수 있습니다. 이 기능은 이미 사용중인 Hive가 있어야 하는 것은 아닙니다. 스파크는 사용자를 위해 (Derby를 사용하여) 로컬 Hive 메타스토어를 생성합니다. `createOrReplaceTempView` 명령어와는 다르게 `saveAsTable`는 DataFrame의 내용을 저장한 뒤 Hive 메타스토어에 저장된 위치를 가리키는 포인터를 생성합니다. 지속 테이블은 스파크 프로그램을 재시작하더라도 동일한 메타스토어에 연결을 유지하기만 한다면 계속 유지됩니다. 지속 테이블의 DataFrame은 `SparkSession`에서 테이블 이름으로 `table`메소드를 호출하여 생성할 수 있습니다.

파일 기반 데이터 소스(예: text, parquet, json 등)에서는 `path` 옵션을 사용하여 커스텀 테이블 경로를 명시할 수 있습니다(예: `df.write.option("path", "/some/path").saveAsTable("t")`). 테이블이 삭제될 때 커스텀 테이블 경로는 삭제되지 않고 테이블의 데이터도 그대로 유지됩니다. 테이블에 지정된 경로가 존재하지 않을 때, 스파크는 웨어하우스 디렉토리의 기본 테이블 경로에 데이터를 작성합니다. 테이블이 삭제되면 기본 테이블 경로도 함께 삭제됩니다. \
스파크 2.1버전부터, 지속 데이터 소스 테이블은 Hive 메타스토어 내에서 각 파티션마다 메타데이터를 가지게 됩니다. 이는 여러 가지 장점이 있습니다:



*   메타스토어는 각 쿼리에 필요한 파티션만 반환하기 때문에 테이블에 대한 전체 파티션의 탐색은 필요하지 않습니다.
*   데이터 소스 API로 생성된 테이블에서 `ALTER TABLE PARTITION ... SET LOCATION`과 같은 Hive DDL를 사용할 수 있습니다.

(`path` 옵션을 이용하여) 외부 데이터 소스로 테이블을 생성할 때, 각 파티션의 정보는 자동으로 얻을 수 없습니다. 메타스토어의 파티션 정보를 동기화하기 위해서는 `MSCK REPAIR TABLE`을 실행해야 합니다.


### **버키팅, 정렬, 파티셔닝**

파일 기반 데이터 소스에서 버키팅(Bucketing), 정렬, 파티셔닝을 사용할 수 있습니다. 버키팅, 정렬은 지속 테이블에만 사용할 수 있습니다:



*   **Scala**


```
peopleDF.write.bucketBy(42, "name").sortBy("age").saveAsTable("people_bucketed")
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala"에서 전체 예제 코드를 볼 수 있습니다.

반면에 분할은 Dataset API를 사용할 때 `save`와 `saveAsTable`에 모두 사용할 수 있습니다. \




*   **Python**


```
df.write.bucketBy(42, "name").sortBy("age").saveAsTable("people_bucketed")
```


스파크 저장소의 "examples/src/main/python/sql/datasource.py"에서 전체 예제 코드를 볼 수 있습니다. \
반면에 분할은 Dataset API를 사용할 때 `save`와 `saveAsTable`에 모두 사용할 수 있습니다.



*   **Scala**


```
usersDF.write.partitionBy("favorite_color").format("parquet").save("namesPartByColor.parquet")
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala"에서 전체 예제 코드를 볼 수 있습니다.

단일 테이블에서는 분할과 버케팅를 동시에 사용할 수 있습니다:



*   **Python**


```
df.write.partitionBy("favorite_color").format("parquet").save("namesPartByColor.parquet")
```


스파크 저장소의 "examples/src/main/python/sql/datasource.py"에서 전체 예제 코드를 볼 수 있습니다.

단일 테이블에서는 분할과 버케팅 동시에 사용할 수 있습니다:



*   **Scala**


```
usersDF
  .write
  .partitionBy("favorite_color")
  .bucketBy(42, "name")
  .saveAsTable("users_partitioned_bucketed")
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala"에서 전체 예제 코드를 볼 수 있습니다. \



```
partitionBy는 파티션 탐색에서 설명하고 있는 디렉토리 구조를 생성합니다. 따라서 컬럼에 저장되는 값의 집합의 크기(cardinality)가 큰 경우 사용에 한계가 있습니다. (역자 주: 컬럼에 저장되는 값마다 디렉토리가 하나씩 생성되니까.) 반면에 bucketBy는 정해진 수의 버킷에 데이터를 분산시키므로 주어진 컬럼에 무한히 많은 값들이 저장되는 경우에도 문제가 없습니다.

```



*   **Python**


```
df = spark.read.parquet("examples/src/main/resources/users.parquet")
(df
    .write
    .partitionBy("favorite_color")
    .bucketBy(42, "name")
    .saveAsTable("people_partitioned_bucketed"))
```


스파크 저장소 "examples/src/main/python/sql/datasource.py"에서 전체 예제 코드를 볼 수 있습니다.

`partitionBy`는 [파티션 탐색](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#partition-discovery)에서 설명하고 있는 디렉토리 구조를 생성합니다. 따라서 컬럼에 저장되는 값의 집합의 크기(cardinality)가 큰 경우 사용에 한계가 있습니다. (역자 주: 컬럼에 저장되는 값마다 디렉토리가 하나씩 생성되니까.) 반면에 `bucketBy`는 정해진 수의 버킷에 데이터를 분산시키므로 주어진 컬럼에 무한히 많은 값들이 저장되는 경우에도 문제가 없습니다.