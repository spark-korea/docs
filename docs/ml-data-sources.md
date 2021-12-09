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

{% highlight scala %}

scala> val df = spark.read.format("image").option("dropInvalid", true).load("data/mllib/images/origin/kittens")
df: org.apache.spark.sql.DataFrame = [image: struct<origin: string, height: int ... 4 more fields>]

scala> df.select("image.origin", "image.width", "image.height").show(truncate=false)
+-----------------------------------------------------------------------+-----+------+
|origin                                                                 |width|height|
+-----------------------------------------------------------------------+-----+------+
|file:///spark/data/mllib/images/origin/kittens/54893.jpg               |300  |311   |
|file:///spark/data/mllib/images/origin/kittens/DP802813.jpg            |199  |313   |
|file:///spark/data/mllib/images/origin/kittens/29.5.a_b_EGDP022204.jpg |300  |200   |
|file:///spark/data/mllib/images/origin/kittens/DP153539.jpg            |300  |296   |
+-----------------------------------------------------------------------+-----+------+

{% endhighlight %}


{% highlight java %}

Dataset<Row> imagesDF = spark.read().format("image").option("dropInvalid", true).load("data/mllib/images/origin/kittens");
imageDF.select("image.origin", "image.width", "image.height").show(false);
/*
Will output:
+-----------------------------------------------------------------------+-----+------+
|origin                                                                 |width|height|
+-----------------------------------------------------------------------+-----+------+
|file:///spark/data/mllib/images/origin/kittens/54893.jpg               |300  |311   |
|file:///spark/data/mllib/images/origin/kittens/DP802813.jpg            |199  |313   |
|file:///spark/data/mllib/images/origin/kittens/29.5.a_b_EGDP022204.jpg |300  |200   |
|file:///spark/data/mllib/images/origin/kittens/DP153539.jpg            |300  |296   |
+-----------------------------------------------------------------------+-----+------+
*/

{% endhighlight %}


{% highlight python %}

>>> df = spark.read.format("image").option("dropInvalid", True).load("data/mllib/images/origin/kittens")
>>> df.select("image.origin", "image.width", "image.height").show(truncate=False)
+-----------------------------------------------------------------------+-----+------+
|origin                                                                 |width|height|
+-----------------------------------------------------------------------+-----+------+
|file:///spark/data/mllib/images/origin/kittens/54893.jpg               |300  |311   |
|file:///spark/data/mllib/images/origin/kittens/DP802813.jpg            |199  |313   |
|file:///spark/data/mllib/images/origin/kittens/29.5.a_b_EGDP022204.jpg |300  |200   |
|file:///spark/data/mllib/images/origin/kittens/DP153539.jpg            |300  |296   |
+-----------------------------------------------------------------------+-----+------+

{% endhighlight %}


{% highlight r %}

> df = read.df("data/mllib/images/origin/kittens", "image")
> head(select(df, df$image.origin, df$image.width, df$image.height))

1               file:///spark/data/mllib/images/origin/kittens/54893.jpg
2            file:///spark/data/mllib/images/origin/kittens/DP802813.jpg
3 file:///spark/data/mllib/images/origin/kittens/29.5.a_b_EGDP022204.jpg
4            file:///spark/data/mllib/images/origin/kittens/DP153539.jpg
  width height
1   300    311
2   199    313
3   300    200
4   300    296

{% endhighlight %}

## LIBSVM 데이터 소스
이 `LIBSVM` 데이터 소스는 디렉터리에서 'libsvm' 유형 파일을 로드하는 데 사용됩니다. 로드된 DataFrame에는 두 개의 열 (label, features) 이 있습니다. 각각 doubles로 저장된 label과, Vectors로 저장된 features vector가 포함되어 있습니다. 해당 스키마의 columns은 다음과 같습니다.

* label: `DoubleType` (instance label을 나타냄)
* features: `VectorUDT` (feature vector를 나타냄)

### 예시
Scala와 Java에서는 `LibSVMDataSource`로 `LIBSVM` 데이터를 DataFrame으로 로드하기 위한 Spark SQL 데이터 소스 API를 제공하며, Python는 PySpark에서, R은 SparkR에서 `LIBSVM` 데이터를 DataFrame으로 로드하기 위한 Spark SQL 데이터 소스 API를 제공하고 있습니다.

{% highlight scala %}

scala> val df = spark.read.format("libsvm").option("numFeatures", "780").load("data/mllib/sample_libsvm_data.txt")
df: org.apache.spark.sql.DataFrame = [label: double, features: vector]

scala> df.show(10)
+-----+--------------------+
|label|            features|
+-----+--------------------+
|  0.0|(780,[127,128,129...|
|  1.0|(780,[158,159,160...|
|  1.0|(780,[124,125,126...|
|  1.0|(780,[152,153,154...|
|  1.0|(780,[151,152,153...|
|  0.0|(780,[129,130,131...|
|  1.0|(780,[158,159,160...|
|  1.0|(780,[99,100,101,...|
|  0.0|(780,[154,155,156...|
|  0.0|(780,[127,128,129...|
+-----+--------------------+
only showing top 10 rows

{% endhighlight %}


{% highlight java %}

Dataset<Row> df = spark.read.format("libsvm").option("numFeatures", "780").load("data/mllib/sample_libsvm_data.txt");
df.show(10);
/*
Will output:
+-----+--------------------+
|label|            features|
+-----+--------------------+
|  0.0|(780,[127,128,129...|
|  1.0|(780,[158,159,160...|
|  1.0|(780,[124,125,126...|
|  1.0|(780,[152,153,154...|
|  1.0|(780,[151,152,153...|
|  0.0|(780,[129,130,131...|
|  1.0|(780,[158,159,160...|
|  1.0|(780,[99,100,101,...|
|  0.0|(780,[154,155,156...|
|  0.0|(780,[127,128,129...|
+-----+--------------------+
only showing top 10 rows
*/

{% endhighlight %}


{% highlight python %}

>>> df = spark.read.format("libsvm").option("numFeatures", "780").load("data/mllib/sample_libsvm_data.txt")
>>> df.show(10)
+-----+--------------------+
|label|            features|
+-----+--------------------+
|  0.0|(780,[127,128,129...|
|  1.0|(780,[158,159,160...|
|  1.0|(780,[124,125,126...|
|  1.0|(780,[152,153,154...|
|  1.0|(780,[151,152,153...|
|  0.0|(780,[129,130,131...|
|  1.0|(780,[158,159,160...|
|  1.0|(780,[99,100,101,...|
|  0.0|(780,[154,155,156...|
|  0.0|(780,[127,128,129...|
+-----+--------------------+
only showing top 10 rows

{% endhighlight %}


{% highlight r %}

> df = read.df("data/mllib/sample_libsvm_data.txt", "libsvm")
> head(select(df, df$label, df$features), 10)

   label                      features
1      0 <environment: 0x7fe6d35366e8>
2      1 <environment: 0x7fe6d353bf78>
3      1 <environment: 0x7fe6d3541840>
4      1 <environment: 0x7fe6d3545108>
5      1 <environment: 0x7fe6d354c8e0>
6      0 <environment: 0x7fe6d35501a8>
7      1 <environment: 0x7fe6d3555a70>
8      1 <environment: 0x7fe6d3559338>
9      0 <environment: 0x7fe6d355cc00>
10     0 <environment: 0x7fe6d35643d8>

{% endhighlight %}