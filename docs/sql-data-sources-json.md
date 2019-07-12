---
layout: global
title: JSON Files
displayTitle: JSON Files
---
# **JSON 파일**



*   **Scala**

스파크 SQL은 JSON dataset의 스키마(schema)를 자동으로 추론하여 `Dataset[Row]`로 로드할 수 있습니다. 이러한 변환은 `Dataset[String]이나 `JSON 파일의 `SparkSession.read.json()`을 호출하여 사용할 수 있습니다. 

여기서의 _json 파일_은 일반적인 JSON 파일이 아닙니다. 각 라인에는 각각 독립적이고 그 자체로 유효한 JSON 객체가 들어 있어야 합니다. 자세한 정보는 [(newline-delimited JSON이라고도 불리는) JSON 라인 텍스트 형식](http://jsonlines.org/)을 참고하세요.

일반적인 multi-line JSON 파일의 경우, `multiLine `옵션을 `true`로 설정하시면 됩니다.


```
// 기본 타입(Int, String, etc)과 프로덕트 타입(case classes) 인코더는
// Dataset을 만들 때 이를 불러와서 사용할 수 있습니다.
import spark.implicits._

// JSON dataset의 경로를 지정합니다.
// 경로는 단일 텍스트 파일 또는 텍스트 파일들을 담고있는 디렉토리가 될 수 있습니다.
val path = "examples/src/main/resources/people.json"
val peopleDF = spark.read.json(path)

// 추론된 스키마는 printSchema() 메소드를 이용해 시각화할 수 있습니다.
peopleDF.printSchema()
// root
//  |-- age: long (nullable = true)
//  |-- name: string (nullable = true)

// DataFrame을 이용하여 임시 뷰(temporary view)를 만듭니다.
peopleDF.createOrReplaceTempView("people")

// 스파크에서 제공하는 sql 메소드를 이용하여 SQL 명령문을 실행할 수 있습니다.
val teenagerNamesDF = spark.sql("SELECT name FROM people WHERE age BETWEEN 13 AND 19")
teenagerNamesDF.show()
// +------+
// |  name|
// +------+
// |Justin|
// +------+

// 다른 방법으로, string마다 하나의 JSON 객체를 저장하는 Dataset[String]으로 표현되는 
// JSON dataset에 대한 DataFrame을 만들 수 있습니다.
val otherPeopleDataset = spark.createDataset(
  """{"name":"Yin","address":{"city":"Columbus","state":"Ohio"}}""" :: Nil)
val otherPeople = spark.read.json(otherPeopleDataset)
otherPeople.show()
// +---------------+----+
// |        address|name|
// +---------------+----+
// |[Columbus,Ohio]| Yin|
// +---------------+----+
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala" 에서 예제 코드를 확인하세요.



*   **Python**

스파크 SQL은 JSON dataset의 스키마(schema)를 자동으로 추론하여 `Dataset[Row]`로 로드할 수 있습니다. 이러한 변환은 JSON 파일의 `SparkSession.read.json()`을 호출하여 사용할 수 있습니다. 

여기서의 _json 파일_은 일반적인 JSON 파일이 아닙니다. 각 라인에는 각각 독립적이고 그 자체로 유효한 JSON 객체가 들어 있어야 합니다. 자세한 정보는 [(newline-delimited JSON이라고도 불리는) JSON 라인 텍스트 형식](http://jsonlines.org/)을 참고하세요.

일반적인 multi-line JSON 파일의 경우, `multiLine `옵션을 `true`로 설정하시면 됩니다.


```
# spark는 이전 예제에서 나온 것입니다.
sc = spark.sparkContext

// JSON dataset의 경로를 지정합니다.
// 경로는 단일 텍스트 파일 또는 텍스트 파일들을 담고있는 디렉토리가 될 수 있습니다.
path = "examples/src/main/resources/people.json"
peopleDF = spark.read.json(path)

# 추론된 스키마는 printSchema() 메소드를 이용해 시각화할 수 있습니다.
peopleDF.printSchema()
# root
#  |-- age: long (nullable = true)
#  |-- name: string (nullable = true)

# DataFrame을 이용하여 임시 뷰(temporary view)를 만듭니다.
peopleDF.createOrReplaceTempView("people")

# 스파크에서 제공하는 sql 메소드를 이용하여 SQL 명령문을 실행할 수 있습니다.
teenagerNamesDF = spark.sql("SELECT name FROM people WHERE age BETWEEN 13 AND 19")
teenagerNamesDF.show()
# +------+
# |  name|
# +------+
# |Justin|
# +------+

# 다른 방법으로, string마다 하나의 JSON 객체를 저장하는 RDD[String]로 표현되는
# JSON dataset에 대한 DataFrame을 만들 수 있습니다.
jsonStrings = ['{"name":"Yin","address":{"city":"Columbus","state":"Ohio"}}']
otherPeopleRDD = sc.parallelize(jsonStrings)
otherPeople = spark.read.json(otherPeopleRDD)
otherPeople.show()
# +---------------+----+
# |        address|name|
# +---------------+----+
# |[Columbus,Ohio]| Yin|
# +---------------+----+
```


스파크 저장소의 "examples/src/main/python/sql/datasource.py"에서 예제 코드를 확인하세요.