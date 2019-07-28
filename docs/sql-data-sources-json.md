---
layout: global
title: JSON 파일
displayTitle: JSON 파일
---

<div class="codetabs">

<div data-lang="scala"  markdown="1">
스파크 SQL은 JSON dataset의 스키마(schema)를 자동으로 추론하여 `Dataset[Row]`로 로드할 수 있습니다. 이러한 변환은 `Dataset[String]이나 `JSON 파일의 `SparkSession.read.json()`을 호출하여 사용할 수 있습니다.

여기서의 _json 파일_은 일반적인 JSON 파일이 아닙니다. 각 라인에는 각각 독립적이고 그 자체로 유효한 JSON 객체가 들어 있어야 합니다. 자세한 정보는 [(newline-delimited JSON이라고도 불리는) JSON 라인 텍스트 형식](http://jsonlines.org/)을 참고하세요.

일반적인 multi-line JSON 파일의 경우, `multiLine `옵션을 `true`로 설정하시면 됩니다.

{% include_example json_dataset scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala %}
</div>

<div data-lang="python"  markdown="1">
스파크 SQL은 JSON dataset의 스키마(schema)를 자동으로 추론하여 `Dataset[Row]`로 로드할 수 있습니다. 이러한 변환은 JSON 파일의 `SparkSession.read.json()`을 호출하여 사용할 수 있습니다.

여기서의 _json 파일_은 일반적인 JSON 파일이 아닙니다. 각 라인에는 각각 독립적이고 그 자체로 유효한 JSON 객체가 들어 있어야 합니다. 자세한 정보는 [(newline-delimited JSON이라고도 불리는) JSON 라인 텍스트 형식](http://jsonlines.org/)을 참고하세요.

일반적인 multi-line JSON 파일의 경우, `multiLine `옵션을 `true`로 설정하시면 됩니다.

{% include_example json_dataset python/sql/datasource.py %}
</div>

<div data-lang="sql"  markdown="1">

{% highlight sql %}

CREATE TEMPORARY VIEW jsonTable
USING org.apache.spark.sql.json
OPTIONS (
  path "examples/src/main/resources/people.json"
)

SELECT * FROM jsonTable

{% endhighlight %}

</div>

</div>
