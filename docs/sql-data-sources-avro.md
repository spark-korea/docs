---
layout: global
title: 아파치 Avro 데이터 소스 가이드
---

* This will become a table of contents (this text will be scraped).
{:toc}

스파크 2.4 이후, 스파크 SQL은 아파치 Avro 데이터 읽기와 쓰기 기능을 내장하고 있습니다.

## 배포하기
`spark-avro` 는 외부 모듈이기 때문에 `spark-submit` or `spark-shell`에 기본적으로 포함되어 있지 않습니다.

다른 스파크 응용 프로그램과 마찬가지로 `spark-submit`은 응용 프로그램을 실행하기 위해 사용됩니다. avro 기능을 사용하기 위해 필요한 `spark-avro_{{site.SCALA_BINARY_VERSION}}` 모듈과 이 모듈이 필요로 하는 다른 의존 라이브러리는 다음과 같이 `--packages` 를 이용하여 `spark-submit `에 추가될 수 있습니다.

    ./bin/spark-submit --packages org.apache.spark:spark-avro_{{site.SCALA_BINARY_VERSION}}:{{site.SPARK_VERSION_SHORT}} ...

`spark-shell`에서 해당 기능을 사용하기 위해서는, `--packages`를 이용하여 `org.apache.spark:spark-avro_2.11`와 이에 따르는 의존 라이브러리를 추가할 수 있습니다.

    ./bin/spark-shell --packages org.apache.spark:spark-avro_{{site.SCALA_BINARY_VERSION}}:{{site.SPARK_VERSION_SHORT}} ...

외부 의존성이 있는 응용 프로그램 실행에 대한 자세한 내용은 [응용 프로그램 실행 안내](submitting-applications.html)를 참조하세요.

## 불러오기와 저장하기 함수

`spark-avro` 는 외부 모듈이기 때문에 `DataFrameReader` 나 `DataFrameWriter`에 `.avro` API 가 없습니다.

Avro 형식으로 데이터를 불러오거나 저장하기 위해서는 데이터 소스 옵션 `format` 을 `avro`(또는 `org.apache.spark.sql.avro`)로 지정해야 합니다.
<div class="codetabs">
<div data-lang="scala" markdown="1">
{% highlight scala %}

val usersDF = spark.read.format("avro").load("examples/src/main/resources/users.avro")
usersDF.select("name", "favorite_color").write.format("avro").save("namesAndFavColors.avro")

{% endhighlight %}
</div>

<div data-lang="python" markdown="1">
{% highlight python %}

df = spark.read.format("avro").load("examples/src/main/resources/users.avro")
df.select("name", "favorite_color").write.format("avro").save("namesAndFavColors.avro")

{% endhighlight %}
</div>
</div>

## to_avro() 와 from_avro()
Avro 패키지는 컬럼을 Avro 형식의 바이너리로 인코드하는 `to_avro` 함수와 Avro 바이너리 데이터를 컬럼으로 디코드하는 `from_avro()`함수를 제공합니다. 두 함수는 하나의 컬럼을 다른 컬럼으로 변환하는 역할을 합니다. 해당 입력/출력 SQL 데이터 타입은 복합(complex) 타입과 기본 타입 모두가 될 수 있습니다.

Avro 레코드를 컬럼으로 사용하는 것은 Kafka와 같은 스트리밍 소스를 읽거나 쓸 때 유용합니다. 각 Kafka key-value 레코드는 Kafka의 timestamp나 Kafka의 offset과 같은 메타데이터와 합쳐지게 됩니다.
* 데이터를 포함하는 “value" 필드가 Avro로 되어있다면, `from_avro()`를 사용해서 데이터를 추출하고, 확장하고, 정제한 다음 다시 Kafka로 downstream에 넣거나 파일로 쓸 수 있습니다.
* `to_avro()` 은 구조체(struct)를 Avro 레코드로 바꾸는데 사용할 수 있습니다. 이 방법은 데이터를 Kafka로 쓸 때 여러 컬럼을 하나의 컬럼으로 다시 인코딩하고 싶은 경우 특히 유용합니다.

두 함수는 현재 Scala와 Java에서만 쓸 수 있습니다.

