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

// $example on:typed_custom_aggregation$
import org.apache.spark.sql.{Encoder, Encoders, SparkSession}
import org.apache.spark.sql.expressions.Aggregator
// $example off:typed_custom_aggregation$

object UserDefinedTypedAggregation {

  // $example on:typed_custom_aggregation$
  case class Employee(name: String, salary: Long)
  case class Average(var sum: Long, var count: Long)

  object MyAverage extends Aggregator[Employee, Average, Double] {
    // 이 집계 함수의 영값(zero value)입니다. 임의의 b 값에 대해서 b + zero = b를 만족합니다.
    def zero: Average = Average(0L, 0L)
    // 두 값을 가지고 새로운 값을 생성합니다. 성능을 위해 새로운 객체를 만드는 대신,
    // 함수에서 직접 `buffer`를 수정하여 반환할 수도 있습니다.
    def reduce(buffer: Average, employee: Employee): Average = {
      buffer.sum += employee.salary
      buffer.count += 1
      buffer
    }
    // 두 중간값을 병합합니다.
    def merge(b1: Average, b2: Average): Average = {
      b1.sum += b2.sum
      b1.count += b2.count
      b1
    }
    // reduce 호출 결과를 최종 리턴값으로 변환합니다.
    def finish(reduction: Average): Double = reduction.sum.toDouble / reduction.count
    // 중간값 타입에 대한 인코더를 명시합니다.
    def bufferEncoder: Encoder[Average] = Encoders.product
    // 최종 출력값 타입에 대한 인코더를 명시합니다.
    def outputEncoder: Encoder[Double] = Encoders.scalaDouble
  }
  // $example off:typed_custom_aggregation$

  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder()
      .appName("Spark SQL user-defined Datasets aggregation example")
      .getOrCreate()

    import spark.implicits._

    // $example on:typed_custom_aggregation$
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

    // 함수를 `TypedColumn`으로 변환하고 이름을 지정합니다.
    val averageSalary = MyAverage.toColumn.name("average_salary")
    val result = ds.select(averageSalary)
    result.show()
    // +--------------+
    // |average_salary|
    // +--------------+
    // |        3750.0|
    // +--------------+
    // $example off:typed_custom_aggregation$

    spark.stop()
  }

}
