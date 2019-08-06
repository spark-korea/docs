---
layout: global
title: 빠른 시작
description: Quick start tutorial for Spark SPARK_VERSION_SHORT
---

* This will become a table of contents (this text will be scraped).
{:toc}

이 튜토리얼에서는 스파크의 사용법을 간단히 소개합니다. 먼저 스파크의 대화형 셸(Scala, Python 지원)에서 사용하는 API를 먼저 소개한 후에 애플리케이션을 만드는 법(Scala, Python 지원)을 알아보겠습니다.

따라서 해보시기 전에, 먼저 [스파크 웹사이트](https://spark.apache.org/downloads.html)에서 스파크 패키지를 다운로드하셔야 합니다. 다운로드 메뉴를 보면 Hadoop 버전을 선택하도록 되어 있는데, 여기서 HDFS를 사용하지 않을 것이기 때문에 아무 것이나 선택해도 상관 없습니다.

스파크 2.0 이전까지는 RDD(Resilient Distributed Dataset)가 주 프로그래밍 인터페이스로 사용되었습니다. 스파크 2.0 이후부터 주 프로그래밍 인터페이스가 RDD에서 Dataset으로 교체되었는데, 이 Dataset은 RDD와 비슷하지만 강한 타입체크(strongly-typed)를 지원하고 훨씬 최적화되어 있습니다. RDD 인터페이스는 여전히 사용 가능하며 [RDD 프로그래밍 가이드(영문)](https://spark.apache.org/docs/latest/rdd-programming-guide.html)에서 자세한 내용을 확인하실 수 있습니다. 하지만 여기에서는 RDD보다 훨씬 좋은 성능을 보여주는 Dataset을 사용할 것을 강력히 권장합니다. [SQL 프로그래밍 가이드](sql-programming-guide.html)에서 Dataset에 대한 자세한 정보를 얻을 수 있습니다.

# 보안

스파크의 보안 기능은 기본적으로 꺼져 있습니다. 즉, 외부 침입에 취약할 수밖에 없다는 얘기죠. 테스트 삼아 로컬에서 돌려 보는 것은 상관이 없습니다만, 실제 운영 환경에 설정하시기 전에는 반드시 [스파크 보안](security.html) 문서를 확인하세요.

# 스파크 셸(Shell)을 이용한 대화형 분석

## 기초

스파크 셸은 스파크 API를 쉽게 익히는 용도 뿐만 아니라, 데이터를 대화형으로 분석할 때 강력한 도구로 사용할 수 있습니다. Scala(Java VM에서 실행되므로 Java 라이브러리 또한 사용할 수 있습니다) 또는 Python 에서 사용할 수 있습니다. 스파크를 다운로드 받은 디렉토리 내에서 아래와 같이 실행하여 시작할 수 있습니다.

<div class="codetabs">
<div data-lang="scala" markdown="1">

    ./bin/spark-shell

스파크에서 가장 기본적인 개념은 Dataset이라고 불리는 분산 컬렉션(distributed collection)입니다. Dataset은 Hadoop InputFormat(HDFS 파일)으로부터 만들어지거나 다른 Dataset을 변환하여 만들어집니다. 이제 스파크 소스 디렉토리 내의 README 파일의 텍스트를 가지고 새로운 Dataset을 만들어보겠습니다:

{% highlight scala %}
scala> val textFile = spark.read.textFile("README.md")
textFile: org.apache.spark.sql.Dataset[String] = [value: string]
{% endhighlight %}

이 Dataset에서 특정한 액션(action)을 호출해서 어떠한 값을 얻을 수도 있고, 트랜스포메이션(transformation)을 호출해서 새로운 Dataset으로 변환할 수도 있습니다. 자세한 내용은 [API 문서](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset)에서 확인할 수 있습니다.

{% highlight scala %}
scala> textFile.count() // Number of items in this Dataset
res0: Long = 126 // May be different from yours as README.md will change over time, similar to other outputs

scala> textFile.first() // First item in this Dataset
res1: String = # Apache Spark
{% endhighlight %}

이제 이 Dataset을 새로운 DataSet으로 변환해보겠습니다. `filter`를 호출하여 파일 내용의 일부만을 가지는 새로운 Dataset을 생성합니다.

{% highlight scala %}
scala> val linesWithSpark = textFile.filter(line => line.contains("Spark"))
linesWithSpark: org.apache.spark.sql.Dataset[String] = [value: string]
{% endhighlight %}

액션(action)과 트랜스포메이션(transformation)을 연결해서 호출할 수도 있습니다:

{% highlight scala %}
scala> textFile.filter(line => line.contains("Spark")).count() // "Spark"를 포함하는 라인의 개수
res3: Long = 15
{% endhighlight %}

</div>
<div data-lang="python" markdown="1">

    ./bin/pyspark


만약 pip로 PySpark를 설치했다면 아래와 같이 실행합니다:

    pyspark

스파크에서 가장 기본적인 개념은 Dataset이라고 불리는 분산 컬렉션(distributed collection)입니다. Dataset은 Hadoop InputFormat(HDFS 파일)으로부터 만들어지거나 다른 Dataset을 변형하여 만들어집니다. 동적으로 타입 검사를 수행하는 Python의 특성 때문에 Python에서는 Dataset에서 강한 타입 체크가 필요하지 않습니다. 따라서 Python에서 사용하는 모든 Dataset은 DataSet[Row]의 형태입니다. 이것을 `DataFrame`이라고 부르는데 Pandas와 R에서 사용하는 DataFrame과 같은 개념입니다. 이제 스파크 소스 디렉토리 내의 README 파일의 텍스트를 이용하여 새로운 Dataset을 만들어보겠습니다:

{% highlight python %}
>>> textFile = spark.read.text("README.md")
{% endhighlight %}

이 Dataset에서 특정한 명령어로 어떠한 값을 얻을 수도 있고, 새로운 Dataset으로 변환할 수도 있습니다. 자세한 내용은 _[API 문서](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset)_에서 확인할 수 있습니다.

{% highlight python %}
>>> textFile.count()  # DataFrame포함된 열(row)의 개수
126

>>> textFile.first()  # DataFrame의 첫 번째 열(row)
Row(value=u'# Apache Spark')
{% endhighlight %}

이제 이 DataFrame을 새로운 DataFrame으로 변환해보겠습니다. `filter`를 호출하여 파일 내용의 일부만을 가지는 새로운 Dataset을 생성합니다.

{% highlight python %}
>>> linesWithSpark = textFile.filter(textFile.value.contains("Spark"))
{% endhighlight %}

특정 동작과 변환을 연속해서 사용할 수도 있습니다:

{% highlight python %}
>>> textFile.filter(textFile.value.contains("Spark")).count()  # How many lines contain "Spark"?
15
{% endhighlight %}

</div>
</div>


## Dataset 활용에 대해 더 알아보기
Dataset 액션(action)과 트랜스포메이션(transformation)을 사용해서 더 복잡한 연산을 수행할 수도 있습니다. 여기에서는 가장 많은 단어를 포함한 라인을 찾아보겠습니다:

<div class="codetabs">
<div data-lang="scala" markdown="1">

{% highlight scala %}
scala> textFile.map(line => line.split(" ").size).reduce((a, b) => if (a > b) a else b)
res4: Long = 15
{% endhighlight %}

먼저 각 라인을 각 정수값에 대응시켜 새로운 Dataset을 생성합니다. `reduce`는 이 Dataset에서 가장 큰 단어 수를 찾기 위해 호출됩니다. `map`과 `reduce`의 인수는 Scala 함수 리터럴(클로져)이며, Scala 언어의 기능뿐만 아니라 Scala/Java 라이브러리 역시 사용할 수 있습니다. 예를 들어, 다른 곳에 선언된 함수도 호출할 수 있습니다. 이 코드를 더 쉽게 이해할 수 있도록 하기 위해 `Math.max()` 함수를 사용해보겠습니다.

{% highlight scala %}
scala> import java.lang.Math
import java.lang.Math

scala> textFile.map(line => line.split(" ").size).reduce((a, b) => Math.max(a, b))
res5: Int = 15
{% endhighlight %}

가장 흔한 데이터 처리 패턴 중 하나는 Hadoop 덕분에 유명해진 MapReduce 패턴입니다. 스파크에서는 이 MapReduce 패턴 데이터 처리를 쉽게 구현할 수 있습니다:

{% highlight scala %}
scala> val wordCounts = textFile.flatMap(line => line.split(" ")).groupByKey(identity).count()
wordCounts: org.apache.spark.sql.Dataset[(String, Long)] = [value: string, count(1): bigint]
{% endhighlight %}

여기에서 `flatMap` 을 호출하여 각 라인로 이루어진 Dataset을 각 단어로 이루어진 Dataset으로 변환합니다. 그리고 `groupByKey` 와 `count`를 차례로 호출하여 이 파일에 포함된 각 단어별 개수를 (String, Long) 페어(pair)로 이루어진 Dataset으로 만듭니다. 셸에서 각 단어의 개수를 구하기 위해서 `collect`를 호출합니다:

{% highlight scala %}
scala> wordCounts.collect()
res6: Array[(String, Int)] = Array((means,1), (under,2), (this,3), (Because,1), (Python,2), (agree,1), (cluster.,1), ...)
{% endhighlight %}

</div>
<div data-lang="python" markdown="1">

{% highlight python %}
>>> from pyspark.sql.functions import *
>>> textFile.select(size(split(textFile.value, "\s+")).name("numWords")).agg(max(col("numWords"))).collect()
[Row(max(numWords)=15)]
{% endhighlight %}

먼저 각 라인을 각 정수값에 대응시켜서 이것을 “numWords”라고 이름 붙여 새로운 DataFrame을 생성합니다. `agg`를 호출하면 DataFrame에서 가장 큰 단어의 개수를 찾을 수 있습니다. select와 agg의 인수는 [*컬럼*](https://spark.apache.org/docs/latest/api/python/index.html#pyspark.sql.Column)으로 이루어지는데, df.colName을 사용하면 DataFrame으로부터 각 로우(row)를 얻을 수 있습니다. pyspark.sql.functions 을 임포트하면 한 Column으로 부터 새로운 Column을 만들 수 있는 편리한 함수들을 사용할 수 있습니다.

이 MapReduce는 Hadoop에서 자주 사용되는 흔한 데이터 플로우 패턴 중 하나입니다. 스파크에서는 MapReduce 플로우를 쉽게 구현할 수 있습니다:

{% highlight python %}
>>> wordCounts = textFile.select(explode(split(textFile.value, "\s+")).alias("word")).groupBy("word").count()
{% endhighlight %}

여기서는 select 내부에서 explode를 사용하여 각 라인로 이루어진 Dataset을 각 단어로 이루어진 Dataset으로 변환합니다. 그리고 `groupByKey` 와 `count`를 함께 사용하여 이 파일에 포함된 각 단어의 개수를 2개의 컬럼(각 단어와 개수)으로 이루어진 DataFrame으로 만듭니다. 셸에서 각 단어의 개수를 구하기 위해서 `collect`를 호출합니다:

{% highlight python %}
>>> wordCounts.collect()
[Row(word=u'online', count=1), Row(word=u'graphs', count=1), ...]
{% endhighlight %}

</div>
</div>

## 캐싱
스파크는 클러스터 단위 인-메모리 캐시(in-memory cache)에서 데이터셋을 가져올 수 있는 기능을 지원합니다. 이 기능은 PageRank 알고리즘과 같은 반복적인 알고리즘을 실행하거나 크기는 작지만 자주 변하는 데이터셋을 쿼리할 때와 같이 특정 데이터에 반복적으로 접근하고자 할 때 매우 유용합니다. 간단한 예로, linesWithSpark Dataset을 캐시해보겠습니다.

<div class="codetabs">
<div data-lang="scala" markdown="1">

{% highlight scala %}
scala> linesWithSpark.cache()
res7: linesWithSpark.type = [value: string]

scala> linesWithSpark.count()
res8: Long = 15

scala> linesWithSpark.count()
res9: Long = 15
{% endhighlight %}

100라인짜리 텍스트 파일을 탐색하고 캐시하기 위해 스파크를 사용하는 것이 불필요해 보일 수 있습니다. 여기서 주목해야 할 점은 매우 큰 데이터셋에서도 이 작은 크기의 데이터셋에 사용된 것과 동일한 함수를 사용할 수 있다는 것입니다. 수십, 수백 개의 노드로 이루어져 있을 때에도 사용할 수 있습니다. 또한 `bin/spark-shell`을 클러스터에 연결해서 대화형으로 사용할 수도 있습니다. 이것에 대한 내용은 [RDD 프로그래밍 가이드(영문)](https://spark.apache.org/docs/latest/rdd-programming-guide.html#using-the-shell)에 설명되어 있습니다.

</div>
<div data-lang="python" markdown="1">

{% highlight python %}
>>> linesWithSpark.cache()

>>> linesWithSpark.count()
15

>>> linesWithSpark.count()
15
{% endhighlight %}

100라인짜리 텍스트 파일을 탐색하고 캐시하기 위해 스파크를 사용하는 것이 불필요해 보일 수 있습니다. 여기서 흥미로운 점은 매우 큰 데이터셋에서도 똑같은 함수를 사용할 수 있다는 것입니다. 수십, 수백 개의 노드로 이루어져 있을 때에도 사용할 수 있습니다. 또한 `bin/spark-shell`을 클러스터에 연결해서 대화형으로 사용할 수도 있습니다. 이것에 대한 내용은 [RDD 프로그래밍 가이드(영문)](https://spark.apache.org/docs/latest/rdd-programming-guide.html#using-the-shell)에 설명되어 있습니다.

</div>
</div>

# 독립형 애플리케이션
스파크 API를 사용해서 독립형 애플리케이션을 만드는 상황이라고 가정하고, Scala(sbt), Python(pip)으로 간단한 애플리케이션을 만들어보겠습니다.

<div class="codetabs">
<div data-lang="scala" markdown="1">

예제로 `SimpleApp.scala`라는 이름의 매우 간단한 Scala 스파크 애플리케이션을 만들어 보겠습니다.

{% highlight scala %}
/* SimpleApp.scala */
import org.apache.spark.sql.SparkSession

object SimpleApp {
  def main(args: Array[String]) {
    val logFile = "YOUR_SPARK_HOME/README.md" // 여러분의 시스템 내에 존재하는 파일이어야 합니다
    val spark = SparkSession.builder.appName("Simple Application").getOrCreate()
    val logData = spark.read.textFile(logFile).cache()
    val numAs = logData.filter(line => line.contains("a")).count()
    val numBs = logData.filter(line => line.contains("b")).count()
    println(s"Lines with a: $numAs, Lines with b: $numBs")
    spark.stop()
  }
}
{% endhighlight %}

Scala에서는 실행 가능한 애플리케이션을 만드는 방법이 두 가지가 있습니다: scala.App 을 확장한 object를 정의하는 방법과 `main` 메소드가 정의된 object를 정의하는 방법. 여기에서는 전자가 아니라 후자를 택해야 합니다. 전자는 제대로 동작하지 않을 수 있습니다.

이 프로그램은 스파크 README 파일에서 ‘a’ 를 포함하는 라인의 개수와 ‘b’를 포함하는 라인의 개수를 세는 프로그램입니다. 여기에서 YOUR_SPARK_HOME을 여러분의 스파크가 설치된 경로로 바꾸어 줍니다. 이전 예제에서는 스파크 셸에서 SparkSession을 초기화했지만, 여기에서는 프로그램 내에서 SparkSession을 초기화합니다.

[[SparkSession]]을 생성하기 위해서 `SparkSession.builder`를 호출합니다. 그리고 애플리케이션의 이름을 정하고 마지막으로 `getOrCreate`를 호출하여 [[SparkSession]] 인스턴스를 얻습니다.

이 애플리케이션은 스파크 API를 기반으로 하기 때문에, 스파크에 대한 의존성을 정의하는 sbt 설정 파일인 build.sbt를 포함시킬 수 있습니다. 스파크가 배포되는 라이브러리 저장소에 대한 정보 역시 이 파일에 설정합니다.

{% highlight scala %}
name := "Simple Project"

version := "1.0"

scalaVersion := "{{site.SCALA_VERSION}}"

libraryDependencies += "org.apache.spark" %% "spark-sql" % "{{site.SPARK_VERSION}}"
{% endhighlight %}

sbt가 제대로 동작하게 하기 위해서는 `SimpleApp.scala`와 `build.sbt` 파일이 올바른 디렉토리 구조에 저장되도록 해야 합니다. 파일이 포함된 디렉토리 구조에 문제가 없어야 애플리케이션 코드를 포함하는 JAR 패키지를 생성하고, `spark-submit` 스크립트를 사용하여 프로그램을 실행할 수 있습니다.

{% highlight bash %}
# 프로젝트가 아래와 같이 메이븐 표준 디렉토리 구조(Apache maven standard directory layout)를 가져야 합니다
$ find .
.
./build.sbt
./src
./src/main
./src/main/scala
./src/main/scala/SimpleApp.scala

# 애플리케이션을 포함하는 jar 패키지를 생성합니다
$ sbt package
...
[info] Packaging {..}/{..}/target/scala-{{site.SCALA_BINARY_VERSION}}/simple-project_{{site.SCALA_BINARY_VERSION}}-1.0.jar

# spark-submit을 사용하여 애플리케이션을 실행합니다
$ YOUR_SPARK_HOME/bin/spark-submit \
  --class "SimpleApp" \
  --master local[4] \
  target/scala-{{site.SCALA_BINARY_VERSION}}/simple-project_{{site.SCALA_BINARY_VERSION}}-1.0.jar
...
Lines with a: 46, Lines with b: 23
{% endhighlight %}

</div>
<div data-lang="python" markdown="1">

이제 Python API(PySpark)를 이용하여 애플리케이션을 작성하는 방법을 알아보겠습니다.


PySpark 패키지 애플리케이션 또는 라이브러리를 만들고자 한다면 setup.py 파일에 아래의 내용을 추가합니다.

{% highlight python %}
    install_requires=[
        'pyspark=={site.SPARK_VERSION}'
    ]
{% endhighlight %}


예제로 `SimpleApp.py`라는 간단한 스파크 애플리케이션을 만들어보겠습니다.

{% highlight python %}
"""SimpleApp.py"""
from pyspark.sql import SparkSession

logFile = "YOUR_SPARK_HOME/README.md"  # 여러분의 시스템 내에 존재하는 파일이어야 합니다
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
logData = spark.read.text(logFile).cache()

numAs = logData.filter(logData.value.contains('a')).count()
numBs = logData.filter(logData.value.contains('b')).count()

print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

spark.stop()
{% endhighlight %}


이 프로그램은 스파크 README 파일에서 ‘a’ 을 포함하는 라인의 개수와 ‘b’를 포함하는 라인의 개수를 세는 프로그램입니다. 여기에서 YOUR_SPARK_HOME을 여러분의 스파크가 설치된 경로로 바꿔 주어야 합니다. Scala 예제에서와 같이, SparkSession을 사용하여 Dataset을 생성합니다. custom class 또는 써드파티 라이브러리를 사용하는 애플리케이션에서는 `spark-submit`에 의존성을 추가할 수 있습니다. 여기에서는 `--py--files` 인자를 사용하여 .zip 파일로 패키징하게 됩니다.(자세한 내용은 `spark-submint --help`를 실행하면 볼 수 있습니다). 이 `SimpleApp`에서는 간단하기 때문에 다른 코드 의존성을 명시할 필요가 없습니다.

`bin/saprk-submint` 스크립트를 사용하여 이 애플리케이션을 실행할 수 있습니다:

{% highlight bash %}
# spark-submit을 사용하여 애플리케이션을 실행합니다
$ YOUR_SPARK_HOME/bin/spark-submit \
  --master local[4] \
  SimpleApp.py
...
Lines with a: 46, Lines with b: 23
{% endhighlight %}

만약 여러분의 개발 환경에 PySpark를 pip로 설치했다면(e.g., `pip install pyspark`), Python 인터프리터를 사용하거나 `spark-submit`를 사용하는 방법 중 하나를 선택하여 애플리케이션을 실행할 수 있습니다.

{% highlight bash %}
# Python 인터프리터를 사용하여 애플리케이션을 실행합니다
$ python SimpleApp.py
...
Lines with a: 46, Lines with b: 23
{% endhighlight %}

</div>
</div>

# 더 자세한 내용이 알고 싶다면
첫 번째 스파크 애플리케이션을 성공적으로 실행하신 것을 축하드립니다!

* API에 대한 상세한 내용은  [RDD 프로그래밍 가이드](https://spark.apache.org/docs/latest/rdd-programming-guide.html)와 [SQL 프로그래밍 가이드](https://spark.apache.org/docs/latest/sql-programming-guide.html)에서 볼 수 있습니다. 또는 “프로그래밍 가이드” 메뉴의 다른 장에서 볼 수 있습니다.
* 클러스터에서 애플리케이션을 실행하는 것은 [클러스터 모드 개요](https://spark.apache.org/docs/latest/cluster-overview.html)를 참고하세요.
* 마지막으로, 스파크는 examples 디렉토리에 다양한 예제를 포함하고 있습니다. ([Scala](https://github.com/apache/spark/tree/master/examples/src/main/scala/org/apache/spark/examples), [Java](https://github.com/apache/spark/tree/master/examples/src/main/java/org/apache/spark/examples), [Python](https://github.com/apache/spark/tree/master/examples/src/main/python), [R](https://github.com/apache/spark/tree/master/examples/src/main/r)). 아래와 같이 실행할 수 있습니다:

{% highlight bash %}
# Scala 예제의 경우 run-example을 사용합니다:
./bin/run-example SparkPi

# Python 예제의 경우 spark-submit를 사용합니다:
./bin/spark-submit examples/src/main/python/pi.py

# R 예제의 경우 spark-submit를 사용합니다:
./bin/spark-submit examples/src/main/r/dataframe.R
{% endhighlight %}
