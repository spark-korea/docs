---
layout: global
title: Getting Started
displayTitle: Getting Started
---


# **시작하기**



*   시작점: SparkSession

*   타입이 없는 Dataset 동작(또는 DataFrame 동작)
*   프로그램 내에서 SQL 쿼리 실행하기<
*   전역 임시 뷰
* Dataset 생성하기


* RDD 인터폴레이션
    *   리플렉션(Reflection)을 사용한 스키마 유추
    *   프로그램 내에서 스키마 명시하기<
*   집계
    *   타입이 없는 사용자 정의 집약 함수
    *   타입 안정(Type-Safe) 사용자 정의 집약 함수]


## **시작점: SparkSession**



*   **Scala**

스파크의 모든 기능은 <code>[SparkSession](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.SparkSession)</code> 클래스에서 시작합니다. <code>SparkSession.builder()</code>를 사용해서 가장 기본적인 설정의 <code>SparkSession</code>을 생성합니다:


```
import org.apache.spark.sql.SparkSession

val spark = SparkSession
  .builder()
  .appName("Spark SQL basic example")
  .config("spark.some.config.option", "some-value")
  .getOrCreate()

// For implicit conversions like converting RDDs to DataFrames
// RDD를 DataFrame으로 바꾸는 것과 같은 암시적(implicit) 변환
import spark.implicits._
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SparkSQLExample.scala"에서 전체 예제 코드를 볼 수 있습니다

스파크 2.0의 `SparkSession`에는 HiveQL을 사용한 쓰기 쿼리, Hive UDF 접근, Hive 테이블에서 데이터 읽기와 같은 Hive 기능이 내장되어 있습니다. 따라서 이 기능을 사용하기 위해서 Hive를 따로 설정하지 않아도 됩니다.



*   **Python**

스파크의 모든 기능은 <code>[SparkSession](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.SparkSession)</code> 클래스에서 시작합니다. <code>SparkSession.builder()</code>를 사용해서 가장 기본적인 설정의 <code>SparkSession</code>을 생성합니다:


```
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
```


스파크 저장소의 "examples/src/main/python/sql/basic.py”에서 전체 예제 코드를 볼 수 있습니다.

스파크 2.0의 `SparkSession`에는 HiveQL을 사용한 쓰기 쿼리, Hive UDF 접근, Hive 테이블에서 데이터 읽기와 같은 Hive 기능이 내장되어 있습니다. 따라서 이 기능을 사용하기 위해서 Hive를 따로 설정하지 않아도 됩니다.


## **DataFrame 생성하기**



*   **Scala**

`SparkSession`을 사용하면 RDD, Hive Table 또는 [스파크 데이터 소스](https://spark.apache.org/docs/latest/sql-data-sources.html)로부터 DataFrame을 생성할 수 있습니다.

아래 예제에서는 JSON 파일의 내용을 읽어와서 DataFrame을 생성합니다:

**<code>val df = spark.read.json("examples/src/main/resources/people.json") \
<em> \
// 표준출력(stdout)에 DataFrame의 내용을 보여줍니다</em> \
df.show() \
<em>// +----+-------+</em> \
<em>// | age|   name|</em> \
<em>// +----+-------+</em> \
<em>// |null|Michael|</em> \
<em>// |  30|   Andy|</em> \
<em>// |  19| Justin|</em> \
<em>// +----+-------+</em> \
</code></strong> \
스파크 저장소의  "examples/src/main/scala/org/apache/spark/examples/sql/SparkSQLExample.scala"에서 전체 예제 코드를 볼 수 있습니다.



*   **Python**

`SparkSession`을 사용하면 RDD, Hive Table 또는 [스파크 데이터 소스](https://spark.apache.org/docs/latest/sql-data-sources.html)로부터 DataFrame을 생성할 수 있습니다.

아래 예제에서는 JSON 파일의 내용을 읽어와서 DataFrame을 생성합니다:

<code><em># 여기에서 spark는 이미 생성된 SparkSession입니다</em> \
df = spark.read.json("examples/src/main/resources/people.json") \
<em># 표준출력(stdout)에 DataFrame의 내용을 보여줍니다</em> \
df.show() \
<em># +----+-------+</em> \
<em># | age|   name|</em> \
<em># +----+-------+</em> \
<em># |null|Michael|</em> \
<em># |  30|   Andy|</em> \
<em># |  19| Justin|</em> \
<em># +----+-------+</em> \
</code> \
스파크 저장소의 "examples/src/main/python/sql/basic.py”에서 전체 예제 코드를 볼 수 있습니다.


## **타입이 없는 Dataset 동작(또는 DataFrame 동작)**

DataFrame을 사용하면 [Scala](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset), [Java](https://spark.apache.org/docs/latest/api/java/index.html?org/apache/spark/sql/Dataset.html), [Python](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame), [R](https://spark.apache.org/docs/latest/api/R/SparkDataFrame.html)에서 각 언어 특성에 맞게 데이터를 조작할 수 있습니다

위에서 언급했듯이 스파크 2.0의 DataFrame은 Scala와 Java API에서 `RowS` 로 이루어진 Dataset을 말합니다. 이와 관련된 동작을 Scala/Java Dataset의 강한 타입체크 특성에서 말하는 “타입 변환"의 반대 의미로 “타입이 없는 변환"이라고 부르기도 합니다. 

다음은 Dataset을 사용하여 구조화된 데이터를 처리하는 기본 예제입니다:



*   **Scala**


```
// $-notation을 사용하기 위해 임포트합니다
import spark.implicits._
// 트리 형태로 스키마를 출력합니다
df.printSchema()
// root
// |-- age: long (nullable = true)
// |-- name: string (nullable = true)

