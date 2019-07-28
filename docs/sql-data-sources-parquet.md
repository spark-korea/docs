---
layout: global
title: Parquet 파일
displayTitle: Parquet 파일
---

* Table of contents
{:toc}

[Parquet('파케이')](http://parquet.io)는 다양한 데이터 처리 시스템에서 사용하는 컬럼 기반 형식입니다. 스파크 SQL은 자동으로 기존 데이터의 스키마를 유지하는 Parquet 파일의 읽기와 쓰기를 지원합니다. Parquet 파일을 쓸 때, 모든 컬럼은 호환성을 위해 자동으로 null을 허용하도록 변경됩니다.

### 프로그램에서 데이터 불러오기

주: 위 예제에서의 데이터를 사용합니다.

<div class="codetabs">

<div data-lang="scala"  markdown="1">
{% include_example basic_parquet_example scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala %}
</div>

<div data-lang="python"  markdown="1">

{% include_example basic_parquet_example python/sql/datasource.py %}
</div>

<div data-lang="sql"  markdown="1">

{% highlight sql %}

CREATE TEMPORARY VIEW parquetTable
USING org.apache.spark.sql.parquet
OPTIONS (
  path "examples/src/main/resources/people.parquet"
)

SELECT * FROM parquetTable

{% endhighlight %}

</div>

</div>

### 파티션(Partition) 탐색

테이블의 내용을 일정한 형태로 분할해서 저장하는 테이블 파티셔닝은 Hive와 같은 시스템에서 일반적으로 사용되는 최적화 방법입니다. 분할된 테이블에서 각 데이터는 일반적으로 다른 디렉토리에 저장되며 각 분할 디렉토리의 경로는 분할 컬럼의 값으로 인코딩됩니다. 모든 내장 파일 소스(Text/CSV/JSON/ORC/Parquet)는 자동으로 분할 정보를 탐색하거나 유추합니다. 예를 들어 우리가 이전에 사용했던 인구 데이터를 아래의 디렉토리 구조를 따라 분할된 테이블로 저장할 수 있습니다. `gender`와 `country는` 별도의 두 분할 컬럼으로 사용할 수 있습니다:

{% highlight text %}

path
└── to
    └── table
        ├── gender=male
        │   ├── ...
        │   │
        │   ├── country=US
        │   │   └── data.parquet
        │   ├── country=CN
        │   │   └── data.parquet
        │   └── ...
        └── gender=female
            ├── ...
            │
            ├── country=US
            │   └── data.parquet
            ├── country=CN
            │   └── data.parquet
            └── ...

{% endhighlight %}

`SparkSession.read.parquet` 또는 `SparkSession.read.load`에 `path/to/table`을 넣어주면 스파크 SQL은 자동으로 해당 경로를 통해 분할 정보를 추출합니다. 반환되는 DataFrame의 스키마는 다음과 같습니다:

{% highlight text %}

root
|-- name: string (nullable = true)
|-- age: long (nullable = true)
|-- gender: string (nullable = true)
|-- country: string (nullable = true)

{% endhighlight %}

파티션 컬럼의 데이터 타입은 자동으로 추론된다는 점을 명심하시기 바랍니다. 현재 날짜, 시간, 숫자 타입, 문자열 타입이 지원됩니다. 자동 데이터 타입 추론을 것을 원치 않을 경우에는 `spark.sql.sources.partitionColumnTypeInference.enabled` 설정값을 바꿔 주면 됩니다. (기본값: true.) 자동 타입 유추가 비활성화되면 파티션 컬럼은 문자열 타입으로 간주됩니다.

스파크 1.6.0 버전부터, 파티션 탐색은 기본적으로 주어진 경로의 파티션만 구별해냅니다. 위의 예제에서, `SparkSession.read.parquet`나 `SparkSession.read.load`에 `genderpath/to/table/gender=male`를 입력하면 파티션 컬럼은 적용되지 않습니다. 만약 사용자가 분할 탐색을 시작할 경로를 명시해야 한다면 데이터 소스 옵션에서 `basePath`를 설정할 수 있습니다. 예를 들어 데이터 경로가 `path/to/table/gender=male`인 경우 사용자는 `basePath`를 `path/to/table/`으로 설정하면 `gender`가 분할 컬럼이 됩니다.

### 스키마 병합

Protocol Buffer, Avro 그리고 Thrift와 마찬가지로, Parquet 또한 스키마를 변경할 수 있습니다. 사용자는 간단한 스키마로 시작하여 필요한 경우 스키마에 컬럼을 더 추가할 수 있습니다. 이것을 위해서 사용자는 서로 호환할 수 있는 스키마를 가진 여러 개의 다른 Parquet 파일을 사용할 수 있습니다. Parquet 데이터 소스는 이러한 파일을 자동으로 감지하고 스키마를 병합합니다.

스키마 병합은 상대적으로 고비용의 연산이기 때문에 대부분의 경우 필수적이진 않습니다. 1.5.0 버전부터는 이 기능은 기본적으로 비활성화되어있습니다. 이 기능을 활성화시키기 위해서는

1. (아래의 예제와 같이) Parquet 파일을 읽어올 때 데이터 소스의 옵션 `mergeSchema`을 `true`로 설정하거나,
2. 전역 SQL 옵션 `spark.sql.parquet.mergeSchema`을 `true`로 설정합니다.

<div class="codetabs">

<div data-lang="scala"  markdown="1">
{% include_example schema_merging scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala %}
</div>

<div data-lang="python"  markdown="1">

{% include_example schema_merging python/sql/datasource.py %}
</div>

</div>

### Hive 메타스토어의 Parquet 테이블 변환

Hive 메타스토어의 Parquet 테이블을 읽거나 쓸 때, 스파크 SQL은 Hive SerDe를 사용하는 것보다 더 나은 성능을 위하여 자체적으로 포함된 Parquet 기능을 사용합니다. 이 기능은 기본적으로 활성화되어 있으며 `spark.sql.hive.convertMetastoreParquet`에서 설정할 수 있습니다.

#### Hive/Parquet 스키마 재조합

테이블 스키마 처리의 관점에서 Hive와 Parquet 사이에는 두 가지 중요한 차이점이 있습니다.

1. Hive는 대소문자를 구분하지 않지만, Parquet는 구분합니다.
2. Hive는 모든 컬럼이 null 값을 가질 수 있지만 Parquet에서는 null 값을 가질 수도있고 그렇지 않을 수도 있습니다.

이러한 이유 때문에 Hive 메타스토어의 Parque 테이블을 스파크 SQL의 Parquet 테이블로 변환할 때 Hive 메타스토어 스키마를 Parquet 스키마와 적절하게 조합해야 합니다. 조합 규칙은 다음과 같습니다:

1. 두 스키마에서 동일한 이름을 가지는 필드는 null 값을 가질 수 있는지에 상관없이 항상 동일한 데이터 타입을 가져야 합니다. 조합된 필드는 Parquet의 데이터 타입을 가져야 하고 null 값을 가질 수 있어야 합니다.

2. 조합된 스키마는 Hive 메타스토어에서 정의된 필드만을 포함해야 합니다.

   - Parquet 스키마에서만 존재했던 필드는 재조합된 스키마에서는 삭제됩니다.
   - Hive 메타스토어에서만 존재했던 필드는 조합된 스키마에 null 값을 가질 수 있는 필드로 추가됩니다.

#### 메타데이터 갱신

스파크 SQL은 성능 향상을 위해 Parquet 메타데이터를 캐시합니다. Hive 메타스토어 Parquet 테이블의 변환이 활성화되어 있을 때, 이 변환된 테이블의 메타데이터 또한 캐시됩니다. 이 테이블이 Hive나 다른 외부의 도구에 의해 업데이트되면, 이를 수동으로 새로고침하여 메타데이터를 일관되게 유지해야 합니다.

<div class="codetabs">

<div data-lang="scala"  markdown="1">

{% highlight scala %}
// spark는 이미 존재하는 SparkSession입니다.
spark.catalog.refreshTable("my_table")
{% endhighlight %}

</div>

<div data-lang="python"  markdown="1">

{% highlight python %}
# spark는 이미 존재하는 SparkSession입니다
{% endhighlight %}

</div>

<div data-lang="sql"  markdown="1">

{% highlight sql %}
REFRESH TABLE my_table;
{% endhighlight %}

</div>

</div>

### 설정

Parquet 설정은 `SparkSession`에서` setConf` 메소드를 사용하거나 SQL에서 `SET key=value` 명령어를 실행하여 설정할 수 있습니다.

<table class="table">
<tr><th>속성 이름</th><th>기본값</th><th>의미</th></tr>
<tr>
  <td><code>spark.sql.parquet.binaryAsString</code></td>
  <td>false</td>
  <td>
    Impala, Hive, 구버전의 스파크 SQL과 같이 Parquet를 생성하는 몇몇 시스템에서는 Parquet 스키마를 쓸 때 바이너리 데이터와 문자열을 구분하지 않습니다. 이 플래그는 스파크 SQL이 바이너리 데이터를 문자열로 인식하도록 하는 호환성을 의미합니다.
  </td>
</tr>
<tr>
  <td><code>spark.sql.parquet.int96AsTimestamp</code></td>
  <td>true</td>
  <td>
    Impala, Hive와 같이 Parquet를 생성하는 시스템에서는 타임스탬프를 INT96으로 저장합니다. 이 플래그는 스파크 SQL이 INT96 데이터를 timestamp로 인식하도록 하는 호환성을 의미합니다.
  </td>
</tr>
<tr>
  <td><code>spark.sql.parquet.compression.codec</code></td>
  <td>snappy</td>
  <td>
    Parquet 파일을 쓸 때 사용할 압축 코덱을 설정합니다. 테이블 옵션/속성에 `compression` 또는 `parquet.compression` 속성이 이미 명시되어 있다면, 우선순위는 `compression`, `parquet.compression`, `spark.sql.parquet.compression.codec`순이 됩니다. 지원 가능한 코덱은 다음과 같습니다: none, uncompressed, snappy, gzip, lzo, brotli, lz4, zstd.
    Hadoop 2.9.0 이하 버전에서는 `zstd`를 사용하기 위해서는 `ZStandardCodec`를 설치해야 합니다. `brotli`를 사용하기 위해서는 `BrotliCodec`를 설치해야 합니다.
  </td>
</tr>
<tr>
  <td><code>spark.sql.parquet.filterPushdown</code></td>
  <td>true</td>
  <td>true로 설정되었을 때, Parquet 필터 푸쉬다운 최적화를 활성화합니다.</td>
</tr>
<tr>
  <td><code>spark.sql.hive.convertMetastoreParquet</code></td>
  <td>true</td>
  <td>
    false로 설정되었을 때, 스파크 SQL은 parquet 테이블을 다룰 때 내장된 기능 대신 Hive SerDe를 사용합니다.
  </td>
</tr>
<tr>
  <td><code>spark.sql.parquet.mergeSchema</code></td>
  <td>false</td>
  <td>
    <p>
      true로 설정되었을 때, Parquet 데이터 소스는 모든 데이터 파일의 스키마를 병합합니다. false로 설정되었을 때는 요약 파일에서 요약된 파일이 없는 경우 임의로 데이터 파일로부터, 스키마를 생성합니다.
    </p>
  </td>
</tr>
<tr>
  <td><code>spark.sql.parquet.writeLegacyFormat</code></td>
  <td>false</td>
  <td>
    true로 설정되었을 때, 데이터는 Spark 1.4 이하 버전에서처럼 쓰여집니다. 예를 들어 decimal 값은 아파치 Hive와 Impala와 마찬가지로 아파치 Parquet의 고정 길이 바이트 배열 형식으로 쓰여집니다. false로 설정되면 Parquet의 새로운 형식이 사용됩니다. 예를 들어 decimal는 정수 기반 형식으로 쓰여집니다. 만약 Parquet 출력값이 새로운 형식을 사용하지 않도록 하려면 true로 설정하여야 합니다.
  </td>
</tr>
</table>
