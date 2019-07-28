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
A simple example demonstrating Spark SQL Hive integration.
Run with:
  ./bin/spark-submit examples/src/main/python/sql/hive.py
"""
from __future__ import print_function

# $example on:spark_hive$
from os.path import expanduser, join, abspath

from pyspark.sql import SparkSession
from pyspark.sql import Row
# $example off:spark_hive$


if __name__ == "__main__":
    # $example on:spark_hive$
    # warehouse_location은 hive 데이터베이스와 테이블의 기본 위치를 지정합니다.
    warehouse_location = abspath('spark-warehouse')

    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL Hive integration example") \
        .config("spark.sql.warehouse.dir", warehouse_location) \
        .enableHiveSupport() \
        .getOrCreate()

    # spark는 위에서 생성한 SparkSession 객체입니다.
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

    # DataFrame은 Row 타입으로 이루어져 있습니다. 각 컬럼에는 index를 사용해서 접근할 수 있습니다.
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
    # $example off:spark_hive$

    spark.stop()
