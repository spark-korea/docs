---
layout: global
title: Reference
displayTitle: Reference
---

# **참조**



*   

<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: undefined internal link (link text: "데이터 타입"). Did you generate a TOC? </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

[데이터 타입](#heading=h.zf7iob93mkov)
*   

<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: undefined internal link (link text: "NaN 시맨틱"). Did you generate a TOC? </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

[NaN 시맨틱](#heading=h.ks50xalnnfqi)
*   

<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: undefined internal link (link text: "산술 연산"). Did you generate a TOC? </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

[산술 연산](#heading=h.feus2krebrsf)


## **데이터 타입**

스파크 SQL 과 DataFrame은 다음 데이터 타입을 지원합니다:



*   숫자 타입
    *   `ByteType`: 1 바이트 부호 있는(signed) 정수를 나타냅니다. 범위는 `-128` 부터 `127`까지 입니다.
    *   `ShortType`: 2 바이트 부호 있는(signed) 정수를 나타냅니다. 범위는 `-32768`부터 `32767`까지입니다.
    *   `IntegerType`: 4 바이트 부호 있는(signed) 정수를 나타냅니다. 범위는 `-2147483648`부터 `2147483647`까지 입니다.
    *   `LongType`: 8 바이트 부호 있는(signed) 정수를 나타냅니다. 범위는 `-9223372036854775808`부터 `9223372036854775807`입니다.
    *   `FloatType`: 4 바이트 단정밀도(single-precision) 부동 소수점수를 나타냅니다.
    *   `DoubleType`: 8 바이트 배정밀도(double-precision) 부동 소수점수를 나타냅니다.
    *   `DecimalType`: 임의정밀도(arbitrary-precision)의 부호 있는(signed) 소수를 나타냅니다. `java.math.BigDecimal`로 내부적으로 지원됩니다. `BigDecimal` 은 임의정밀도(arbitrary-precision)의 제한 없는(unscaled) 정수와 32비트의 제한 있는(scaled) 정수 스케일로 구성됩니다.
*   문자열 타입
    *   `StringType`: 문자열 값을 나타냅니다.
*   이진 타입
    *   `BinaryType`: 바이트 시퀀스 값을 나타냅니다.
*   Boolean 타입
    *   `BooleanType`: boolean값을 나타냅니다.
*   날짜시간 타입
    *   `TimestampType`: 년, 월, 일, 시, 분, 초 필드 값으로 구성된 값을 나타냅니다. 
    *   `DateType`: 연, 월, 일 필드 값으로 구성된 값을 나타냅니다.
*   복합 타입
    *   `ArrayType(elementType, containsNull)`: `elementType`의 요소 시퀀스로 구성된 값을 나타냅니다. `containsNull`은 `ArrayType`의 요소가 `null`값을 가질 수 있는지 여부를 나타내는데 사용됩니다.
    *   `MapType(keyType, valueType, valueContainsNull)`: 일련의 키-값 쌍으로 구성된 값을 나타냅니다. 키의 데이터 타입은 `keyType` 이고 값의 데이터 타입은 `valueType` 입니다. `MapType` 값에서 키는 `null`값을 가질 수 없습니다. `valueContainsNull` 은 `MapType` 이 `null` 값을 가질 수 있는지 여부를 나타내는 데 사용됩니다.
    *   `StructType(fields)`: `StructField `(`fields`)` `구조의 시퀀스를 가진 값을 나타냅니다.
        *   `StructField(name, dataType, nullable)`: `StructType` 의 필드를 나타냅니다. 필드 이름은 `name`으로 지정됩니다. 필드의 데이터 타입은 `dataType`으로 지정됩니다. `nullable` 은 필드 값이 `null`값을 가질 수 있는지 여부를 나타내는 데 사용됩니다. 
*   **Scala**

스파크 SQL의 모든 데이터 타입은 `org.apache.spark.sql.types` 패키지에 있습니다. 다음 코드를 통해 해당 데이터 타입에 접근할 수 있습니다.


```
import org.apache.spark.sql.types._
```


전체 예제는 스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SparkSQLExample.scala" 를 참고하세요.


<table>
  <tr>
   <td><strong>데이터 타입</strong>
   </td>
   <td><strong>Scala 값 유형</strong>
   </td>
   <td><strong>데이터 타입에 접근하거나 데이터 타입을 생성하기 위한 API </strong>
   </td>
  </tr>
  <tr>
   <td><strong>ByteType</strong>
   </td>
   <td>Byte
   </td>
   <td>ByteType
   </td>
  </tr>
  <tr>
   <td><strong>ShortType</strong>
   </td>
   <td>Short
   </td>
   <td>ShortType
   </td>
  </tr>
  <tr>
   <td><strong>IntegerType</strong>
   </td>
   <td>Int
   </td>
   <td>IntegerType
   </td>
  </tr>
  <tr>
   <td><strong>LongType</strong>
   </td>
   <td>Long
   </td>
   <td>LongType
   </td>
  </tr>
  <tr>
   <td><strong>FloatType</strong>
   </td>
   <td>Float
   </td>
   <td>FloatType
   </td>
  </tr>
  <tr>
   <td><strong>DoubleType</strong>
   </td>
   <td>Double
   </td>
   <td>DoubleType
   </td>
  </tr>
  <tr>
   <td><strong>DecimalType</strong>
   </td>
   <td>java.math.BigDecimal
   </td>
   <td>DecimalType
   </td>
  </tr>
  <tr>
   <td><strong>StringType</strong>
   </td>
   <td>String
   </td>
   <td>StringType
   </td>
  </tr>
  <tr>
   <td><strong>BinaryType</strong>
   </td>
   <td>Array[Byte]
   </td>
   <td>BinaryType
   </td>
  </tr>
  <tr>
   <td><strong>BooleanType</strong>
   </td>
   <td>Boolean
   </td>
   <td>BooleanType
   </td>
  </tr>
  <tr>
   <td><strong>TimestampType</strong>
   </td>
   <td>java.sql.Timestamp
   </td>
   <td>TimestampType
   </td>
  </tr>
  <tr>
   <td><strong>DateType</strong>
   </td>
   <td>java.sql.Date
   </td>
   <td>DateType
   </td>
  </tr>
  <tr>
   <td><strong>ArrayType</strong>
   </td>
   <td>scala.collection.Seq
   </td>
   <td>ArrayType(<em>elementType</em>, [<em>containsNull</em>])
<p>
<strong>Note:</strong> <em>containsNull</em> 의 기본값은 <em>true</em>입니다.
   </td>
  </tr>
  <tr>
   <td><strong>MapType</strong>
   </td>
   <td>scala.collection.Map
   </td>
   <td>MapType(<em>keyType</em>, <em>valueType</em>, [<em>valueContainsNull</em>])
<p>
<strong>Note:</strong> <em>valueContainsNull</em> 의 기본값은 <em>true</em>입니다.
   </td>
  </tr>
  <tr>
   <td><strong>StructType</strong>
   </td>
   <td>org.apache.spark.sql.Row
   </td>
   <td>StructType(<em>fields</em>)
<p>
<strong>Note:</strong> <em>fields</em> 는 StructField의 시퀀스입니다. 두 필드가 같은 이름을 가질 수는 없습니다.
   </td>
  </tr>
  <tr>
   <td><strong>StructField</strong>
   </td>
   <td>필드 데이터 타입의 Scala 값 유형. (예를 들어, 데이터 타입으로 IntegerType를 가지는 StructField는 Int)
   </td>
   <td>StructField(<em>name</em>, <em>dataType</em>, [<em>nullable</em>])
<p>
<strong>Note:</strong> <em>nullable</em> 의 기본값은 <em>true</em>입니다.
   </td>
  </tr>
</table>




*   **Python**

스파크 SQL의 모든 데이터 타입은 `pyspark.sql.types` 패키지에 있습니다. 다음 코드를 통해 해당 데이터 타입에 접근할 수 있습니다.


```
from pyspark.sql.types import *
```

<table>
  <tr>
   <td>

<strong>데이터 타입</strong>
   </td>
   <td>Python 값 유형
   </td>
   <td><strong>데이터 타입에 접근하거나 데이터 타입을 생성하기 위한 API </strong>
   </td>
  </tr>
  <tr>
   <td><strong>ByteType</strong>
   </td>
   <td>int 또는 long 
<p>
Note: 런타임 시 숫자가 1바이트 부호 있는 정수로 변환됩니다. 숫자가  -128에서 127 사이인지 확인하십시오.
   </td>
   <td>ByteType()
   </td>
  </tr>
  <tr>
   <td><strong>ShortType</strong>
   </td>
   <td>int 또는 long 
<p>
Note: 런타임 시 숫자가 2바이트 부호 있는 정수로 변환됩니다. 숫자가 -32768에서 32767 사이인지 확인하십시오.
   </td>
   <td>ShortType()
   </td>
  </tr>
  <tr>
   <td><strong>IntegerType</strong>
   </td>
   <td>int 또는 long
   </td>
   <td>IntegerType()
   </td>
  </tr>
  <tr>
   <td><strong>LongType</strong>
   </td>
   <td>long 
<p>
Note: 런타임 시 숫자가 8바이트 부호 있는 정수로 변환됩니다. 숫자가 9223372036854775808에서 9223372036854775807 사이인지 확인하십시오. 해당 범위의 숫자가 아니라면 데이터를 decimal.Decimal로 변환하고 DecimalType을 사용하십시오.
   </td>
   <td>LongType()
   </td>
  </tr>
  <tr>
   <td><strong>FloatType</strong>
   </td>
   <td>float 
<p>
Note: 런타임 시 숫자가 4바이트 단정도 부동 소수점수로 변환됩니다.
   </td>
   <td>FloatType()
   </td>
  </tr>
  <tr>
   <td><strong>DoubleType</strong>
   </td>
   <td>float
   </td>
   <td>DoubleType()
   </td>
  </tr>
  <tr>
   <td><strong>DecimalType</strong>
   </td>
   <td>decimal.Decimal
   </td>
   <td>DecimalType()
   </td>
  </tr>
  <tr>
   <td><strong>StringType</strong>
   </td>
   <td>string
   </td>
   <td>StringType()
   </td>
  </tr>
  <tr>
   <td><strong>BinaryType</strong>
   </td>
   <td>bytearray
   </td>
   <td>BinaryType()
   </td>
  </tr>
  <tr>
   <td><strong>BooleanType</strong>
   </td>
   <td>bool
   </td>
   <td>BooleanType()
   </td>
  </tr>
  <tr>
   <td><strong>TimestampType</strong>
   </td>
   <td>datetime.datetime
   </td>
   <td>TimestampType()
   </td>
  </tr>
  <tr>
   <td><strong>DateType</strong>
   </td>
   <td>datetime.date
   </td>
   <td>DateType()
   </td>
  </tr>
  <tr>
   <td><strong>ArrayType</strong>
   </td>
   <td>list, tuple, or array
   </td>
   <td>ArrayType(<em>elementType</em>, [<em>containsNull</em>])
<p>
Note: <em>containsNull</em> 의 기본값은 <em>True</em>입니다.
   </td>
  </tr>
  <tr>
   <td><strong>MapType</strong>
   </td>
   <td>dict
   </td>
   <td>MapType(<em>keyType</em>, <em>valueType</em>, [<em>valueContainsNull</em>])
<p>
Note: <em>valueContainsNull</em> 의 기본값은 <em>True</em>입니다.
   </td>
  </tr>
  <tr>
   <td><strong>StructType</strong>
   </td>
   <td>list 또는 tuple
   </td>
   <td>StructType(<em>fields</em>)
<p>
Note: <em>fields</em> 는 StructFields의 시퀀스입니다. 또한, 두개의 필드가 같은 이름을 가질 수 없습니다.
   </td>
  </tr>
  <tr>
   <td><strong>StructField</strong>
   </td>
   <td>필드 데이터 타입의 Python 값 유형 (예를 들어, 데이터 타입으로 IntegerType를 가지는 StructField는 Int)
   </td>
   <td>StructField(<em>name</em>, <em>dataType</em>, [<em>nullable</em>])
<p>
Note: <em>nullable</em> 의 기본값은 <em>True</em>입니다.
   </td>
  </tr>
</table>



## **NaN 의미 구조**

표준 부동 소수점 의미와 정확히 일치하지 않는 float 또는 double 타입을 처리 할 때 not-a-number (NaN)을 다루는 방법이 있습니다. 구체적으로는 다음과 같이 처리합니다.



*   NaN = NaN은 true를 반환합니다.
*   집계에서 모든 NaN값은 같은 그룹으로 묶입니다.
*   조인 키에서 NaN은 일반 값으로 다뤄집니다.
*   오름차순일 때, NaN 값은 가장 큰 숫자로서 제일 마지막에 위치합니다.


## **산술 연산**

숫자 타입 (`decimal`제외) 연산 시 오버플로가 체크되지 않습니다. 이는 오버플로를 발생시키는 연산 시 그 결과값이 Java/Scala 프로그램에서 반환되는 연산 결과값과 같다는 것을 의미합니다. (예. 두 정수의 합이 표현할 수 있는 최댓값보다 크다면 결과값이 음수가 됩니다).
