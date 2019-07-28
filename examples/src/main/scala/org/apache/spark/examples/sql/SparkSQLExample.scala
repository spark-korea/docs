/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.spark.examples.sql

import org.apache.spark.sql.Row
// $example on:init_session$
import org.apache.spark.sql.SparkSession
// $example off:init_session$
// $example on:programmatic_schema$
// $example on:data_types$
import org.apache.spark.sql.types._
// $example off:data_types$
// $example off:programmatic_schema$

object SparkSQLExample {

  // $example on:create_ds$
  case class Person(name: String, age: Long)
  // $example off:create_ds$

  def main(args: Array[String]) {
    // $example on:init_session$
    val spark = SparkSession
      .builder()
      .appName("Spark SQL basic example")
      .config("spark.some.config.option", "some-value")
      .getOrCreate()

    // RDD를 DataFrame으로 바꾸는 것과 같은 암시적 변환(implicit conversion)을 처리하기 위해
    // 아래와 같이 import를 해 줍니다.
    import spark.implicits._
    // $example off:init_session$

    runBasicDataFrameExample(spark)
    runDatasetCreationExample(spark)
    runInferSchemaExample(spark)
    runProgrammaticSchemaExample(spark)

    spark.stop()
  }

  private def runBasicDataFrameExample(spark: SparkSession): Unit = {
    // $example on:create_df$
    val df = spark.read.json("examples/src/main/resources/people.json")

    // 표준출력(stdout)에 DataFrame의 내용을 보여줍니다.
    df.show()
    // +----+-------+
    // | age|   name|
    // +----+-------+
    // |null|Michael|
    // |  30|   Andy|
    // |  19| Justin|
    // +----+-------+
    // $example off:create_df$

    // $example on:untyped_ops$
    // $-notation을 사용하기 위해 임포트합니다.
    import spark.implicits._
    // 트리 형태로 스키마를 출력합니다.
    df.printSchema()
    // root
    // |-- age: long (nullable = true)
    // |-- name: string (nullable = true)

    // "name" 컬럼을 선택합니다.
    df.select("name").show()
    // +-------+
    // |   name|
    // +-------+
    // |Michael|
    // |   Andy|
    // | Justin|
    // +-------+

    // 모든 사람을 선택하고, 나이를 1씩 증가시킵니다.
    df.select($"name", $"age" + 1).show()
    // +-------+---------+
    // |   name|(age + 1)|
    // +-------+---------+
    // |Michael|     null|
    // |   Andy|       31|
    // | Justin|       20|
    // +-------+---------+

    // 나이가 21살보다 많은 사람을 선택합니다.
    df.filter($"age" > 21).show()
    // +---+----+
    // |age|name|
    // +---+----+
    // | 30|Andy|
    // +---+----+

    // 각 나이별로 사람의 수를 셉니다.
    df.groupBy("age").count().show()
    // +----+-----+
    // | age|count|
    // +----+-----+
    // |  19|    1|
    // |null|    1|
    // |  30|    1|
    // +----+-----+
    // $example off:untyped_ops$

    // $example on:run_sql$
    // DataFrame을 SQL 임시 뷰로 등록합니다.
    df.createOrReplaceTempView("people")

    val sqlDF = spark.sql("SELECT * FROM people")
    sqlDF.show()
    // +----+-------+
    // | age|   name|
    // +----+-------+
    // |null|Michael|
    // |  30|   Andy|
    // |  19| Justin|
    // +----+-------+
    // $example off:run_sql$

    // $example on:global_temp_view$
    // DataFrame을 전역 임시 뷰에 등록합니다.
    df.createGlobalTempView("people")

    // 전역 임시 뷰는 시스템 데이터베이스에 `global_temp` 라는 이름으로 등록됩니다.
    spark.sql("SELECT * FROM global_temp.people").show()
    // +----+-------+
    // | age|   name|
    // +----+-------+
    // |null|Michael|
    // |  30|   Andy|
    // |  19| Justin|
    // +----+-------+

    // 전역 임시 뷰는 다른 SparkSession에서도 사용할 수 있습니다.
    spark.newSession().sql("SELECT * FROM global_temp.people").show()
    // +----+-------+
    // | age|   name|
    // +----+-------+
    // |null|Michael|
    // |  30|   Andy|
    // |  19| Justin|
    // +----+-------+
    // $example off:global_temp_view$
  }

