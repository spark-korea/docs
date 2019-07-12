---
layout: global
title: Hive Tables
displayTitle: Hive Tables
---


# **Hive 테이블**



*   <span style="text-decoration:underline;">Hive 테이블의 저장 형식 명시하기</span>
*   <span style="text-decoration:underline;">다른 버전의 Hive 메타스토어와 연동하기</span>

스파크 SQL은 Apache Hive에 저장된 데이터에 대한 읽기/쓰기를 지원합니다. Hive가 이미 많은 의존 라이브러리를 포함하고 있기때문에, 기본 스파크 배포판은 이 의존 라이브러리를 포함하고 있지 않습니다. Hive의 의존성 라이브러리를 classpath에서 찾을 수 있으면, 스파크는 이를 자동으로 로드합니다. 모든 작업 노드가 Hive에 저장된 데이터에 접근하기 위해 Hive 직렬화/역직렬화 라이브러리(SerDe) 그리고 Hive 의존 라이브러리는 모든 작업 노드에서 접근 가능해야 합니다.

Hive 관련 설정을 하기 위해서는 conf/ 안에 `hive-site.xml`, `core-site.xml`(보안 설정용)과 `hdfs-site.xml`(HDFS 설정용)파일을 넣어 주면 됩니다.

Hive를 사용할 때, SparkSession를 객체에 지속되는 Hive 메타스토어로의 연결성, Hive SerDe, Hive 사용자 정의 함수 등의 기능을 설정할 수 있습니다. Hive 배포판이 설치되어 있지 않더라도 Hive 지원을 활성화할 수 있습니다. `hive-site.xml`이 설정되어 있지 않은 경우, 현재 디렉토리에서 `metastore_db`를 자동으로 생성하고 `spark.sql.warehouse.dir`에 설정된 디렉토리를 생성합니다. `spark-warehouse`의 기본 디렉토리는 스파크 애플리케이션을 시작한 현재 디렉토리입니다. `hive-site.xml`의 `hive.metastore.warehouse.dir `속성은 스파크 2.0.0 버전부터 더 이상 지원되지 않으며, 대신 warehouse에서 데이터베이스의 기본 위치를 명시하려면 `spark.sql.warehouse.dir`을 사용해야 합니다. 스파크 애플리케이션을 실행하는 유저에게 쓰기 권한의 승인이 필요할 수 있습니다.



*   **Scala**