// "name" 컬럼을 선택합니다
df.select("name").show()
// +-------+
// |   name|
// +-------+
// |Michael|
// |   Andy|
// | Justin|
// +-------+

// 모든 사람을 선택하고 나이를 1씩 증가시킵니다
df.select($"name", $"age" + 1).show()
// +-------+---------+
// |   name|(age + 1)|
// +-------+---------+
// |Michael|     null|
// |   Andy|       31|
// | Justin|       20|
// +-------+---------+

// 나이가 21살보다 많은 사람을 선택합니다
df.filter($"age" > 21).show()
// +---+----+
// |age|name|
// +---+----+
// | 30|Andy|
// +---+----+

// 각 나이에 해당하는 사람의 수를 셉니다
df.groupBy("age").count().show()
// +----+-----+
// | age|count|
// +----+-----+
// |  19|    1|
// |null|    1|
// |  30|    1|
// +----+-----+
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SparkSQLExample.scala"에서 전체 예제 코드를 볼 수 있습니다.

Dataset에서 사용할 수 있는 명령어의 전체 목록은 [API 문서](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset)에서 볼 수 있습니다.

Dataset에는 컬럼에 대한 간단한 참조 또는 표현뿐만 아니라, 문자열 처리, 날짜 연산, 일반적인 수학 연산 등의 다양한 함수를 포함하는 라이브러리가 있습니다. 라이브러리의 전체 목록은 [DataFrame 함수 레퍼런스](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.functions$)에서 볼 수 있습니다.



*   **Python**

Python에서는 속성(`df.age`) 또는 인덱스(`df['age']`)로 DataFrame의 각 컬럼에 접근할 수 있습니다. 비록 속성을 사용하는 방법이 대화형 데이터 탐색에 편리하긴 하지만, 인덱스를 이용한 접근을 이용할 것을 적극 권장합니다. 속성을 사용하는 방법은 컬럼 이름이 DataFrame 클래스의 속성 이름과 겹치는 경우 문제를 일으킬 수 있는데, 추후 스파크 버전에서 DataFrame 클래스에 어떠한 새로운 속성이 추가될지 모르기 때문입니다. (이 경우, 멀쩡하게 동작하던 코드가 스파크 버전을 올린 이유 하나만으로 오동작할 수 있습니다.) 즉, 인덱스를 사용하는 방법이 좀 더 미래 지향적이고 안정적인 방법입니다.


