---
layout: global
displayTitle: 스파크 SQL, DataFrame, Dataset
title: 스파크 SQL, DataFrame, Dataset
---

스파크 SQL은 구조화된 데이터 처리를 위한 스파크 모듈입니다. 기본 스파크 RDD API와는 다르게, 스파크 SQL이 제공하는 인터페이스는 데이터의 구조와 계산 과정의 구조에 대한 정보를 더 많이 포함하고 있습니다. 내부적으로, 스파크 SQL은 내부에서 별도의 정보를 이용해 최적화를 수행합니다. Dataset API와 SQL을 포함하고 있는 스파크 SQL의 사용법은 다양합니다. 동일한 실행 엔진을 사용한다면 계산되는 결과는 어떤 API나 프로그래밍 언어를 사용하는지에 상관 없이 동일합니다. 이것이 의미하는 것은 개발자가 필요한 변환을 가장 자연스럽게 표현하기 위해서 적절한 API를 유연하게 사용할 수 있다는 것입니다.

여기에서 소개할 예제들은 스파크가 제공하는 예제 데이터를 사용합니다. 이 예제들은 `spark-shell`, `pyspark` 셸, `sparkR` 셸에서 실행할 수 있습니다.


## SQL

스파크 SQL을 사용하는 방법 중 하나는 SQL 쿼리를 실행하는 것입니다. 스파크 SQL을 사용하여 이미 설치되어 있는 Hive에서 데이터를 읽어올 수도 있습니다. 이 기능에 대해 더 자세히 알고 싶다면 [Hive Tables](sql-data-sources-hive-tables.html)에서 자세한 내용을 볼 수 있습니다. 이와 다른 프로그래밍 언어에서 SQL을 실행하면 [Dataset/DataFrame](sql-programming-guide.html#datasets-and-dataframes)으로 된 결과를 얻게 됩니다. [명령어](sql-distributed-sql-engine.html#running-the-spark-sql-cli)를 사용하거나 [JDBC/ODBC](sql-distributed-sql-engine.html#running-the-thrift-jdbcodbc-server)를 통해 SQL 인터페이스를 활용할 수도 있습니다.

## Dataset과 DataFrame

Dataset은 1개 이상의 컴퓨팅 장치에 분산되어 저장된 데이터의 집합입니다. Dataset은 스파크 1.6에서 새롭게 추가된 인터페이스이며, RDD의 장점(강한 타입 체크, 람다 함수의 사용)과 스파크 SQL의 최적화된 실행 엔진의 장점을 갖고 있습니다. JVM 객체를 이용해 Dataset을 [생성](sql-getting-started.html#creating-datasets)하고 함수형 변환(`map`, `flatMap`, `filter`)으로 조작할 수 있습니다. Dataset API는 [Scala](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset) 와 [Java](https://spark.apache.org/docs/latest/api/java/index.html?org/apache/spark/sql/Dataset.html)에서 사용가능합니다. Python은 Dataset API를 지원되지 않습니다. 하지만 Python에서는 Python의 동적 특성때문에 Dataset API의 많은 장점들을 이미 사용할 수 있습니다(예: `row.columnName`를 사용해서 각 컬럼의 특정 필드에 접근할 수 있습니다). R의 경우에도 Python과 비슷합니다.

DataFrame은 Dataset에서 각 컬럼에 이름을 붙여 만들어진 형태입니다. DataFrame은 관계형 데이터 베이스의 테이블, 또는 R이나 Python의 데이터 프레임과 같은 개념이지만 이들보다 더 최적화되어 있습니다. DataFrame은 다음과 같은 다양한 [데이터 소스](sql-data-sources.html)로부터 만들어 낼 수 있습니다: 구조화된 데이터 파일, Hive 테이블, 외부 데이터베이스, 기존의 RDD. DataFrame API는 Scala, Java, [Python](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame), [R](https://spark.apache.org/docs/latest/api/R/index.html)에서 사용할 수 있습니다. Scala와 Java에서는 DataFrame을 Row 객체로 이루어진 Dataset으로 표현합니다. [Scala API](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset)에서는 DataFrame의 타입을 Dataset[Row]으로 지정하여 사용할 수 있습니다. [Java API](https://spark.apache.org/docs/latest/api/java/index.html?org/apache/spark/sql/Dataset.html)에서는 DataFrame을 표현하려면 Dataset<Row>의 형태를 사용해야 합니다.

[scala-datasets]: api/scala/index.html#org.apache.spark.sql.Dataset
[java-datasets]: api/java/index.html?org/apache/spark/sql/Dataset.html

이 문서에서는 Row객체로 이루어진 Scala/Java의 Dataset을 DataFrame으로 간주하도록 하겠습니다.
