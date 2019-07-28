---
layout: global
title: 시작하기
displayTitle: 시작하기
---

* Table of contents
{:toc}

## 시작점: SparkSession

<div class="codetabs">
<div data-lang="scala"  markdown="1">

스파크의 모든 기능은 [`SparkSession`](api/scala/index.html#org.apache.spark.sql.SparkSession) 클래스에서 시작합니다. `SparkSession.builder()`를 사용해서 가장 기본적인 설정의 `SparkSession`을 생성합니다:

{% include_example init_session scala/org/apache/spark/examples/sql/SparkSQLExample.scala %}
</div>

<div data-lang="python"  markdown="1">

스파크의 모든 기능은 [`SparkSession`](api/python/pyspark.sql.html#pyspark.sql.SparkSession) 클래스에서 시작합니다. `SparkSession.builder`를 사용해서 가장 기본적인 설정의 `SparkSession`을 생성합니다:

{% include_example init_session python/sql/basic.py %}
</div>
</div>

스파크 2.0의 `SparkSession`에는 HiveQL을 사용한 쓰기 쿼리, Hive UDF 접근, Hive 테이블에서 데이터 읽기와 같은 Hive 기능이 내장되어 있습니다. 따라서 이 기능을 사용하기 위해서 Hive를 따로 설정하지 않아도 됩니다.

## DataFrame 생성하기

<div class="codetabs">
<div data-lang="scala"  markdown="1">
`SparkSession`을 사용하면 [이미 생성된 `RDD`](#interoperating-with-rdds), Hive Table 또는 [스파크 데이터 소스](https://spark.apache.org/docs/latest/sql-data-sources.html)로부터 DataFrame을 생성할 수 있습니다.

아래 예제에서는 JSON 파일의 내용을 읽어와서 DataFrame을 생성합니다:

{% include_example create_df scala/org/apache/spark/examples/sql/SparkSQLExample.scala %}
</div>

<div data-lang="python"  markdown="1">
`SparkSession`을 사용하면 [이미 생성된 `RDD`](#interoperating-with-rdds), Hive Table 또는 [스파크 데이터 소스](sql-data-sources.html)로부터 DataFrame을 생성할 수 있습니다.

아래 예제에서는 JSON 파일의 내용을 읽어와서 DataFrame을 생성합니다:

{% include_example create_df python/sql/basic.py %}
</div>
</div>


## 타입이 없는 Dataset 동작 (또는 DataFrame 동작)

DataFrame을 사용하면 [Scala](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset), [Java](https://spark.apache.org/docs/latest/api/java/index.html?org/apache/spark/sql/Dataset.html), [Python](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame), [R](https://spark.apache.org/docs/latest/api/R/SparkDataFrame.html)에서 각 언어 특성에 맞게 데이터를 조작할 수 있습니다

위에서 언급했듯이 스파크 2.0의 DataFrame은 Scala와 Java API에서 `Row`들로 이루어진 Dataset을 말합니다. 이와 관련된 동작을 Scala/Java Dataset의 강한 타입체크 특성에서 말하는 "타입 변환"의 반대 의미로 "타입이 없는 변환"이라고 부르기도 합니다.

다음은 Dataset을 사용하여 구조화된 데이터를 처리하는 기본 예제입니다:

<div class="codetabs">
<div data-lang="scala"  markdown="1">
{% include_example untyped_ops scala/org/apache/spark/examples/sql/SparkSQLExample.scala %}

Dataset에서 사용할 수 있는 명령어의 전체 목록은 [API 문서](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset)에서 볼 수 있습니다.

Dataset에는 컬럼에 대한 간단한 참조 또는 표현뿐만 아니라 문자열 처리, 날짜 연산, 일반적인 수학 연산 등의 다양한 함수를 포함하는 라이브러리가 있습니다. 라이브러리의 전체 목록은 [DataFrame 함수 레퍼런스](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.functions$)에서 볼 수 있습니다.
</div>

<div data-lang="python"  markdown="1">
Python에서는 속성(`df.age`) 또는 인덱스(`df['age']`)로 DataFrame의 각 컬럼에 접근할 수 있습니다. 비록 속성을 사용하는 방법이 대화형 데이터 탐색에 편리하긴 하지만, 인덱스를 이용한 접근을 이용할 것을 적극 권장합니다. 속성을 사용하는 방법은 컬럼 이름이 DataFrame 클래스의 속성 이름과 겹치는 경우 문제를 일으킬 수 있는데, 추후 스파크 버전에서 DataFrame 클래스에 어떠한 새로운 속성이 추가될지 모르기 때문입니다. (이 경우, 멀쩡하게 동작하던 코드가 스파크 버전을 올린 이유 하나만으로 오동작할 수 있습니다.) 즉, 인덱스를 사용하는 방법이 좀 더 미래 지향적이고 안정적인 방법입니다.

{% include_example untyped_ops python/sql/basic.py %}
Dataset에서 사용할 수 있는 명령어의 전체 목록은 [API 문서](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame)에서 볼 수 있습니다.

Dataset에는 컬럼에 대한 간단한 참조 또는 표현뿐만 아니라 문자열 처리, 날짜 연산, 일반적인 수학 연산 등의 다양한 함수를 포함하는 라이브러리가 있습니다. 라이브러리의 전체 목록은 [DataFrame 함수 레퍼런스](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#module-pyspark.sql.functions)에서 볼 수 있습니다.

</div>

</div>

## 응용 프로그램 안에서 SQL 쿼리 실행하기

<div class="codetabs">
<div data-lang="scala"  markdown="1">
SparkSession의 `sql` 함수를 사용하면 애플리케이션 안에서 SQL 쿼리를 실행하고 `DataFrame` 형태로 결과를 반환받을 수 있습니다.

{% include_example run_sql scala/org/apache/spark/examples/sql/SparkSQLExample.scala %}
</div>

<div data-lang="python"  markdown="1">
SparkSession의 `sql` 함수를 사용하면 애플리케이션 안에서 SQL 쿼리를 실행하고 `DataFrame` 형태로 결과를 반환받을 수 있습니다.

{% include_example run_sql python/sql/basic.py %}
</div>
</div>


## 전역 임시 뷰

스파크 SQL의 임시 뷰는 기본적으로 세션 내에서만 유효합니다. 즉, 임시 뷰를 생성한 세션이 종료되면 사라집니다. 모든 세션에서 공유할 수 있는 임시 뷰를 만들고 스파크 애플리케이션을 종료하기 전까지 이것을 유지하려면, 전역 임시 뷰를 생성하여 사용해야 합니다. 전역 임시 뷰는 시스템 데이터베이스에서 `global_temp`로 저장되므로, 이를 참조하기 위해서는 여기에 맞춰서 전체 이름을 지정해 주어야 합니다. (예: `SELECT * FROM global_temp.view1`.)

<div class="codetabs">
<div data-lang="scala"  markdown="1">
{% include_example global_temp_view scala/org/apache/spark/examples/sql/SparkSQLExample.scala %}
</div>

<div data-lang="python"  markdown="1">
{% include_example global_temp_view python/sql/basic.py %}
</div>

<div data-lang="sql"  markdown="1">

{% highlight sql %}

CREATE GLOBAL TEMPORARY VIEW temp_view AS SELECT a + 1, b * 2 FROM tbl

SELECT * FROM global_temp.temp_view

{% endhighlight %}

</div>
</div>


## Dataset 생성하기

Dataset은 RDD와 비슷하지만, 네트워크 상에서의 전달 및 처리에 필요한 객체 직렬화를 위해 Java 직렬화 또는 Kryo를 사용하는 대신 특수한 [인코더(Encoder)](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Encoder)를 사용합니다. 이 인코더와 표준 직렬화는 모두 객체를 바이트 뭉치로 변환한다는 점에서는 같지만, 인코더는 동적으로 생성될 뿐만 아니라 바이트 뭉치 전체를 객체로 역직렬화 시킬 필요 없이 (즉, 필요한 필드에 대해서만 객체로 역직렬화함으로써 불필요한 자원 낭비를 하지 않고) 필터링, 정렬, 해싱과 같은 다양한 동작을 수행할 수 있도록 해 주는 특수한 형식을 사용합니다.

<div class="codetabs">
<div data-lang="scala"  markdown="1">
{% include_example create_ds scala/org/apache/spark/examples/sql/SparkSQLExample.scala %}
</div>
</div>

## RDD 연동하기

Spark SQL은 RDD를 Dataset으로 변환하기 위해 두 가지 방법을 지원합니다. 첫 번째 방법은 리플렉션을 사용하여 특정 타입 객체를 담고 있는 RDD에 해당하는 스키마를 자동으로 추론하는 것입니다. 이 리플렉션 기반의 방법을 사용하면 훨씬 간결한 코드를 쓸 수 있으며, 스파크 애플리케이션 개발시 스키마를 이미 알고 있는 경우라면 매우 잘 동작할 것입니다.

Dataset을 생성하는 두 번째 방법은 프로그래밍 가능한 인터페이스를 사용하여 스키마를 명시적으로 생성한 뒤 이를 RDD에 적용하는 방법입니다. 이 방법을 사용하면 코드는 길어지겠지만, 코드가 실행되기 전 각 컬럼과 그 타입을 모르는 경우에도 Dataset을 구성할 수 있습니다.

### 리플렉션(Reflection)을 사용한 스키마 유추
<div class="codetabs">

<div data-lang="scala"  markdown="1">

Spark SQL의 Scala 인터페이스는 자동으로 케이스 클래스가 포함된 RDD를 DataFrame으로 변환합니다. 이 때 스키마는 케이스 클래스에 따라 정의됩니다. 즉, 리플렉션을 이용하여 케이스 클래스의 파라미터 이름을 컬럼 이름으로 사용합니다. 케이스 클래스는 `Seq`나 `Array`와 같은 복합 타입 혹은 중첩된 형태의 타입도 사용할 수 있습니다. 이렇게 RDD를 DataFrame으로 변환하여 테이블에 등록할 수 있습니다. 이렇게 만들어진 테이블은 이후 SQL문에서도 사용할 수 있습니다.

{% include_example schema_inferring scala/org/apache/spark/examples/sql/SparkSQLExample.scala %}
</div>

<div data-lang="python"  markdown="1">

스파크 SQL은 Row 객체를 담고 있는 RDD에서 데이터 타입을 추론함으로써 DataFrame으로 변환할 수 있습니다. Row 객체는 키/값 쌍으로 이루어진 kwargs를 Row 클래스로 넘겨받아 생성됩니다. 이 목록에서 키가 테이블 컬럼의 이름이 됩니다. 타입은 전체 데이터셋을 샘플링하여 유추하는데, 이 과정은 JSON 파일에서 수행하는 것과 비슷하게 이루어집니다.

{% include_example schema_inferring python/sql/basic.py %}
</div>

</div>

### 프로그램적으로 스키마 명시하기

<div class="codetabs">

<div data-lang="scala"  markdown="1">

케이스 클래스가 미리 정의되지 않았을 때 (예를 들어, 레코드의 구조가 특정 문자열로 인코딩되어 있거나 텍스트 dataset이 사용자에 따라 서로 다르게 파싱되어 각 유저마다 필드값이 다르게 보이는 경우), 프로그램 내에서 세 단계를 거쳐 `DataFrame`을 생성할 수 있습니다.

1. 기존의 RDD에서 `RowS` 객체의 RDD를 생성합니다;
2. 1단계에서 생성한 `Row`s 객체의 RDD 구조와 일치하는 `StructType`으로 스키마를 생성합니다.
3. `SparkSession`의 `createDataFrame` 메소드를 사용하여 `RowS`객체의 RDD에 이 스키마를 적용합니다.

예:

{% include_example programmatic_schema scala/org/apache/spark/examples/sql/SparkSQLExample.scala %}
</div>

<div data-lang="python"  markdown="1">

kwargs의 구조를 미리 정의할 수 없을 때 (예를 들어, 레코드의 구조가 특정 문자열로 인코딩되어 있거나 텍스트 Dataset이 사용자에 따라 서로 다르게 파싱되어 각 유저마다 필드값이 다르게 보이는 경우), `DataFrame`을 프로그램 내에서 세 단계를 거쳐 생성할 수 있습니다.

1. 기존의 RDD에서 튜플 또는 리스트로 이루어진 RDD를 생성합니다;
2. 1단계에서 생성한 RDD의 튜플 또는 리스트 구조와 일치하는 `StructType`으로 나타낸 스키마를 생성합니다.
3. `SparkSession`의 `createDataFrame` 메소드를 사용하여 RDD에 이 스키마를 적용합니다.

예:

{% include_example programmatic_schema python/sql/basic.py %}
</div>

</div>

## 집계(Aggregations)

[내장 DataFrames 함수](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.functions$)는 `count()`, `countDistinct()`, `avg()`, `max()`, `min()`와 같은 집계 함수를 제공합니다. 이 함수들은 DataFrame에서 사용할 수 있도록 만들어졌지만, 이들 중 일부는 [Scala](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.expressions.scalalang.typed$)의 (강한 타입체크를 수행하는) Dataset에서 사용할 수 있는 타입 안전(type-safe) 버전이 있습니다. 또한, 사용자는 내장된 집계 함수 뿐만 아니라 자기만의 집계 함수를 생성할 수도 있습니다.

### 타입이 없는 사용자 정의 집계 함수
사용자는 [UserDefinedAggregateFunction](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.expressions.UserDefinedAggregateFunction) 클래스를 확장하여 타입이 없는 사용자 정의 집계 함수를 구현할 수 있습니다. 예를 들어, 사용자 정의 평균 함수는 아래 예제와 같이 구현할 수 있습니다:

<div class="codetabs">
<div data-lang="scala"  markdown="1">
{% include_example untyped_custom_aggregation scala/org/apache/spark/examples/sql/UserDefinedUntypedAggregation.scala%}
</div>
</div>

### 타입 안전(Type-safe) 사용자 정의 집계 함수

강한 타입 체크를 사용하는 Dataset에서 사용자 정의 집계 함수는 [Aggregator](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.expressions.Aggregator) 클래스를 이용해야 합니다. 타입 안전 사용자 정의 평균 함수는 아래 예제와 같이 구현합니다:

<div class="codetabs">
<div data-lang="scala"  markdown="1">
{% include_example typed_custom_aggregation scala/org/apache/spark/examples/sql/UserDefinedTypedAggregation.scala%}
</div>
</div>