```
# spark와 df는 이전 예제와 동일합니다
# 트리 형태로 스키마를 출력합니다
df.printSchema()
# root
# |-- age: long (nullable = true)
# |-- name: string (nullable = true)

# "name" 컬럼을 선택합니다
df.select("name").show()
# +-------+
# |   name|
# +-------+
# |Michael|
# |   Andy|
# | Justin|
# +-------+

# 모든 사람을 선택하고 나이를 1씩 증가시킵니다
df.select(df['name'], df['age'] + 1).show()
# +-------+---------+
# |   name|(age + 1)|
# +-------+---------+
# |Michael|     null|
# |   Andy|       31|
# | Justin|       20|
# +-------+---------+

# 나이가 21살보다 많은 사람을 선택합니다
df.filter(df['age'] > 21).show()
# +---+----+
# |age|name|
# +---+----+
# | 30|Andy|
# +---+----+

# 각 나이에 해당하는 사람의 수를 셉니다
df.groupBy("age").count().show()
# +----+-----+
# | age|count|
# +----+-----+
# |  19|    1|
# |null|    1|
# |  30|    1|
# +----+-----+
```



## **프로그램 내에서 SQL 쿼리 실행하기**



*   **Scala**

SparkSession의 `sql` 함수를 사용하면 애플리케이션 프로그램내에서 SQL 쿼리를 실행하고 `DataFrame` 형태로 결과를 반환받을 수 있습니다.

<code><em>// DataFrame을 SQL 임시 뷰로 등록합니다</em> \
df.createOrReplaceTempView("people") \
 \
<strong>val</strong> sqlDF <strong>=</strong> spark.sql("SELECT * FROM people") \
sqlDF.show() \
<em>// +----+-------+</em> \
<em>// | age|   name|</em> \
<em>// +----+-------+</em> \
<em>// |null|Michael|</em> \
<em>// |  30|   Andy|</em> \
<em>// |  19| Justin|</em> \
<em>// +----+-------+</em> \
</code> \
스파크 저장소의  "examples/src/main/scala/org/apache/spark/examples/sql/SparkSQLExample.scala"에서 전체 예제 코드를 볼 수 있습니다



*   **Python**

SparkSession의 `sql` 함수를 사용하면 애플리케이션 프로그램 내에서 SQL 쿼리를 실행하고 `DataFrame` 형태로 결과를 반환받을 수 있습니다.


```
# DataFrame을 SQL 임시 뷰로 등록합니다
df.createOrReplaceTempView("people")

sqlDF = spark.sql("SELECT * FROM people")
sqlDF.show()
# +----+-------+
# | age|   name|
# +----+-------+
# |null|Michael|
# |  30|   Andy|
# |  19| Justin|
# +----+-------+
```


스파크 저장소의 "examples/src/main/python/sql/basic.py"에서 전체 예제 코드를 볼 수 있습니다


## **전역 임시 뷰**

스파크 SQL의 임시 뷰는 기본적으로 세션 내에서만 유효합니다. 즉, 임시 뷰를 생성한 세션이 종료되면 사라집니다. 모든 세션에서 공유할 수 있는 임시 뷰를 만들고 스파크 애플리케이션을 종료하기 전까지 이것을 유지하려면, 전역 임시 뷰를 생성하여 사용해야 합니다. 전역 임시 뷰는 시스템 데이터베이스에서 `global_temp`로 저장되므로, 이를 참조하기 위해서는 여기에 맞춰서 전체 이름을 지정해 주어야 합니다. 예: `SELECT * FROM global_temp.view1`.



*   **Scala**


```
// DataFrame을 전역 임시 뷰에 등록합니다
df.createGlobalTempView("people")

// 전역 임시 뷰는 시스템 데이터베이스에서 `global_temp`로 사용됩니다
spark.sql("SELECT * FROM global_temp.people").show()
// +----+-------+
// | age|   name|
// +----+-------+
// |null|Michael|
// |  30|   Andy|
// |  19| Justin|
// +----+-------+g

// 전역 임시 뷰는 다른 SparkSession에서도 사용할 수 있습니다
spark.newSession().sql("SELECT * FROM global_temp.people").show()
// +----+-------+
// | age|   name|
// +----+-------+
// |null|Michael|
// |  30|   Andy|
// |  19| Justin|
// +----+-------+
```