```
import java.io.File

import org.apache.spark.sql.{Row, SaveMode, SparkSession}

case class Record(key: Int, value: String)

// warehouseLocation은 hive 데이터베이스와 테이블의 기본 위치를 지정합니다.
val warehouseLocation = new File("spark-warehouse").getAbsolutePath

val spark = SparkSession
  .builder()
  .appName("Spark Hive Example")
  .config("spark.sql.warehouse.dir", warehouseLocation)
  .enableHiveSupport()
  .getOrCreate()

import spark.implicits._
import spark.sql

sql("CREATE TABLE IF NOT EXISTS src (key INT, value STRING) USING hive")
sql("LOAD DATA LOCAL INPATH 'examples/src/main/resources/kv1.txt' INTO TABLE src")

// HiveQL로 쿼리를 표현합니다. (역자 주: Spark SQL과 조금 다릅니다.)
sql("SELECT * FROM src").show()
// +---+-------+
// |key|  value|
// +---+-------+
// |238|val_238|
// | 86| val_86|
// |311|val_311|
// ...

// 집계 쿼리도 지원합니다
sql("SELECT COUNT(*) FROM src").show()
// +--------+
// |count(1)|
// +--------+
// |    500 |
// +--------+

// SQL 쿼리의 결과는 DataFrame으로 생성되며 모든 일반적인 함수를 지원합니다.
val sqlDF = sql("SELECT key, value FROM src WHERE key < 10 ORDER BY key")

// DataFrame은 Row 타입으로 이루어져 있습니다. 각 컬럼에는 index를 사용해서 접근할 수 있습니다.
val stringsDS = sqlDF.map {
  case Row(key: Int, value: String) => s"Key: $key, Value: $value"
}
stringsDS.show()
// +--------------------+
// |               value|
// +--------------------+
// |Key: 0, Value: val_0|
// |Key: 0, Value: val_0|
// |Key: 0, Value: val_0|
// ...

// DataFrame을 사용하여 SparkSession에 임시 뷰를 생성할 수 있습니다.
val recordsDF = spark.createDataFrame((1 to 100).map(i => Record(i, s"val_$i")))
recordsDF.createOrReplaceTempView("records")

// 이제, DataFrame의 데이터와 Hive에 저장된 데이터에 JOIN 쿼리를 사용할 수 있습니다.
sql("SELECT * FROM records r JOIN src s ON r.key = s.key").show()
// +---+------+---+------+
// |key| value|key| value|
// +---+------+---+------+
// |  2| val_2|  2| val_2|
// |  4| val_4|  4| val_4|
// |  5| val_5|  5| val_5|
// ...

// 스파크 SQL의 기존 문법 대신 HiveQL의 문법을 사용하여 Hive managed Parquet 테이블을 생성합니다.
// `USING hive`
sql("CREATE TABLE hive_records(key int, value string) STORED AS PARQUET")
// DataFrame을 Hive managed 테이블로 저장합니다.
val df = spark.table("src")
df.write.mode(SaveMode.Overwrite).saveAsTable("hive_records")
// 데이터를 삽입한 후에는 Hive 매니지드 테이블(managed table)에 데이터가 저장됩니다.
sql("SELECT * FROM hive_records").show()
// +---+-------+
// |key|  value|
// +---+-------+
// |238|val_238|
// | 86| val_86|
// |311|val_311|
// ...

// Parquet 데이터 디렉토리를 지정합니다.
val dataDir = "/tmp/parquet_data"
spark.range(10).write.parquet(dataDir)
// Hive 외부 Parquet 테이블을 생성합니다.
sql(s"CREATE EXTERNAL TABLE hive_ints(key int) STORED AS PARQUET LOCATION '$dataDir'")
// Hive 외부 테이블은 이미 데이터를 갖고있어야 합니다.
sql("SELECT * FROM hive_ints").show()
// +---+
// |key|
// +---+
// |  0|
// |  1|
// |  2|
// ...

// Hive 동적 파티셔닝(Partitioning)을 위한 플래그를 활성화합니다.
spark.sqlContext.setConf("hive.exec.dynamic.partition", "true")
spark.sqlContext.setConf("hive.exec.dynamic.partition.mode", "nonstrict")
// DataFrame API를 사용하여 Hive 분할 테이블을 생성합니다.
df.write.partitionBy("key").format("hive").saveAsTable("hive_part_tbl")
// 분할된 컬럼 `key`는 스키마의 마지막 순서로 이동합니다.
sql("SELECT * FROM hive_part_tbl").show()
// +-------+---+
// |  value|key|
// +-------+---+
// |val_238|238|
// | val_86| 86|
// |val_311|311|
// ...

spark.stop()
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/hive/SparkHiveExample.scala"에서 전체 예제 코드를 볼 수 있습니다.



*   **Python**


```
from os.path import expanduser, join, abspath

from pyspark.sql import SparkSession
from pyspark.sql import Row

# warehouse_location은 hive 데이터베이스와 테이블의 기본 위치를 지정합니다.
warehouse_location = abspath('spark-warehouse')

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL Hive integration example") \
    .config("spark.sql.warehouse.dir", warehouse_location) \
    .enableHiveSupport() \
    .getOrCreate()

# spark는 이미 생성한 SparkSession입니다.
spark.sql("CREATE TABLE IF NOT EXISTS src (key INT, value STRING) USING hive")
spark.sql("LOAD DATA LOCAL INPATH 'examples/src/main/resources/kv1.txt' INTO TABLE src")

# HiveQL로 쿼리를 표현합니다.
spark.sql("SELECT * FROM src").show()
# +---+-------+
# |key|  value|
# +---+-------+
# |238|val_238|
# | 86| val_86|
# |311|val_311|
# ...

# 집계 쿼리도 지원합니다.
spark.sql("SELECT COUNT(*) FROM src").show()
# +--------+
# |count(1)|
# +--------+
# |    500 |
# +--------+

# SQL 쿼리의 결과는 DataFrame으로 생성되며 모든 일반 함수를 지원합니다.
sqlDF = spark.sql("SELECT key, value FROM src WHERE key < 10 ORDER BY key")