<div class="codetabs">
<div data-lang="scala" markdown="1">
{% highlight scala %}
import org.apache.spark.sql.avro._

// `from_avro` 는 JSON string 형식으로 된 Avro 스키마를 필요로 합니다.
val jsonFormatSchema = new String(Files.readAllBytes(Paths.get("./examples/src/main/resources/user.avsc")))

val df = spark
  .readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "host1:port1,host2:port2")
  .option("subscribe", "topic1")
  .load()

// 1. Avro data를 구조체(struct)로 디코딩합니다;
// 2. 컬럼 `favorite_color`로 필터링합니다;
// 3. 컬럼 `name`을 Avro 형식으로 인코딩합니다.
val output = df
  .select(from_avro('value, jsonFormatSchema) as 'user)
  .where("user.favorite_color == \"red\"")
  .select(to_avro($"user.name") as 'value)

val query = output
  .writeStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "host1:port1,host2:port2")
  .option("topic", "topic2")
  .start()

{% endhighlight %}
</div>
</div>

## 데이터 소스 옵션

Avro의 데이터 소스 옵션은 `DataFrameReader` 이나 `DataFrameWriter` 에 있는 `.option `메소드를 이용하여 설정할 수 있습니다.
<table class="table">
  <tr><th><b>속성 이름</b></th><th><b>기본값</b></th><th><b>의미</b></th><th><b>적용 범위</b></th></tr>
  <tr>
    <td><code>avroSchema</code></td>
    <td>(없음)</td>
    <td>사용자가 JSON 형식으로 지정하는 Avro 스키마입니다(선택). 레코드 필드의 날짜 타입과 이름은 입력된 Avro 데이터나 Catalyst 데이터와 일치 해야 합니다. 그렇지 않을 경우 읽기/쓰기 작업이 실패합니다</td>
    <td>읽기, 쓰기</td>
  </tr>
  <tr>
    <td><code>recordName</code></td>
    <td>topLevelRecord</td>
    <td>Avro 스펙에서 요구하는 쓰기 결과의 최상위 레코드 이름.</td>
    <td>쓰기</td>
  </tr>
  <tr>
    <td><code>recordNamespace</code></td>
    <td>""</td>
    <td>쓰기 결과의 레코드 네임 스페이스(namespace).</td>
    <td>쓰기</td>
  </tr>
  <tr>
    <td><code>ignoreExtension</code></td>
    <td>true</td>
    <td>이 옵션은 읽기에서 <code>.avro</code> 확장자가 없는 파일을 무시할지를 결정합니다.<br> 이 옵션이 활성화되면 모든 파일(<code>.avro</code> 확장자가 있는 파일과 없는 파일 모두)을 불러옵니다.</td>
    <td>읽기</td>
  </tr>
  <tr>
    <td><code>compression</code></td>
    <td>snappy</td>
    <td><code>compression</code> 옵션은 쓰기에 사용되는 압축 코덱을 지정하도록 합니다.<br>
  현재 지원되는 코덱은 <code>uncompressed</code>, <code>snappy</code>, <code>deflate</code>, <code>bzip2</code> 와 <code>xz</code> 입니다.<br> 옵션이 설정되어 있지 않다면, 설정값 <code>spark.sql.avro.compression.codec</code> 이 적용됩니다.</td>
    <td>쓰기</td>
  </tr>
</table>

## 설정
Avro의 설정은 SparkSession의 `setConf` 메소드를 이용하거나 SQL로  `SET key=value `명령을 실행해 구성할 수 있습니다.
<table class="table">
  <tr><th><b>속성 이름</b></th><th><b>기본값</b></th><th><b>의미</b></th></tr>
  <tr>
    <td>spark.sql.legacy.replaceDatabricksSparkAvro.enabled</td>
    <td>true</td>
    <td>true로 설정되면, 데이터 소스 제공자 <code>com.databricks.spark.avro</code> 는 하위 호환성을 위해 내장된 외부 모듈인 Avro 데이터 소스 모듈에 매핑됩니다.</td>
  </tr>
  <tr>
    <td>spark.sql.avro.compression.codec</td>
    <td>snappy</td>
    <td>AVRO 파일을 쓰는데 사용되는 압축 코덱. 지원 코덱: uncompressed, deflate, snappy, bzip2 and xz. 기본 코덱은 snappy입니다.</td>
  </tr>
  <tr>
    <td>spark.sql.avro.deflate.level</td>
    <td>-1</td>
    <td>AVRO 파일을 쓰는데 사용되는 deflate 코덱의 압축 레벨입니다. 유효한 값은 1 이상 9 이하 또는 -1 이여야 합니다. 기본값은 -1로 현재 구현에서는 6 레벨에 해당합니다. (역자 주: gzip 등에 사용되는 deflate 압축 코덱은 1 부터 9까지의 압축 레벨을 가지며, -1로 지정될 경우에는 현재 사용중인 구현체의 기본값을 사용한다. 그리고 스파크 2.4 기준으로 그 '기본값'이 6이다.)</td>
  </tr>
</table>

## Databricks spark-avro와의 호환성
이 Avro 데이터 소스 모듈은 원래 Databricks가 제작하여 독립된 오픈 소스 저장소를 통해 공개된 모듈인 https://github.com/databricks/spark-avro에서 비롯되었으며, 자연히 이 모듈과 호환됩니다. 여기서는 2.4 이전부터 spark-avro를 사용해 온 경우 호환성을 유지하기 위한 방법에 대해 설명합니다.

SQL 설정 `spark.sql.legacy.replaceDatabricksSparkAvro.enabled` 은 켜져 있도록 기본값이 잡혀 있습니다. 그리고 이 데이터 소스 제공자 `com.databricks.spark.avro` 는 내장된 Avro 모듈에 매핑되도록 구현되어 있습니다. 카탈로그 메타 스토어에 Provider 속성이 `com.databricks.spark.avro` 로 잡혀 있는 스파크 테이블의 경우, 내장 Avro 모듈을 사용하고 있다면 이 테이블을 불러오기 위한 매핑이 필수입니다.

Databricks의 spark-avro에서 implicit class인 `AvroDataFrameWriter` 와 `AvroDataFrameReader` 는 `.avro()`라는 단축 함수를 위해 만들어졌습니다. 이 내장된 외부 모듈에서, 두 implicit class는 삭제됩니다. 대신 `DataFrameWriter` 이나 `DataFrameReader` 의 `.format("avro")` 를 사용할 수 있습니다.

여러분이 직접 빌드한 `spark-avro` jar 파일을 사용하고 싶다면,  간단하게 `spark.sql.legacy.replaceDatabricksSparkAvro.enabled `설정을 비활성화 하고 애플리케이션을 배포할 때 `--jars` 를 이용하면 됩니다. 자세한 내용은 [애플리케이션 제출 가이드의 고급 의존성 관리](https://spark.apache.org/docs/latest/submitting-applications.html#advanced-dependency-management) 섹션을 참고하세요.

## 지원되는 Avro -> Spark SQL 변환 타입
현재 스파크는 Avro 레코드의 모든 기본 타입 및 복합 타입을 읽을 수 있습니다.
<table class="table">
  <tr><th><b>Avro 타입</b></th><th><b>스파크 SQL 타입</b></th></tr>
  <tr>
    <td>boolean</td>
    <td>BooleanType</td>
  </tr>
  <tr>
    <td>int</td>
    <td>IntegerType</td>
  </tr>
  <tr>
    <td>long</td>
    <td>LongType</td>
  </tr>
  <tr>
    <td>float</td>
    <td>FloatType</td>
  </tr>
  <tr>
    <td>double</td>
    <td>DoubleType</td>
  </tr>
  <tr>
    <td>string</td>
    <td>StringType</td>
  </tr>
  <tr>
    <td>enum</td>
    <td>StringType</td>
  </tr>
  <tr>
    <td>fixed</td>
    <td>BinaryType</td>
  </tr>
  <tr>
    <td>bytes</td>
    <td>BinaryType</td>
  </tr>
  <tr>
    <td>record</td>
    <td>StructType</td>
  </tr>
  <tr>
    <td>array</td>
    <td>ArrayType</td>
  </tr>
  <tr>
    <td>map</td>
    <td>MapType</td>
  </tr>
  <tr>
    <td>union</td>
    <td>See below</td>
  </tr>
</table>

위에 나열된 타입 이외에도 `union` 타입을 읽는 것을 지원합니다. 다음의 세 타입은 기본 `union `타입으로 간주됩니다:

1. `union(int, long)` 은 LongType에 매핑됩니다.
2. `union(float, double)` 은 DoubleType에 매핑됩니다.
3. `union(something, null)`(여기서 something은 모든 지원되는 Avro 타입입니다)은 같은 nullable 설정이 true로 설정된 something의 스파크 SQL 타입에 매핑됩니다. 이 외의 모든 union 타입은 복합 타입으로 간주됩니다. 이는 StructType에 매핑되며 필드 이름은 union 멤버의 이름에 따라 member0, member1, ... 와 같이 정해집니다. 이는 Avro와 Parquet 사이의 변환 동작과 같습니다.

다음과 같이 Avro 논리 타입을 읽는 것도 지원합니다.

<table class="table">
  <tr><th><b>Avro 논리 타입</b></th><th><b>Avro 타입</b></th><th><b>스파크 SQL 타입</b></th></tr>
  <tr>
    <td>date</td>
    <td>int</td>
    <td>DateType</td>
  </tr>
  <tr>
    <td>timestamp-millis</td>
    <td>long</td>
    <td>TimestampType</td>
  </tr>
  <tr>
    <td>timestamp-micros</td>
    <td>long</td>
    <td>TimestampType</td>
  </tr>
  <tr>
    <td>decimal</td>
    <td>fixed</td>
    <td>DecimalType</td>
  </tr>
  <tr>
    <td>decimal</td>
    <td>bytes</td>
    <td>DecimalType</td>
  </tr>
</table>
현재 버전에서 Avro 파일에 정의되어 있는 docs, aliases 그리고 기타 다른 속성들은 모두 무시됩니다.

## 지원되는 Spark SQL -> Avro 변환 타입
스파크는 모든 스파크 SQL 타입을 Avro로 쓰는 것을 지원합니다. 대부분의 경우 각각의 스파크 타입에서 Avro 타입으로의 변환은 직관적입니다만 (예. IntegerType을 int로 변환), 아래 목록과 같이 몇 가지 특별한 경우가 존재합니다.

<table class="table">
<tr><th><b>Spark SQL type</b></th><th><b>Avro 타입</b></th><th><b>Avro 논리 타입</b></th></tr>
  <tr>
    <td>ByteType</td>
    <td>int</td>
    <td></td>
  </tr>
  <tr>
    <td>ShortType</td>
    <td>int</td>
    <td></td>
  </tr>
  <tr>
    <td>BinaryType</td>
    <td>bytes</td>
    <td></td>
  </tr>
  <tr>
    <td>DateType</td>
    <td>int</td>
    <td>date</td>
  </tr>
  <tr>
    <td>TimestampType</td>
    <td>long</td>
    <td>timestamp-micros</td>
  </tr>
  <tr>
    <td>DecimalType</td>
    <td>fixed</td>
    <td>decimal</td>
  </tr>
</table>

스파크 SQL 타입이 Avro 타입으로 변환될 수 있도록 `avroSchema` 옵션을 사용하여 전체 출력 Avro 스키마를 지정할 수도 있습니다. 아래 타입들은 기본값이 적용되지 않기 때문에, 사용자가 반드시 지정해 줘야 합니다.

<table class="table">
  <tr><th><b>Spark SQL type</b></th><th><b>Avro type</b></th><th><b>Avro logical type</b></th></tr>
  <tr>
    <td>BinaryType</td>
    <td>fixed</td>
    <td></td>
  </tr>
  <tr>
    <td>StringType</td>
    <td>enum</td>
    <td></td>
  </tr>
  <tr>
    <td>TimestampType</td>
    <td>long</td>
    <td>timestamp-millis</td>
  </tr>
  <tr>
    <td>DecimalType</td>
    <td>bytes</td>
    <td>decimal</td>
  </tr>
</table>