스파크 저장소의  "examples/src/main/scala/org/apache/spark/examples/sql/SparkSQLExample.scala"에서 전체 코드를 볼 수 있습니다



*   **Python**

<code><em># DataFrame을 전역 임시 뷰에 등록합니다</em> \
df.createGlobalTempView("people") \
 \
<em># 전역 임시 뷰는 시스템 데이터베이스에서 `global_temp`로 사용됩니다</em> \
spark.sql("SELECT * FROM global_temp.people").show() \
<em># +----+-------+</em> \
<em># | age|   name|</em> \
<em># +----+-------+</em> \
<em># |null|Michael|</em> \
<em># |  30|   Andy|</em> \
<em># |  19| Justin|</em> \
<em># +----+-------+</em> \
<em> \
# 전역 임시 뷰는 다른 SparkSession에서도 사용할 수 있습니다</em> \
spark.newSession().sql("SELECT * FROM global_temp.people").show() \
<em># +----+-------+</em> \
<em># | age|   name|</em> \
<em># +----+-------+</em> \
<em># |null|Michael|</em> \
<em># |  30|   Andy|</em> \
<em># |  19| Justin|</em> \
<em># +----+-------+</em> \
</code> \
스파크 저장소의 "examples/src/main/python/sql/basic.py"에서 전체 예제 코드를 볼 수 있습니다<strong> \
Dataset 생성하기</strong>

Dataset은 RDD와 비슷하지만, 네트워크 상에서의 전달 및 처리에 필요한 객체 직렬화를 위해 Java 직렬화 또는 Kryo를 사용하는 대신 특수한 [인코더(Encoder)](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Encoder)를 사용합니다. 이 인코더와 표준 직렬화는 모두 객체를 바이트 뭉치로 변환한다는 점에서는 같지만, 인코더는 동적으로 생성될 뿐만 아니라 바이트 뭉치 전체를 객체로 역직렬화 시킬 필요 없이 (즉, 필요한 필드에 대해서만 객체로 역직렬화함으로써 불필요한 자원 낭비를 하지 않고) 필터링, 정렬, 해싱과 같은 다양한 동작을 수행할 수 있도록 해 주는 특수한 형식을 사용합니다. 

**Scala**


```
case class Person(name: String, age: Long)

// Encoder는 케이스 클래스로 생성됩니다
val caseClassDS = Seq(Person("Andy", 32)).toDS()
caseClassDS.show()
// +----+---+
// |name|age|
// +----+---+
// |Andy| 32|
// +----+---+

// 일반적으로 사용되는 타입에 대한 인코더는 spark.implicits._를 임포트하면 자동으로 포함됩니다
val primitiveDS = Seq(1, 2, 3).toDS()
primitiveDS.map(_ + 1).collect() // Array(2, 3, 4) 반환

// 클래스를 지정하여 DataFrame을 Dataset으로 변환할 수 있습니다. 값들은 클래스의 속성 변수 이름에 따라 자동으로 할당됩니다.
val path = "examples/src/main/resources/people.json"
val peopleDS = spark.read.json(path).as[Person]
peopleDS.show()
// +----+-------+
// | age|   name|
// +----+-------+
// |null|Michael|
// |  30|   Andy|
// |  19| Justin|
// +----+-------+
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SparkSQLExample.scala"에서 전체 예제 코드를 볼 수 있습니다

** \
RDD 연동하기**

Spark SQL은 RDD를 Dataset으로 변환하기 위해 두 가지 방법을 지원합니다. 첫 번째 방법은 리플렉션을 사용하여 특정 타입 객체를 담고 있는 RDD에 해당하는 스키마를 자동으로 추론하는 것입니다. 이 리플렉션 기반의 방법을 사용하면 훨씬 간결한 코드를 쓸 수 있으며, 스파크 애플리케이션 개발시 스키마를 이미 알고 있는 경우라면 매우 잘 동작할 것입니다.

Dataset을 생성하는 두 번째 방법은 프로그래밍 가능한 인터페이스를 사용하여 스키마를 명시적으로 생성한 뒤 이를 RDD에 적용하는 방법입니다. 이 방법을 사용하면 코드는 길어지겠지만, 코드가 실행되기 전 각 컬럼과 그 타입을 모르는 경우에도 Dataset을 구성할 수 있습니다.


### **리플렉션(Reflection)을 사용한 스키마 유추**



*   **Scala**

Spark SQL의 Scala 인터페이스는 자동으로 케이스 클래스가 포함된 RDD를 DataFrame으로 변환합니다. 이 때 스키마는 케이스 클래스에 따라 정의됩니다. 즉, 리플렉션을 이용하여 케이스 클래스의 파라미터 이름을 컬럼 이름으로 사용합니다. 케이스 클래스는 `Seq`나 `Array`와 같은 복합 타입 혹은 중첩된 형태의 타입도 사용할 수 있습니다. 이렇게 RDD를 DataFrame으로 변환하여 테이블에 등록할 수 있습니다. 이렇게 만들어진 테이블은 하위 SQL문에서도 사용할 수 있습니다.


```
// RDD를 DataFrame으로 변환합니다
import spark.implicits._

