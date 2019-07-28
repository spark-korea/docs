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
A simple example demonstrating Arrow in Spark.
Run with:
  ./bin/spark-submit examples/src/main/python/sql/arrow.py
"""

from __future__ import print_function

from pyspark.sql import SparkSession
from pyspark.sql.utils import require_minimum_pandas_version, require_minimum_pyarrow_version

require_minimum_pandas_version()
require_minimum_pyarrow_version()


def dataframe_with_arrow_example(spark):
    # $example on:dataframe_with_arrow$
    import numpy as np
    import pandas as pd

    # Arrow 기반 컬럼 데이터 전송을 활성화합니다.
    spark.conf.set("spark.sql.execution.arrow.enabled", "true")

    # Pandas DataFrame 생성합니다.
    pdf = pd.DataFrame(np.random.rand(100, 3))

    # Arrow를 사용하여 Pandas DataFrame에서 스파크 DataFrame을 생성합니다.
    df = spark.createDataFrame(pdf)

    # Arrow를 사용하여 스파크 DataFrame을 Pandas DataFrame으로 다시 변환합니다.
    result_pdf = df.select("*").toPandas()
    # $example off:dataframe_with_arrow$
    print("Pandas DataFrame result statistics:\n%s\n" % str(result_pdf.describe()))


def scalar_pandas_udf_example(spark):
    # $example on:scalar_pandas_udf$
    import pandas as pd

    from pyspark.sql.functions import col, pandas_udf
    from pyspark.sql.types import LongType

    # 함수를 정의하고 UDF를 생성합니다.
    def multiply_func(a, b):
        return a * b

    multiply = pandas_udf(multiply_func, returnType=LongType())

    # pandas_udf에 주어지는 함수는 로컬 Pandas 데이터와 실행될 수 있어야 합니다.
    x = pd.Series([1, 2, 3])
    print(multiply_func(x, x))
    # 0    1
    # 1    4
    # 2    9
    # dtype: int64

    # 스파크 DataFrame을 생성합니다. ('spark'는 이전에 생성한 SparkSession입니다.)
    df = spark.createDataFrame(pd.DataFrame(x, columns=["x"]))

    # 스파크 벡터화된 UDF로 함수를 실행합니다.
    df.select(multiply(col("x"), col("x"))).show()
    # +-------------------+
    # |multiply_func(x, x)|
    # +-------------------+
    # |                  1|
    # |                  4|
    # |                  9|
    # +-------------------+
    # $example off:scalar_pandas_udf$


def grouped_map_pandas_udf_example(spark):
    # $example on:grouped_map_pandas_udf$
    from pyspark.sql.functions import pandas_udf, PandasUDFType

    df = spark.createDataFrame(
        [(1, 1.0), (1, 2.0), (2, 3.0), (2, 5.0), (2, 10.0)],
        ("id", "v"))

    @pandas_udf("id long, v double", PandasUDFType.GROUPED_MAP)
    def subtract_mean(pdf):
        # pdf의 타입은 pandas.DataFrame 입니다.
        v = pdf.v
        return pdf.assign(v=v - v.mean())

    df.groupby("id").apply(subtract_mean).show()
    # +---+----+
    # | id|   v|
    # +---+----+
    # |  1|-0.5|
    # |  1| 0.5|
    # |  2|-3.0|
    # |  2|-1.0|
    # |  2| 4.0|
    # +---+----+
    # $example off:grouped_map_pandas_udf$


def grouped_agg_pandas_udf_example(spark):
    # $example on:grouped_agg_pandas_udf$
    from pyspark.sql.functions import pandas_udf, PandasUDFType
    from pyspark.sql import Window

    df = spark.createDataFrame(
        [(1, 1.0), (1, 2.0), (2, 3.0), (2, 5.0), (2, 10.0)],
        ("id", "v"))

    @pandas_udf("double", PandasUDFType.GROUPED_AGG)
    def mean_udf(v):
        return v.mean()

    df.groupby("id").agg(mean_udf(df['v'])).show()
    # +---+-----------+
    # | id|mean_udf(v)|
    # +---+-----------+
    # |  1|        1.5|
    # |  2|        6.0|
    # +---+-----------+

    w = Window \
        .partitionBy('id') \
        .rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)
    df.withColumn('mean_v', mean_udf(df['v']).over(w)).show()
    # +---+----+------+
    # | id|   v|mean_v|
    # +---+----+------+
    # |  1| 1.0|   1.5|
    # |  1| 2.0|   1.5|
    # |  2| 3.0|   6.0|
    # |  2| 5.0|   6.0|
    # |  2|10.0|   6.0|
    # +---+----+------+
    # $example off:grouped_agg_pandas_udf$


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Python Arrow-in-Spark example") \
        .getOrCreate()

    print("Running Pandas to/from conversion example")
    dataframe_with_arrow_example(spark)
    print("Running pandas_udf scalar example")
    scalar_pandas_udf_example(spark)
    print("Running pandas_udf grouped map example")
    grouped_map_pandas_udf_example(spark)

    spark.stop()