  private def runDatasetCreationExample(spark: SparkSession): Unit = {
    import spark.implicits._
    // $example on:create_ds$
    // Encoder는 케이스 클래스별로 생성됩니다.
    val caseClassDS = Seq(Person("Andy", 32)).toDS()
    caseClassDS.show()
    // +----+---+
    // |name|age|
    // +----+---+
    // |Andy| 32|
    // +----+---+

    // 일반적으로 사용되는 대부분의 타입에 대한 인코더는 spark.implicits._를 임포트하면 자동으로 포함됩니다.
    val primitiveDS = Seq(1, 2, 3).toDS()
    primitiveDS.map(_ + 1).collect() // Array(2, 3, 4) 반환.

    // 클래스를 지정함으로써 DataFrame을 Dataset으로 변환할 수 있습니다. 값들은 클래스의 속성 변수 이름에 따라 자동으로 할당됩니다.
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
    // $example off:create_ds$
  }

  private def runInferSchemaExample(spark: SparkSession): Unit = {
    // $example on:schema_inferring$
    // RDD를 DataFrame으로 암시적으로 변환(implicit conversion)하기 위해 임포트합니다.
    import spark.implicits._

    // Create an RDD of Person objects from a text file, convert it to a Dataframe
    // 텍스트 파일을 읽어 Person 객체의 RDD를 생성하고, 이를 DataFrame으로 변환합니다.
    val peopleDF = spark.sparkContext
      .textFile("examples/src/main/resources/people.txt")
      .map(_.split(","))
      .map(attributes => Person(attributes(0), attributes(1).trim.toInt))
      .toDF()
    // DataFrame을 임시 뷰로 등록합니다.
    peopleDF.createOrReplaceTempView("people")

    // 스파크에서 제공하는 sql 메소드를 이용해서 SQL문을 실행할 수 있습니다.
    val teenagersDF = spark.sql("SELECT name, age FROM people WHERE age BETWEEN 13 AND 19")

    // 결과에서 각 로우의 컬럼은 필드의 인덱스로 접근할 수 있습니다.
    teenagersDF.map(teenager => "Name: " + teenager(0)).show()
    // +------------+
    // |       value|
    // +------------+
    // |Name: Justin|
    // +------------+

    // 필드의 이름으로 접근할 수도 있습니다.
    teenagersDF.map(teenager => "Name: " + teenager.getAs[String]("name")).show()
    // +------------+
    // |       value|
    // +------------+
    // |Name: Justin|
    // +------------+

    // Dataset[Map[K,V]]에 대한 인코더가 선언되어 있지 않으므로, 여기서 명시적으로 선언해줍니다.
    implicit val mapEncoder = org.apache.spark.sql.Encoders.kryo[Map[String, Any]]
    // 기본 타입과 케이스 클래스는 아래와 같이 정의할 수 있습니다:
    // implicit val stringIntMapEncoder: Encoder[Map[String, Any]] = ExpressionEncoder()

    // row.getValuesMap[T]는 여러 개의 컬럼을 한번에 Map[String, T] 형태로 가져옵니다.
    teenagersDF.map(teenager => teenager.getValuesMap[Any](List("name", "age"))).collect()
    // Array(Map("name" -> "Justin", "age" -> 19))
    // $example off:schema_inferring$
  }

  private def runProgrammaticSchemaExample(spark: SparkSession): Unit = {
    import spark.implicits._
    // $example on:programmatic_schema$
    // RDD를 생성합니다.
    val peopleRDD = spark.sparkContext.textFile("examples/src/main/resources/people.txt")

    // 스키마는 문자열로 인코딩됩니다.
    val schemaString = "name age"

    // 스키마 문자열을 기반으로 스키마를 생성합니다.
    val fields = schemaString.split(" ")
      .map(fieldName => StructField(fieldName, StringType, nullable = true))
    val schema = StructType(fields)

    // RDD(people)에 들어 있는 레코드를 Row 객체로 변환합니다.
    val rowRDD = peopleRDD
      .map(_.split(","))
      .map(attributes => Row(attributes(0), attributes(1).trim))

    // RDD에 스키마를 적용합니다.
    val peopleDF = spark.createDataFrame(rowRDD, schema)

    // DataFrame을 사용하여 임시 뷰를 생성합니다.
    peopleDF.createOrReplaceTempView("people")

    // 테이블의 형태로 등록된 Dataframe에서 SQL 문을 실행할 수 있습니다.
    val results = spark.sql("SELECT name FROM people")

    // SQL 쿼리의 결과 역시 DataFrame이 되며, 모든 일반적인 RDD 동작을 지원합니다.
    // 각 컬럼의 로우는 필드의 인덱스 값 또는 이름으로 접근할 수 있습니다.
    results.map(attributes => "Name: " + attributes(0)).show()
    // +-------------+
    // |        value|
    // +-------------+
    // |Name: Michael|
    // |   Name: Andy|
    // | Name: Justin|
    // +-------------+
    // $example off:programmatic_schema$
  }
}