// 텍스트 파일을 읽어 각 Person 객체의 RDD를 생성하고, 이를 DataFrame으로 변환합니다
val peopleDF = spark.sparkContext
  .textFile("examples/src/main/resources/people.txt")
  .map(_.split(","))
  .map(attributes => Person(attributes(0), attributes(1).trim.toInt))
  .toDF()
// DataFrame을 임시 뷰로 등록합니다
peopleDF.createOrReplaceTempView("people")

// 스파크에서 제공하는 sql 메소드를 이용해서 SQL문을 실행할 수 있습니다
val teenagersDF = spark.sql("SELECT name, age FROM people WHERE age BETWEEN 13 AND 19")

// 결과에서 각 로우의 컬럼은 필드의 인덱스로 접근할 수 있습니다
teenagersDF.map(teenager => "Name: " + teenager(0)).show()
// +------------+
// |       value|
// +------------+
// |Name: Justin|
// +------------+

// 필드의 이름으로 접근할 수도 있습니다
teenagersDF.map(teenager => "Name: " + teenager.getAs[String]("name")).show()
// +------------+
// |       value|
// +------------+
// |Name: Justin|
// +------------+

// Dataset[Map[K,V]]에 대한 인코더가 선언되어 있지 않으므로, 여기서 선언해줍니다
implicit val mapEncoder = org.apache.spark.sql.Encoders.kryo[Map[String, Any]]
// 기본 타입과 케이스 클래스는 아래와 같이 정의할 수 있습니다
// implicit val stringIntMapEncoder: Encoder[Map[String, Any]] = ExpressionEncoder()

// row.getValuesMap[T]는 여러 개의 컬럼을 한번에 Map[String, T] 형태로 가져옵니다
teenagersDF.map(teenager => teenager.getValuesMap[Any](List("name", "age"))).collect()
// Array(Map("name" -> "Justin", "age" -> 19))
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SparkSQLExample.scala"에서 전체 예제 코드를 볼 수 있습니다



*   **Python**

스파크 SQL은 Row 객체를 담고 있는 RDD에서 데이터 타입을 유추하여 DataFrame으로 변환할 수 있습니다. Row 객체는 키/값 쌍으로 이루어진 kwargs를 Row 클래스로 넘겨받아 생성됩니다. 이 목록에서 키는 테이블에서 컬럼의 이름을 정의합니다. 그리고 타입은 전체 데이터셋을 샘플링하여 유추하는데, 이 과정은 JSON 파일에서 수행하는 것과 비슷하게 이루어집니다.

**<code>from pyspark.sql import Row \
 \
sc = spark.sparkContext \
<em> \
# 텍스트 파일을 불러와 각 줄을 Row 객체로 변환합니다</em> \
lines = sc.textFile("examples/src/main/resources/people.txt") \
parts = lines.map(lambda l: l.split(",")) \
people = parts.map(lambda p: Row(name=p[0], age=int(p[1]))) \
 \
