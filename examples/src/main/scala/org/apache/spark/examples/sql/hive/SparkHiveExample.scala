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
package org.apache.spark.examples.sql.hive

// $example on:spark_hive$
import java.io.File

import org.apache.spark.sql.{Row, SaveMode, SparkSession}
// $example off:spark_hive$

object SparkHiveExample {

  // $example on:spark_hive$
  case class Record(key: Int, value: String)
  // $example off:spark_hive$

  def main(args: Array[String]) {
    // When working with Hive, one must instantiate `SparkSession` with Hive support, including
    // connectivity to a persistent Hive metastore, support for Hive serdes, and Hive user-defined
    // functions. Users who do not have an existing Hive deployment can still enable Hive support.
    // When not configured by the hive-site.xml, the context automatically creates `metastore_db`
    // in the current directory and creates a directory configured by `spark.sql.warehouse.dir`,
    // which defaults to the directory `spark-warehouse` in the current directory that the spark
    // application is started.

    // $example on:spark_hive$
    // warehouseLocation은 hive 데이터베이스와 테이블의 기본 위치를 지정합니다.
    val warehouseLocation = new File("spark-warehouse").getAbsolutePath

    val spark = SparkSession
      .builder()
      .appName("Spark Hive Example")
      .config("spark.sql.warehouse.dir", warehouseLocation)
      .enableHiveSupport()
      .getOrCreate()

    import spark.implicits._
    import spark.sql

    sql("CREATE TABLE IF NOT EXISTS src (key INT, value STRING) USING hive")
    sql("LOAD DATA LOCAL INPATH 'examples/src/main/resources/kv1.txt' INTO TABLE src")

    // HiveQL로 쿼리를 표현합니다. (역자 주: Spark SQL과 조금 다릅니다.)
    sql("SELECT * FROM src").show()
    // +---+-------+
    // |key|  value|
    // +---+-------+
    // |238|val_238|
    // | 86| val_86|
    // |311|val_311|
    // ...

    // 집계 쿼리도 지원합니다.
    sql("SELECT COUNT(*) FROM src").show()
    // +--------+
    // |count(1)|
    // +--------+
    // |    500 |
    // +--------+

    // SQL 쿼리의 결과는 그 자체로 DataFrame이며, 모든 일반적인 함수를 지원합니다.
    val sqlDF = sql("SELECT key, value FROM src WHERE key < 10 ORDER BY key")

    // DataFrame은 Row 타입으로 이루어져 있습니다. 각 컬럼에는 index를 사용해서 접근할 수 있습니다.
    val stringsDS = sqlDF.map {
      case Row(key: Int, value: String) => s"Key: $key, Value: $value"
    }
    stringsDS.show()
    // +--------------------+
    // |               value|
    // +--------------------+
    // |Key: 0, Value: val_0|
    // |Key: 0, Value: val_0|
    // |Key: 0, Value: val_0|
    // ...

    // DataFrame을 사용하여 SparkSession에 임시 뷰를 생성할 수 있습니다.
    val recordsDF = spark.createDataFrame((1 to 100).map(i => Record(i, s"val_$i")))
    recordsDF.createOrReplaceTempView("records")

    // 이제, DataFrame의 데이터와 Hive에 저장된 데이터에 JOIN 쿼리를 사용할 수 있습니다.
    sql("SELECT * FROM records r JOIN src s ON r.key = s.key").show()
    // +---+------+---+------+
    // |key| value|key| value|
    // +---+------+---+------+
    // |  2| val_2|  2| val_2|
    // |  4| val_4|  4| val_4|
    // |  5| val_5|  5| val_5|
    // ...

    // `USING hive`를 사용하는 스파크 SQL 문법 대신 HiveQL의 문법을 사용하여 Hive managed Parquet 테이블을 생성합니다.
    sql("CREATE TABLE hive_records(key int, value string) STORED AS PARQUET")
    // DataFrame을 Hive managed 테이블로 저장합니다.
    val df = spark.table("src")
    df.write.mode(SaveMode.Overwrite).saveAsTable("hive_records")
    // 데이터를 삽입한 후에는 Hive 매니지드 테이블(managed table)에 데이터가 저장됩니다.
    sql("SELECT * FROM hive_records").show()
    // +---+-------+
    // |key|  value|
    // +---+-------+
    // |238|val_238|
    // | 86| val_86|
    // |311|val_311|
    // ...

    // Parquet 데이터 디렉토리를 지정합니다.
    val dataDir = "/tmp/parquet_data"
    spark.range(10).write.parquet(dataDir)
    // Hive 외부 Parquet 테이블을 생성합니다.
    sql(s"CREATE EXTERNAL TABLE hive_ints(key int) STORED AS PARQUET LOCATION '$dataDir'")
    // Hive 외부 테이블은 이미 데이터를 갖고있어야 합니다.
    sql("SELECT * FROM hive_ints").show()
    // +---+
    // |key|
    // +---+
    // |  0|
    // |  1|
    // |  2|
    // ...

    // Hive 동적 파티셔닝(Partitioning)을 위한 플래그를 활성화합니다.
    spark.sqlContext.setConf("hive.exec.dynamic.partition", "true")
    spark.sqlContext.setConf("hive.exec.dynamic.partition.mode", "nonstrict")
    // DataFrame API를 사용하여 Hive 분할 테이블을 생성합니다.
    df.write.partitionBy("key").format("hive").saveAsTable("hive_part_tbl")
    // 분할된 컬럼 `key`는 스키마의 마지막 순서로 이동합니다.
    sql("SELECT * FROM hive_part_tbl").show()
    // +-------+---+
    // |  value|key|
    // +-------+---+
    // |val_238|238|
    // | val_86| 86|
    // |val_311|311|
    // ...

    spark.stop()
    // $example off:spark_hive$
  }
}
