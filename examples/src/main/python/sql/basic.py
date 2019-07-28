#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
A simple example demonstrating basic Spark SQL features.
Run with:
  ./bin/spark-submit examples/src/main/python/sql/basic.py
"""
from __future__ import print_function

# $example on:init_session$
from pyspark.sql import SparkSession
# $example off:init_session$

# $example on:schema_inferring$
from pyspark.sql import Row
# $example off:schema_inferring$

# $example on:programmatic_schema$
# 데이터 타입을 임포트합니다.
from pyspark.sql.types import *
# $example off:programmatic_schema$


def basic_df_example(spark):
    # $example on:create_df$
    # 여기에서 spark는 이미 생성된 SparkSession입니다.
    df = spark.read.json("examples/src/main/resources/people.json")
    # 표준출력(stdout)에 DataFrame의 내용을 보여줍니다.
    df.show()
    # +----+-------+
    # | age|   name|
    # +----+-------+
    # |null|Michael|
    # |  30|   Andy|
    # |  19| Justin|
    # +----+-------+
    # $example off:create_df$

    # $example on:untyped_ops$
    # spark와 df는 이전 예제와 동일합니다.
    # 트리 형태로 스키마를 출력합니다.
    df.printSchema()
    # root
    # |-- age: long (nullable = true)
    # |-- name: string (nullable = true)

    # "name" 컬럼을 선택합니다.
    df.select("name").show()
    # +-------+
    # |   name|
    # +-------+
    # |Michael|
    # |   Andy|
    # | Justin|
    # +-------+

    # 모든 사람을 선택하고, 나이를 1씩 증가시킵니다.
    df.select(df['name'], df['age'] + 1).show()
    # +-------+---------+
    # |   name|(age + 1)|
    # +-------+---------+
    # |Michael|     null|
    # |   Andy|       31|
    # | Justin|       20|
    # +-------+---------+

    # 나이가 21살보다 많은 사람을 선택합니다.
    df.filter(df['age'] > 21).show()
    # +---+----+
    # |age|name|
    # +---+----+
    # | 30|Andy|
    # +---+----+

    # 각 나이별로 사람의 수를 셉니다.
    df.groupBy("age").count().show()
    # +----+-----+
    # | age|count|
    # +----+-----+
    # |  19|    1|
    # |null|    1|
    # |  30|    1|
    # +----+-----+
    # $example off:untyped_ops$

    # $example on:run_sql$
    # DataFrame을 SQL 임시 뷰로 등록합니다.
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
    # $example off:run_sql$

    # $example on:global_temp_view$
    # DataFrame을 전역 임시 뷰에 등록합니다.
    df.createGlobalTempView("people")

    # 전역 임시 뷰는 시스템 데이터베이스에 `global_temp` 라는 이름으로 등록됩니다.
    spark.sql("SELECT * FROM global_temp.people").show()
    # +----+-------+
    # | age|   name|
    # +----+-------+
    # |null|Michael|
    # |  30|   Andy|
    # |  19| Justin|
    # +----+-------+

    # 전역 임시 뷰는 다른 SparkSession에서도 사용할 수 있습니다.
    spark.newSession().sql("SELECT * FROM global_temp.people").show()
    # +----+-------+
    # | age|   name|
    # +----+-------+
    # |null|Michael|
    # |  30|   Andy|
    # |  19| Justin|
    # +----+-------+
    # $example off:global_temp_view$


def schema_inference_example(spark):
    # $example on:schema_inferring$
    sc = spark.sparkContext

    # 텍스트 파일을 불러와 각 라인을 로우(row)로 변환합니다.
    lines = sc.textFile("examples/src/main/resources/people.txt")
    parts = lines.map(lambda l: l.split(","))
    people = parts.map(lambda p: Row(name=p[0], age=int(p[1])))

    # 스키마를 추론하고, DataFrame을 테이블로 등록합니다.
    schemaPeople = spark.createDataFrame(people)
    schemaPeople.createOrReplaceTempView("people")

    # 테이블의 형태로 등록된 Dataframe에서 SQL 문을 실행할 수 있습니다.
    teenagers = spark.sql("SELECT name FROM people WHERE age >= 13 AND age <= 19")

    # SQL 쿼리의 결과는 DataFrame 객체가 됩니다.
    # rdd는 :class:`Row`의 :class:`pyspark.RDD` 타입으로 내용을 반환합니다.
    teenNames = teenagers.rdd.map(lambda p: "Name: " + p.name).collect()
    for name in teenNames:
        print(name)
    # Name: Justin
    # $example off:schema_inferring$


def programmatic_schema_example(spark):
    # $example on:programmatic_schema$
    sc = spark.sparkContext

    # 텍스트 파일을 불러와 각 라인을 로우(row)로 변환합니다.
    lines = sc.textFile("examples/src/main/resources/people.txt")
    parts = lines.map(lambda l: l.split(","))
    # 각 라인을 튜플로 변환합니다.
    people = parts.map(lambda p: (p[0], p[1].strip()))

    # 스키마는 문자열로 인코딩됩니다.
    schemaString = "name age"

    fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
    schema = StructType(fields)

    # RDD에 스키마를 적용합니다.
    schemaPeople = spark.createDataFrame(people, schema)

    # DataFrame을 사용하여 임시 뷰를 생성합니다.
    schemaPeople.createOrReplaceTempView("people")

    # 테이블의 형태로 등록된 Dataframe에서 SQL 문을 실행할 수 있습니다.
    results = spark.sql("SELECT name FROM people")

    results.show()
    # +-------+
    # |   name|
    # +-------+
    # |Michael|
    # |   Andy|
    # | Justin|
    # +-------+
    # $example off:programmatic_schema$

if __name__ == "__main__":
    # $example on:init_session$
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL basic example") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()
    # $example off:init_session$

    basic_df_example(spark)
    schema_inference_example(spark)
    programmatic_schema_example(spark)

    spark.stop()