<em># 스키마를 유추하여 DataFrame을 테이블로 등록합니다</em> \
schemaPeople = spark.createDataFrame(people) \
schemaPeople.createOrReplaceTempView("people") \
 \
<em># 테이블로 등록한 Dataframe에서 SQL을 실행할 수 있습니다.</em> \
teenagers = spark.sql("SELECT name FROM people WHERE age >= 13 AND age <= 19") \
 \
<em># SQL 쿼리의 결과는 DataFrame 객체가 됩니다</em> \
<em># rdd는 :class:`Row`의 :class:`pyspark.RDD` 내용을 반환합니다</em> \
teenNames = teenagers.rdd.map(lambda p: "Name: " + p.name).collect() \
for name in teenNames: \
    print(name) \
<em># 이름: Justin</em> \
</code></strong> \
스파크 저장소의 "examples/src/main/python/sql/basic.py"에서 전체 예제 코드를  볼 수 있습니다.


### **프로그램 내에서 스키마 명시하기**



*   **Scala**

케이스 클래스가 미리 정의되지 않았을 때 (예를 들어, 레코드의 구조가 특정 문자열로 인코딩되어 있거나 텍스트 dataset이 사용자에 따라 서로 다르게 파싱되어 각 유저마다 필드값이 다르게 보이는 경우), 프로그램 내에서 세 단계를 거쳐 `DataFrame`을 생성할 수 있습니다.



1. 기존의 RDD에서 `RowS` 객체의 RDD를 생성합니다;
2. 1단계에서 생성한 `Row`s 객체의 RDD 구조와 일치하는 `StructType`으로 스키마를 생성합니다.
3. `SparkSession`의 `createDataFrame` 메소드를 사용하여 `RowS`객체의 RDD에 이 스키마를 적용합니다.

예를 들어:


```
import org.apache.spark.sql.types._

// RDD를 생성합니다
val peopleRDD = spark.sparkContext.textFile("examples/src/main/resources/people.txt")

// 스키마는 문자열로 인코딩됩니다
val schemaString = "name age"

// 스키마 문자열을 기반으로 스키마를 생성합니다
val fields = schemaString.split(" ")
  .map(fieldName => StructField(fieldName, StringType, nullable = true))
val schema = StructType(fields)

// RDD를 Rows 객체로 변환합니다
val rowRDD = peopleRDD
  .map(_.split(","))
  .map(attributes => Row(attributes(0), attributes(1).trim))

// RDD에 스키마를 적용합니다
val peopleDF = spark.createDataFrame(rowRDD, schema)

// DataFrame을 사용하여 임시 뷰를 생성합니다
peopleDF.createOrReplaceTempView("people")

// SQL은 DataFrame을 사용한 임시뷰에서 실행할 수 있습니다
val results = spark.sql("SELECT name FROM people")

// SQL 쿼리의 결과는 DataFrame이 되며 모든 일반 RDD 동작을 지원합니다
// 각 컬럼의 로우는 필드의 색인 또는 이름으로 접근할 수 있습니다
results.map(attributes => "Name: " + attributes(0)).show()
// +-------------+
// |        value|
// +-------------+
// |Name: Michael|
// |   Name: Andy|
// | Name: Justin|
// +-------------+
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SparkSQLExample.scala"에서 전체 예제 코드를 볼 수 있습니다.



*   **Python**

kwargs의 구조를 미리 정의할 수 없을 때 (예를 들어, 레코드의 구조가 특정 문자열로 인코딩되어 있거나 텍스트 Dataset이 사용자에 따라 서로 다르게 파싱되어 각 유저마다 필드값이 다르게 보이는 경우), `DataFrame`을 프로그램 내에서 세 단계를 거쳐 생성할 수 있습니다.



1. 기존의 RDD에서 튜플 또는 리스트로 이루어진 RDD를 생성합니다;
2. 1단계에서 생성한 RDD의 튜플 또는 리스트 구조와 일치하는 `StructType`으로 나타낸 스키마를 생성합니다.
3. `SparkSession`의 `createDataFrame` 메소드를 사용하여 RDD에 이 스키마를 적용합니다.

예제:


```
# 데이터 타입을 임포트합니다
from pyspark.sql.types import *

