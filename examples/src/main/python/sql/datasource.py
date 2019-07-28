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
A simple example demonstrating Spark SQL data sources.
Run with:
  ./bin/spark-submit examples/src/main/python/sql/datasource.py
"""
from __future__ import print_function

from pyspark.sql import SparkSession
# $example on:schema_merging$
from pyspark.sql import Row
# $example off:schema_merging$


def basic_datasource_example(spark):
    # $example on:generic_load_save_functions$
    df = spark.read.load("examples/src/main/resources/users.parquet")
    df.select("name", "favorite_color").write.save("namesAndFavColors.parquet")
    # $example off:generic_load_save_functions$

    # $example on:write_partitioning$
    df.write.partitionBy("favorite_color").format("parquet").save("namesPartByColor.parquet")
    # $example off:write_partitioning$

    # $example on:write_partition_and_bucket$
    df = spark.read.parquet("examples/src/main/resources/users.parquet")
    (df
        .write
        .partitionBy("favorite_color")
        .bucketBy(42, "name")
        .saveAsTable("people_partitioned_bucketed"))
    # $example off:write_partition_and_bucket$

    # $example on:manual_load_options$
    df = spark.read.load("examples/src/main/resources/people.json", format="json")
    df.select("name", "age").write.save("namesAndAges.parquet", format="parquet")
    # $example off:manual_load_options$

    # $example on:manual_load_options_csv$
    df = spark.read.load("examples/src/main/resources/people.csv",
                         format="csv", sep=":", inferSchema="true", header="true")
    # $example off:manual_load_options_csv$

    # $example on:manual_save_options_orc$
    df = spark.read.orc("examples/src/main/resources/users.orc")
    (df.write.format("orc")
        .option("orc.bloom.filter.columns", "favorite_color")
        .option("orc.dictionary.key.threshold", "1.0")
        .save("users_with_options.orc"))
    # $example off:manual_save_options_orc$

    # $example on:write_sorting_and_bucketing$
    df.write.bucketBy(42, "name").sortBy("age").saveAsTable("people_bucketed")
    # $example off:write_sorting_and_bucketing$

    # $example on:direct_sql$
    df = spark.sql("SELECT * FROM parquet.`examples/src/main/resources/users.parquet`")
    # $example off:direct_sql$

    spark.sql("DROP TABLE IF EXISTS people_bucketed")
    spark.sql("DROP TABLE IF EXISTS people_partitioned_bucketed")


def parquet_example(spark):
    # $example on:basic_parquet_example$
    peopleDF = spark.read.json("examples/src/main/resources/people.json")

    # DataFrame은 스키마 정보를 유지하면서 Parquet 파일로 저장할 수 있습니다.
    peopleDF.write.parquet("people.parquet")

    # 위에서 생성한 parquet 파일을 읽습니다.
    # parquet 파일에는 스키마 정보가 포함되어 있습니다. 따라서 위에서 읽어온 스키마는 그대로 보존됩니다.
    # parquet 파일을 불러온 결과 역시 DataFrame이 됩니다.
    parquetFile = spark.read.parquet("people.parquet")

    # parquet 파일은 임시 뷰를 생성하고 SQL문을 실행하는데 사용할 수 있습니다.
    parquetFile.createOrReplaceTempView("parquetFile")
    teenagers = spark.sql("SELECT name FROM parquetFile WHERE age >= 13 AND age <= 19")
    teenagers.show()
    # +------+
    # |  name|
    # +------+
    # |Justin|
    # +------+
    # $example off:basic_parquet_example$


def parquet_schema_merging_example(spark):
    # $example on:schema_merging$
    # spark는 이전 예제에서 나온 것입니다.
    # 간단한 DataFrame을 생성하고 분할 디렉토리에 저장합니다.
    sc = spark.sparkContext

    squaresDF = spark.createDataFrame(sc.parallelize(range(1, 6))
                                      .map(lambda i: Row(single=i, double=i ** 2)))
    squaresDF.write.parquet("data/test_table/key=1")

    # 새로운 컬럼을 추가하고 기존의 컬럼을 삭제함으로써 또 다른 DataFrame을 생성하고,
    # 새로운 분할 디렉토리에 저장합니다.
    cubesDF = spark.createDataFrame(sc.parallelize(range(6, 11))
                                    .map(lambda i: Row(single=i, triple=i ** 3)))
    cubesDF.write.parquet("data/test_table/key=2")

    # 분할된 테이블을 읽어옵니다.
    mergedDF = spark.read.option("mergeSchema", "true").parquet("data/test_table")
    mergedDF.printSchema()

    # 최종 스키마는 Parquet 파일에 들어 있는 세 개의 컬럼과
    # 파티션 디렉토리 경로에 나타나는 파티션 컬럼, 모두 네 개의 컬럼으로 이루어집니다.
    # root
    #  |-- double: long (nullable = true)
    #  |-- single: long (nullable = true)
    #  |-- triple: long (nullable = true)
    #  |-- key: integer (nullable = true)
    # $example off:schema_merging$


def json_dataset_example(spark):
    # $example on:json_dataset$
    # spark는 이전 예제에서 나온 것입니다.
    sc = spark.sparkContext

    # JSON dataset의 경로를 지정합니다.
    # 경로는 단일 텍스트 파일 또는 텍스트 파일들을 담고있는 디렉토리가 될 수 있습니다.
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
    # $example off:json_dataset$


def jdbc_dataset_example(spark):
    # $example on:jdbc_dataset$
    # 주의: JDBC 불러오기와 저장하기는 load/save나 jdbc 메소드로 할 수 있습니다
    # JDBC 소스에서 데이터 불러오기
    jdbcDF = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql:dbserver") \
        .option("dbtable", "schema.tablename") \
        .option("user", "username") \
        .option("password", "password") \
        .load()

    jdbcDF2 = spark.read \
        .jdbc("jdbc:postgresql:dbserver", "schema.tablename",
              properties={"user": "username", "password": "password"})

    # 읽기 DataFrame의 컬럼 데이터 유형 지정하기
    jdbcDF3 = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql:dbserver") \
        .option("dbtable", "schema.tablename") \
        .option("user", "username") \
        .option("password", "password") \
        .option("customSchema", "id DECIMAL(38, 0), name STRING") \
        .load()

    # JDBC 소스로 데이터 저장하기
    jdbcDF.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql:dbserver") \
        .option("dbtable", "schema.tablename") \
        .option("user", "username") \
        .option("password", "password") \
        .save()

    jdbcDF2.write \
        .jdbc("jdbc:postgresql:dbserver", "schema.tablename",
              properties={"user": "username", "password": "password"})

    # 쓰기의 테이블 생성시 컬럼 데이터 유형 지정하기
    jdbcDF.write \
        .option("createTableColumnTypes", "name CHAR(64), comments VARCHAR(1024)") \
        .jdbc("jdbc:postgresql:dbserver", "schema.tablename",
              properties={"user": "username", "password": "password"})
    # $example off:jdbc_dataset$


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL data source example") \
        .getOrCreate()

    basic_datasource_example(spark)
    parquet_example(spark)
    parquet_schema_merging_example(spark)
    json_dataset_example(spark)
    jdbc_dataset_example(spark)

    spark.stop()
