---
layout: global
title: PySpark Usage Guide for Pandas with Apache Arrow
displayTitle: PySpark Usage Guide for Pandas with Apache Arrow
---

# **아파치 애로우(Arrow)와 Pandas를 위한 PySpark 사용 가이드**



*  [ Arrow](#heading=h.n3yuzu4a4wo2)
    * [PyArrow 설치 확인](#heading=h.983l6ty2cevq)
* [Pandas로의 변환 또는 Pandas로부터의 변환 활성화](#heading=h.8qfpme8upsln)
*   [Pandas UDF (벡터화된 UDF)](#heading=h.hrqodxuz2074)
    *   [Scalar](#heading=h.b6yrjkugbwdn)
    *   <span style="text-decoration:underline;">그룹화된 맵</span>
    *   [그룹화된 집계 ](#heading=h.zcdd0fjbpjnu)
*   <span style="text-decoration:underline;">사용 기록</span>
    *  지원되는 [ SQL 타입](#heading=h.ngxghesdirnv)</span>
    *   [Arrow 배치 크기 설정](#heading=h.mu36f2vaq3cm)
    *   <span style="text-decoration:underline;">타임존(Time Zone) 의미와
[ timestamp ](#heading=h.sq7c6tks27gk)</span>


## **스파크의 아파치 애로우**

아파치 애로우는 인메모리(In-Memory) 컬럼기반 데이터 포맷으로 스파크에서 JVM과 Python 프로세스 간에 데이터를 효율적으로 전송하기 위해 사용됩니다. 현재 Pandas/NumPy 데이터로 작업하는 Python 사용자에게 가장 유용할 것입니다. 바로 사용할 수는 없으며 장점을 최대한 살리고 호환성을 높이기 위해서 설정이나 코드를 조금 수정해야 할 수 있습니다. 이 가이드는 스파크에서 애로우를 사용하는 방법에 대해 상위레벨에서 설명하고, 애로우를 사용할 수 있는 데이터로 작업할 때의 차이를 강조하여 알려줍니다.


### **PyArrow 설치 확인**

pip을 사용하여 PySpark를 설치한다면 `pip install pyspark[sql]` 명령을 사용하여 PyArrow를 SQL 모듈의 추가 의존성으로 가져올 수 있습니다. 그렇지 않다면 모든 클러스터 노드에서 PyArrow가 설치되어 있고 사용 가능한지 확인해야 합니다. 현재 지원되는 버전은 0.8.0입니다. pip 또는 conda-forge 채널의 conda를 사용하여 설치할 수 있습니다. 자세한 내용은 PyArrow [설치](https://arrow.apache.org/docs/python/install.html)를 참조하세요.

**Pandas와의 변환 활성화**

애로우는 `toPandas()`호출을 사용하여 스파크 DataFrame을 Pandas DataFrame으로 변환할 때와 `createDataFrame(pandas_df)`로 Pandas DataFrame에서 Spark DataFrame을 생성할 때 최적화를 위해 사용할 수 있습니다. 이러한 호출을 실행할 때 Arrow를 사용하려면 먼저 스파크 설정 'spark.sql.execution.arrow.enabled'를 'true'로 설정해야 합니다. 기본 설정은 사용하지 않음으로 되어 있습니다.

또한, 실제 연산 전에 스파크에서 에러가 발생한다면  'spark.sql.execution.arrow.enabled'로 활성화된 최적화는 자동으로 non-Arrow 최적화로 대체 될 수 있습니다. 이는 'spark.sql.execution.arrow.fallback.enabled'로 제어할 수 있습니다.



*   **Python**


```
import numpy as np
import pandas as pd

# Arrow 기반 컬럼 데이터 전송 활성화
spark.conf.set("spark.sql.execution.arrow.enabled", "true")

# Pandas DataFrame 생성
pdf = pd.DataFrame(np.random.rand(100, 3))

# Arrow를 사용하여 Pandas DataFrame에서 스파크 DataFrame 생성
df = spark.createDataFrame(pdf)

# Arrow를 사용하여 스파크 DataFrame을 Pandas DataFrame으로 다시 변환
result_pdf = df.select("*").toPandas()
```


전체 예제 코드는 스파크 저장소의 "examples/src/main/python/sql/arrow.py"를 참조하세요.

Arrow를 사용하여 위와 같이 최적화를 하면 Arrow가 활성화되지 않은 경우와 같은 결과가 나옵니다. Arrow를 사용하는 경우에도 `toPandas()`는 DataFrame의 모든 레코드 콜렉션을 드라이버 프로그램으로 변환하므로 데이터의 작은 서브셋에서 실행해야 합니다. 현재 모든 스파크 데이터 타입이 지원되는 것은 아니며 지원하지 않는 타입의 컬럼이 있는 경우 오류가 발생할 수 있으니 [지원 SQL 타입](https://spark.apache.org/docs/latest/sql-pyspark-pandas-with-arrow.html#supported-sql-types)을 참조하세요. `createDataFrame()`에서 오류가 발생하면 스파크는 Arrow를 사용하지 않고 DataFrame을 생성합니다.


## **Pandas UDFs (벡터화된 UDFs)**

Pandas UDF는 Arrow를 사용하여 데이터를 전송하고 Pandas를 이용하여 데이터를 다루기 위해 스파크에서 실행되는 사용자 정의 함수입니다. Pandas UDF는 `pandas_udf `키워드를 사용해서 정의할 수 있으며, 데코레이터로 또는 함수를 감싸기(wrap) 위해 사용합니다. 추가 설정은 필요하지 않습니다. 현재 두 종류의 Pandas UDF: Scalar와 그룹화된 맵이 있습니다.


### **Scalar**

Scalar Pandas UDF는 scalar 연산을 벡터화하는 데 사용됩니다. `select` 와 `withColumn` 같은 함수와 함께 사용할 수 있습니다. Python 함수는 `pandas.Series`를 입력으로 받아 같은 길이의 `pandas.Series`를 반환 해야 합니다. 스파크는 컬럼을 배치(batch)로 분할하고, 각 배치에서 함수를 호출하여 생성된 데이터 결과값들을 연결하여 Pandas UDF를 실행합니다.

다음 예제는 2개의 컬럼을 곱하는 scalar Pandas UDF를 만드는 방법을 보여줍니다.



*   **Python**


```
import pandas as pd

from pyspark.sql.functions import col, pandas_udf
from pyspark.sql.types import LongType

# 함수를 정의하고 UDF를 생성
def multiply_func(a, b):
    return a * b

multiply = pandas_udf(multiply_func, returnType=LongType())

# pandas_udf의 함수는 로컬 Pandas 데이터와 실행될 수 있어야 합니다
x = pd.Series([1, 2, 3])
print(multiply_func(x, x))
# 0    1
# 1    4
# 2    9
# dtype: int64

# 스파크 DataFrame 생성, 'spark'는 이미 생성된 SparkSession임
df = spark.createDataFrame(pd.DataFrame(x, columns=["x"]))

# 스파크 벡터화된 UDF로 함수 실행
df.select(multiply(col("x"), col("x"))).show()
# +-------------------+
# |multiply_func(x, x)|
# +-------------------+
# |                  1|
# |                  4|
# |                  9|
# +-------------------+
```


전제 예제는 스파크 저장소의 "examples/src/main/python/sql/arrow.py"를 참조하세요.

**그룹화된 맵**

그룹화된 맵 Pandas UDF는 “분할-적용-결합” 패턴을 구현하는 `groupBy().apply()`와 함께 사용됩니다. 분할-적용-결합은 세 단계로 구성됩니다:



*   `DataFrame.groupBy`를 이용하여 데이터를 그룹으로 분할합니다.
*   각 그룹에 함수를 적용합니다. 함수의 입력과 출력값은 모두 `pandas.DataFrame`입니다. 입력 데이터는 각 그룹의 모든 로우와 컬럼을 포함합니다. 
*   결과값을 새로운 `DataFrame`으로 결합합니다.

`groupBy().apply()`를 사용하려면 사용자는 다음 내용을 정의해야 합니다:



*   각 그룹에서의 연산을 정의할 Python 함수.
*   `DataFrame` 출력의 스키마를 정의할 `StructType` 객체나 문자열.

반환된 `pandas.DataFrame`의 컬럼 레이블이 문자열인 경우에는 정의된 출력 스키마의 필드 이름과 일치해야하며, 문자열이 아닌 경우에는 위치의 필드 데이터 타입과 일치해야 합니다 (예 : 정수 인덱스). `pandas.DataFrame`을 작성할 때 컬럼 레이블을 작성하는 방법은 [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html#pandas.DataFrame)을 참조하세요.

함수가 적용되기 전에 그룹의 모든 데이터가 메모리에 로드됩니다. 그룹 크기가 비대칭이면 메모리 부족 예외가 발생할 수 있습니다. [maxRecordsPerBatch](https://spark.apache.org/docs/latest/sql-pyspark-pandas-with-arrow.html#setting-arrow-batch-size)의 설정은 그룹에는 적용되지 않으며, 사용자는 직접 그룹화된 데이터 크기가 사용 가능한 메모리 크기 적절한지 확인해야 합니다.

다음 예제는 `groupby().apply()`를 사용하여 그룹의 각 값에서 평균을 빼는 것을 보여줍니다.



*   **Python**


```
from pyspark.sql.functions import pandas_udf, PandasUDFType

df = spark.createDataFrame(
    [(1, 1.0), (1, 2.0), (2, 3.0), (2, 5.0), (2, 10.0)],
    ("id", "v"))

@pandas_udf("id long, v double", PandasUDFType.GROUPED_MAP)
def subtract_mean(pdf):
    # pdf는 pandas.DataFrame입니다
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
```


전체 예제는 스파크 저장소의 "examples/src/main/python/sql/arrow.py"를 참조하세요.

자세한 사용법은 <code>[pyspark.sql.functions.pandas_udf](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.functions.pandas_udf)</code> 와 <code>[pyspark.sql.GroupedData.apply](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.GroupedData.apply)</code>를 참조하세요.


### **그룹화된 집계 (Aggregate)**

그룹화된 집계 Pandas UDF는 스파크 집계 함수와 비슷합니다. 그룹화된 집계  Pandas UDF는 `groupBy().agg()`및 <code>[pyspark.sql.Window](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.Window)</code>와 함께 사용됩니다. 각 <code>pandas.Series</code>가 그룹 또는 윈도우 내의 컬럼을 의미할 때,  그룹화된 집계 Pandas UDF는 하나 이상의 <code>pandas.Series</code>에서 scalar 값까지의 집계를 정의합니다.

이런 타입의 UDF는 부분 집계를 지원하지 않으며 그룹 또는 윈도우의 모든 데이터는 메모리로 로드됩니다. 또한 현재 그룹화된 집계 Pandas UDF는 언바운드(unbounded) 윈도우만 지원합니다. 

다음 예제는 이 타입의 UDF를 사용하여 groupBy로 평균값을 계산하는 방법과 윈도우 동작들을 보여줍니다:



*   **Python**


```
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
```


전체 예제는 스파크 저장소의 "examples/src/main/python/sql/arrow.py"를 참조하세요.

자세한 사용법은 `pyspark.sql.functions.pandas_udf `를 참조하세요.


## **사용 기록**


### **지원되는 SQL 타입**

현재 `MapType`, `TimestampType`의 `ArrayType, 중첩 StructType`을 제외한 모든 스파크 SQL 데이터 타입은 Arrow 기반 변환을 지원합니다. `BinaryType`은 설치된 PyArrow 버전 0.10.0 이상에서만 지원됩니다.


### **애로우 배치 크기 설정**

Spark의 데이터 파티션은 Arrow 레코드 배치로 변환되어 JVM에서 메모리 사용량을 일시적으로 높일 수 있습니다. 메모리 부족 문제를 방지하기 위해, "spark.sql.execution.arrow.maxRecordsPerBatch"를 각 배치의 최대 로우 수를 결정하는 정수로 설정하여 Arrow 레코드 배치의 크기를 조정할 수 있습니다. 기본값은 배치 당 10,000 레코드입니다. 컬럼 수가 많으면 적절하게 값을 조정해야 합니다. 이 방법을 통해, 각 데이터 파티션은 프로세싱을 위한 하나 이상의 레코드 배치로 만들어집니다.


### **타임존(Time Zone) 의미와 timestamp**

스파크는 내부적으로 timestamp를 UTC 값으로 저장하며, 지정된 시간대가 없는 timestamp 데이터는 로컬 타임에서 마이크로초 단위의 UTC로 변환됩니다. timestamp 데이터를 내보내거나 스파크에서 표시할 때, 세션 시간대는 timestamp값을 지역화하는 데 사용됩니다. 세션 시간대는 'spark.sql.session.timeZone'으로 설정되며, 설정되지 않은 경우 기본값은 JVM 시스템 로컬 시간대가 기본값이 됩니다. Pandas 는 나노초(nanosecond) 단위의 `datetime64` 인 `datetime64[ns]`를 사용하며, 각 컬럼 단위 시간대는 선택 사항입니다.

timestamp 데이터가 스파크에서 Pandas로 전송될 때 나노초로 변환되고, 각 컬럼은 스파크 세션 시간대로 변환된 후 해당 시간대로 지역화되어 기존 시간대를 제거하고 로컬 타임으로 값을 표시합니다. 이 변환은 timestamp 컬럼에서 `toPandas()` 또는 `pandas_udf`를 호출할 때 발생합니다.

timestamp 데이터가 Pandas에서 스파크로 전송될 때는 UTC 마이크로초(microsecond)로 변환됩니다. 이는 pandas DataFrame으로 `createDataFrame`을 호출하거나 `pandas_udf`에서 timestamp를 반환할 때 발생합니다. 이 변환은 스파크가 예상할 수 있는 형식의 데이터를 받을 수 있도록 자동으로 실행되기 때문에 우리가 직접 변환할 필요가 없습니다. 이 때 나노 이하 단위는 삭제됩니다.

(Pandas가 아닌) 표준 UDF는 timestamp 데이터를 Pandas timestamp가 아닌 Python datetime 오브젝트로 불러옵니다. `pandas_udf`의 timestamp로 작업할 때 최상의 성능을 얻으려면 Pandas 타임 시리즈 기능을 사용하는 것이 좋습니다. 자세한 내용은 [여기](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html)를 참조하세요.