sc = spark.sparkContext

# 텍스트 파일을 불러와 각 라인을 로우(row)로 변환합니다
lines = sc.textFile("examples/src/main/resources/people.txt")
parts = lines.map(lambda l: l.split(","))
# 각 라인을 튜플로 변환합니다
people = parts.map(lambda p: (p[0], p[1].strip()))

# 스키마는 문자열로 인코딩됩니다
schemaString = "name age"

fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)

# RDD에 스키마를 적용합니다
schemaPeople = spark.createDataFrame(people, schema)

# DataFrame을 사용하여 임시 뷰를 생성합니다
schemaPeople.createOrReplaceTempView("people")

# SQL은 DataFrame을 사용한 임시뷰에서 실행할 수 있습니다
results = spark.sql("SELECT name FROM people")

results.show()
# +-------+
# |   name|
# +-------+
# |Michael|
# |   Andy|
# | Justin|
# +-------+
```


스파크 저장소의 "examples/src/main/python/sql/basic.py" 에서 전체 예제 코드를 볼 수 있습니다.


## **집계(Aggregations)**

[내장 DataFrames 함수](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.functions$)는 `count()`, `countDistinct()`, `avg()`, `max()`, `min()`와 같은 집계 함수를 제공합니다. 이 함수들은 DataFrame에서 사용할 수 있도록 만들어졌지만, 이들 중 일부는 [Scala](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.expressions.scalalang.typed$), [Java](https://spark.apache.org/docs/latest/api/java/org/apache/spark/sql/expressions/javalang/typed.html)의 (강한 타입체크를 수행하는) Dataset에서 사용할 수 있는 타입 안전(type-safe) 버전이 있습니다. 또한, 사용자는 내장된 집계 함수를 제한없이 사용할 수 있고 새로운 함수를 생성할 수도 있습니다.


### **타입이 없는 사용자 정의 집계 함수** \
사용자는 [UserDefinedAggregateFunction](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.expressions.UserDefinedAggregateFunction) 클래스를 확장하여 타입이 없는 사용자 정의 집계 함수를 구현할 수 있습니다. 예를 들어, 사용자 정의 평균 함수는 아래 예제와 같이 구현할 수 있습니다:



*   **Scala**

**<code>import org.apache.spark.sql.{Row, SparkSession} \
import org.apache.spark.sql.expressions.MutableAggregationBuffer \
import org.apache.spark.sql.expressions.UserDefinedAggregateFunction \
import org.apache.spark.sql.types._ \
 \
object MyAverage extends UserDefinedAggregateFunction { \
  <em>// 이 집계 함수 입력 인자의 데이터 타입</em> \
  def inputSchema: StructType = StructType(StructField("inputColumn", LongType) :: Nil) \
  <em>// 집계 버퍼 값의 데이터 타입 \
</em>  def bufferSchema: StructType = { \
    StructType(StructField("sum", LongType) :: StructField("count", LongType) :: Nil) \
  } \
  <em>// 반환 값의 데이터 타입</em> \
  def dataType: DataType = DoubleType \
  <em>// 동일한 입력에 대해 항상 동일한 출력 값을 반환하는지 확인합니다 \
</em>  def deterministic: Boolean = true \
  <em>// 주어진 집계 버퍼를 초기화합니다. 버퍼는 `Row` 객체이며 그 자체가 특정 인덱스에 해당하는 값을 반환하거나 값을 바꿀 수 있는 표준 메소드가 됩니다 (예: get(), getBoolean()) \
  // 버퍼 내의 배열과 맵은 값을 바꿀 수 없습니다</em> \
  def initialize(buffer: MutableAggregationBuffer): Unit = { \
    buffer(0) = 0L \
    buffer(1) = 0L \
  } \
  <em>// 새로운 입력 데이터 `input` 을 받아 집계 버퍼 `buffer` 를 업데이트합니다</em> \
  def update(buffer: MutableAggregationBuffer, input: Row): Unit = { \
    if (!input.isNullAt(0)) { \
      buffer(0) = buffer.getLong(0) + input.getLong(0) \
      buffer(1) = buffer.getLong(1) + 1 \
    } \
  } \
  <em>// 두 집계 버퍼를 병합하고 그 값을 `buufer1`에 저장합니다</em> \
  def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = { \
    buffer1(0) = buffer1.getLong(0) + buffer2.getLong(0) \
    buffer1(1) = buffer1.getLong(1) + buffer2.getLong(1) \
  } \
  <em>// 최종 결과를 계산합니다</em> \
  def evaluate(buffer: Row): Double = buffer.getLong(0).toDouble / buffer.getLong(1) \
} \
 \
<em>// 함수를 사용할 수 있도록 등록합니다</em> \
spark.udf.register("myAverage", MyAverage) \
 \
val df = spark.read.json("examples/src/main/resources/employees.json") \
df.createOrReplaceTempView("employees") \
df.show() \
<em>// +-------+------+</em> \
<em>// |   name|salary|</em> \
<em>// +-------+------+</em> \
<em>// |Michael|  3000|</em> \
<em>// |   Andy|  4500|</em> \
<em>// | Justin|  3500|</em> \
<em>// |  Berta|  4000|</em> \
<em>// +-------+------+</em> \
 \
val result = spark.sql("SELECT myAverage(salary) as average_salary FROM employees") \
result.show() \
<em>// +--------------+</em> \
<em>// |average_salary|</em> \
<em>// +--------------+</em> \
<em>// |        3750.0|</em> \
<em>// +--------------+</em> \
</code></strong> \
스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/UserDefinedUntypedAggregation.scala"에서 전체 예제 코드를 볼 수 있습니다.


### **타입 안전(Type-safe) 사용자 정의 집계 함수**

강한 타입 체크를 사용하는 Dataset에서 사용자 정의 집계 함수는 [Aggregator](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.expressions.Aggregator) 클래스를 이용해야 합니다. 타입 안전 사용자 정의 평균 함수는 아래 예제와 같이 구현합니다:



*   **Scala**


```
import org.apache.spark.sql.{Encoder, Encoders, SparkSession}
import org.apache.spark.sql.expressions.Aggregator

