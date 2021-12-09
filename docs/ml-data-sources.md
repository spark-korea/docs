---
layout: global
title: ML 데이터 소스
displayTitle: ML 데이터 소스
---


* Table of contents
{:toc}


이 섹션에서는 ML의 데이터 소스를 사용하여 데이터를 로드하는 방법을 소개하겠습니다. Parquet(파케이), CSV, JSON 및 JDBC와 같은 일부 일반 데이터 소스 외에도 ML을 위한 특정 데이터 소스도 제공합니다.


## 이미지 데이터 소스
이미지 데이터 소스는 디렉토리에서 이미지 파일을 로드하는 데 사용되며, 압축된 이미지(jpeg, png 등)를 Java 라이브러리 안의 `ImageIO`를 통해 원시 이미지 표현으로 로드할 수 있습니다. 로드된 DataFrame에는 이미지 스키마로 저장된 이미지 데이터를 포함하는 하나의 `StructType` 컬럼 "image"가 있습니다. `image` 열의 스키마는 다음과 같습니다.


* origin: `StringType` (이미지 파일 경로)
* height: `IntegerType` (이미지 높이)
* width: `IntegerType` (이미지 너비)
* nChannels: `IntegerType` (이미지 채널의 개수)
* mode: `IntegerType` (OpenCV 호환 유형)
* data: `BinaryType` (OpenCV 호환 순서의 이미지 바이트, 대부분의 경우 행 단위 BGR)

### 예시
Scala와 Java에서는 `ImageDataSource`로 이미지 데이터를 DataFrame으로 로드하기 위한 Spark SQL 데이터 소스 API를 제공하며, Python는 PySpark에서, R은 SparkR에서 이미지 데이터를 DataFrame으로 로드하기 위한 Spark SQL 데이터 소스 API를 제공하고 있습니다.


<table class="table">
  <tr><th>언어</th><th>예시코드</th></tr>
  <tr>
    <td>Scala</td>
    <td>
    scala> <code>val df = spark.read.format("image").option("dropInvalid", true).load("data/mllib/images/origin/kittens")</code><br>
    scala> <code>df.select("image.origin", "image.width", "image.height").show(truncate=false)</code>
    </td>
  </tr>
  <tr>
    <td>Java</td>
     <td> <code> Dataset&lt;Row&gt; imagesDF = spark.read().format("image").option("dropInvalid", true).load("data/mllib/images/origin/kittens");
     <br><br>imageDF.select("image.origin", "image.width", "image.height").show(false); </code>
    </td>
  </tr>
  <tr>
    <td>Python</td>
    <td>>>> <code> df = spark.read.format("image").option("dropInvalid", True).load("data/mllib/images/origin/kittens") </code>
    <br>
    >>> <code> df.select("image.origin", "image.width", "image.height").show(truncate=False) </code> </td>
  </tr>
  <tr>
    <td>R</td>
    <td>> <code>df = read.df("data/mllib/images/origin/kittens", "image") </code>
    <br>
    > <code>head(select(df, df$image.origin, df$image.width, df$image.height))</code></td>
  </tr>
</table>

## LIBSVM 데이터 소스
이 `LIBSVM` 데이터 소스는 디렉터리에서 'libsvm' 유형 파일을 로드하는 데 사용됩니다. 로드된 DataFrame에는 두 개의 열 (label, features) 이 있습니다. 각각 doubles로 저장된 label과, Vectors로 저장된 features vector가 포함되어 있습니다. 해당 스키마의 columns은 다음과 같습니다.

* label: `DoubleType` (instance label을 나타냄)
* features: `VectorUDT` (feature vector를 나타냄)

### 예시
Scala와 Java에서는 `LibSVMDataSource`로 `LIBSVM` 데이터를 DataFrame으로 로드하기 위한 Spark SQL 데이터 소스 API를 제공하며, Python는 PySpark에서, R은 SparkR에서 `LIBSVM` 데이터를 DataFrame으로 로드하기 위한 Spark SQL 데이터 소스 API를 제공하고 있습니다.

<table class="table">
  <tr><th>언어</th><th>예시코드</th></tr>
  <tr>
    <td>Scala</td>
    <td>
    scala> <code>val df = spark.read.format("libsvm").option("numFeatures", "780").load("data/mllib/sample_libsvm_data.txt")</code><br>
    scala> <code>df.show(10)</code>
    </td>
  </tr>
  <tr>
    <td>Java</td>
     <td> <code> Dataset&lt;Row&gt; df = spark.read.format("libsvm").option("numFeatures", "780").load("data/mllib/sample_libsvm_data.txt");
     <br><br>df.show(10);</code>
    </td>
  </tr>
  <tr>
    <td>Python</td>
    <td>>>> <code> df = spark.read.format("libsvm").option("numFeatures", "780").load("data/mllib/sample_libsvm_data.txt") </code>
    <br>
    >>> <code> df.show(10)</code> </td>
  </tr>
  <tr>
    <td>R</td>
    <td>> <code>df = read.df("data/mllib/sample_libsvm_data.txt", "libsvm") </code>
    <br>
    > <code>head(select(df, df$label, df$features), 10)</code></td>
  </tr>
</table>