# DataFrame은 Row 타입으로 이루어져 있습니다. 각 컬럼에는 index를 사용해서 접근할 수 있습니다
stringsDS = sqlDF.rdd.map(lambda row: "Key: %d, Value: %s" % (row.key, row.value))
for record in stringsDS.collect():
    print(record)
# Key: 0, Value: val_0
# Key: 0, Value: val_0
# Key: 0, Value: val_0
# ...

# DataFrame을 사용하여 SparkSession에 임시 뷰를 생성할 수 있습니다.
Record = Row("key", "value")
recordsDF = spark.createDataFrame([Record(i, "val_" + str(i)) for i in range(1, 101)])
recordsDF.createOrReplaceTempView("records")

# 이제, DataFrame의 데이터와 Hive에 저장된 데이터에 JOIN 쿼리를 사용할 수 있습니다.
spark.sql("SELECT * FROM records r JOIN src s ON r.key = s.key").show()
# +---+------+---+------+
# |key| value|key| value|
# +---+------+---+------+
# |  2| val_2|  2| val_2|
# |  4| val_4|  4| val_4|
# |  5| val_5|  5| val_5|
# ...
```


스파크 저장소의 "examples/src/main/python/sql/hive.py"에서 전체 예제 코드를 볼 수 있습니다.


### **Hive 테이블의 저장 형식 명시**

Hive 테이블을 생성할 때, 이 테이블이 어떻게 파일시스템에서/으로 데이터를 읽고/쓸지 정의해야 합니다. 다시 말해 “입력 형식"과 “출력 형식"을 정의해야 합니다. 또한, 이 테이블이 데이터를 로우로 역직렬화하거나 로우를 데이터로 직렬화하는 방식(serde)도 정의해야 합니다. 아래의 옵션(“serde”, “input format”, “output format”)을 사용하여 `CREATE TABLE src(id int) USING hive OPTIONS(fileFormat 'parquet') `와 같이 저장 형식을 명시할 수 있습니다. 기본적으로, 테이블 파일은 플레인 텍스트(plain text)로 읽어들입니다. 단, 테이블을 생성할 때 Hive의 스토리지 핸들러 기능은 아직 지원되지 않으므로, Hive에서 직접 저장소 핸들러를 사용하여 테이블을 생성하고 스파크 SQL에서 읽어오는 방법을 사용할 수 있습니다. \



<table>
  <tr>
   <td><strong>속성 이름</strong>
   </td>
   <td><strong>의미</strong>
   </td>
  </tr>
  <tr>
   <td><code>fileFormat</code>
   </td>
   <td>fileForamat은 "serde", "input format", "output format"등과 같은 저장 형식 명세의 한 종류입니다. 현재 6가지의 fileFormat을 지원합니다: 'sequencefile', 'rcfile', 'orc', 'parquet', 'textfile', 'avro'
   </td>
  </tr>
  <tr>
   <td><code>inputFormat, outputFormat</code>
   </td>
   <td>이 두 옵션은 글자 그대로 사용할 `InputFormat`과 `OutputFormat`의 이름을 지정합니다(문자열 타입).예를 들면, `org.apache.hadoop.hive.ql.io.orc.OrcInputFormat`와 같습니다. 이 두 가지 옵션은 한 쌍으로 함께 사용하며, `fileForamt` 옵션을 이미 사용하였다면 이 옵션은 사용할 수 없습니다.
   </td>
  </tr>
  <tr>
   <td><code>serde</code>
   </td>
   <td>seder 클래스의 이름을 명시합니다. `fileFormat` 옵션이 이미 명시되어 있고 여기에 serde에 대한 정보가 포함되어 있다면 이 옵션을 사용할 수 없습니다. 현재, 6가지의 fileFormat 옵션 중 "sequencefile", "textfile", "rcfile" 세 가지 옵션은 serde에 대한 정보를 포함하지 않으므로, fileFormat에서 이 세 가지 옵션을 사용하고 있을 때는 이 옵션을 사용할 수 있습니다.
   </td>
  </tr>
  <tr>
   <td><code>fieldDelim, escapeDelim, collectionDelim, mapkeyDelim, lineDelim</code>
   </td>
   <td>fileFormat 옵션으로 "textfile"이 지정되어 있을 때만 사용가능합니다. 필드가 구분된 파일(delimited file)을 로우로 변환하는 방법을 정의합니다.
   </td>
  </tr>
</table>


`OPTIONS`으로 정의되는 다른 모든 속성은 Hive serde 속성으로 간주됩니다. \
** \
서로 다른 버전의 Hive 메타스토어와 연동하기**

스파크 SQL의 Hive 지원에서 가장 중요한 부분 중 하나는, 스파크 SQL이 Hive 테이블의 메타데이터에 접근할 수 있도록 하는 Hive 메타스토어와의 연동 기능입니다. 스파크 1.4.0 버전부터, 아래에 설명된 설정을 사용하면, 단일 스파크 SQL 빌드에서 서로 다른 버전의 Hive 메타스토어에 쿼리를 실행할 수 있습니다. 연동하는 메타스토어 Hive의 버전과는 별개로, 스파크 SQL은 Hive 1.2.1 버전을 기준으로 컴파일되며 이 버전에 포함된 클래스(serde, UDF, UDAF 등)를 내부적으로 사용합니다.

아래의 옵션을 사용하여 메타데이터를 받아올 때 사용되는 Hive 버전을 설정할 수 있습니다:


<table>
  <tr>
   <td><strong>속성 이름</strong>
   </td>
   <td><strong>기본값</strong>
   </td>
   <td><strong>의미</strong>
   </td>
  </tr>
  <tr>
   <td><code>spark.sql.hive.metastore.version</code>
   </td>
   <td><code>1.2.1</code>
   </td>
   <td>Hive 메타스토어의 버전. \
0.12.0 버전부터 2.3.3 버전까지 사용할 수 있습니다.
   </td>
  </tr>
  <tr>
   <td><code>spark.sql.hive.metastore.jars</code>
   </td>
   <td><code>builtin</code>
   </td>
   <td>Hive 메타스토어에 연결할 때 사용하는 HiveMetastoreClient 객체를 생성하는데 사용될 jar 파일의 위치. 다음 세 가지 옵션이 사용 가능합니다:
<ol>

<li><code>builtin \
-Phive</code>이 활성화되어 있을 때 스파크에 포함되어 있는 Hive 1.2.1을 사용합니다. 이 옵션을 사용하면 <code>spark.sql.hive.metastore.version</code>는 1.2.1이 되거나 정의되지 않아야 합니다.

<li><code>maven \
</code>Maven 저장소에서 명시된 버전의 Hive jar를 다운로드하여 사용합니다. 이 설정을 배포판에서 사용하는 것은 추천하지 않습니다.

<li>JVM의 표준 형식 classpath. \
이 classpath는 Hive와 올바른 버전의 Hadoop을 포함한 모든 의존 라이브러리를 포함해야 합니다. 이 jar 파일은 드라이버 에서 접근 가능해야하며, yarn 클러스터 모드에서 실행하고자 한다면 애플케이션으로 패키지화되어 있어야 합니다.
</li>
</ol>
   </td>
  </tr>
  <tr>
   <td><code>spark.sql.hive.metastore.sharedPrefixes</code>
   </td>
   <td><code>com.mysql.jdbc,</code>
<p>
<code>org.postgresql,</code>
<p>
<code>com.microsoft.sqlserver,</code>
<p>
<code>oracle.jdbc</code>
   </td>
   <td>스파크 SQL과 (특정 버전의) Hive 클래스를 로드할 때 사용되는 classloader를 사용하여 로드해야하는 클래스들의 접두사 리스트(쉼표로 구분). 예를 들면, 메타스토어와 연결하기 위한 JDBC 드라이버 목록은 공유되어야 하는 클래스이므로, 드라이버 클래스의 접두사인 <code>com.mysql.jdbc, org.postgresql,</code> … 등이 지정되어야 합니다. 이미 공유되고 있는 클래스 간의 상호작용을 위해 필요한 클래스의 접두사 역시 명시되어야 합니다. (예: log4j에서 사용하는 사용자 정의 Appender)
   </td>
  </tr>
  <tr>
   <td><code>spark.sql.hive.metastore.barrierPrefixes</code>
   </td>
   <td><code>(empty)</code>
   </td>
   <td>스파크 SQL이 통신하는 Hive의 각 버전에 맞게 다시 로드해야 하는 클래스 접두사 목록(쉼표로 구분). 예를 들어 일반적으로 공유되는 접두사에서 선언한 Hive UDF가 여기에 포함됩니다. (예: <code>org.apache.spark.*</code>)
   </td>
  </tr>
</table>