case class Employee(name: String, salary: Long)
case class Average(var sum: Long, var count: Long)

object MyAverage extends Aggregator[Employee, Average, Double] {
  // 이 집계 함수의 영값(zero value)입니다. 어떠한 b 값에 대해서도 b + zero = b를 만족해야 합니다
  def zero: Average = Average(0L, 0L)
  // 두 값을 가지고 새로운 값을 생성합니다. 성능을 위해 새로운 객체를 만드는 대신, 함수에서 직접 `buffer`를 수정하여 반환할 수도 있습니다
  def reduce(buffer: Average, employee: Employee): Average = {
    buffer.sum += employee.salary
    buffer.count += 1
    buffer
  }
  // 두 중간값을 병합합니다
  def merge(b1: Average, b2: Average): Average = {
    b1.sum += b2.sum
    b1.count += b2.count
    b1
  }
  // reduce 호출 결과를 최종 리턴값으로 변환합니다.
  def finish(reduction: Average): Double = reduction.sum.toDouble / reduction.count
  // 중간값 타입에 대한 인코더를 명시합니다
  def bufferEncoder: Encoder[Average] = Encoders.product
  // 최종 출력값 타입에 대한 인코더를 명시합니다
  def outputEncoder: Encoder[Double] = Encoders.scalaDouble
}

val ds = spark.read.json("examples/src/main/resources/employees.json").as[Employee]
ds.show()
// +-------+------+
// |   name|salary|
// +-------+------+
// |Michael|  3000|
// |   Andy|  4500|
// | Justin|  3500|
// |  Berta|  4000|
// +-------+------+

// 함수를 `TypedColumn`으로 변환하고 이름을 지정합니다
val averageSalary = MyAverage.toColumn.name("average_salary")
val result = ds.select(averageSalary)
result.show()
// +--------------+
// |average_salary|
// +--------------+
// |        3750.0|
// +--------------+
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/UserDefinedTypedAggregation.scala" 에서 전체 예제 코드를 볼 수 있습니다.