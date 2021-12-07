|layout|title|displayTitle|
|--|--|--|
| global | Basic Statistics |Basic Statistics

해당 페이지에서는 MLlib의 Statistics에 대해 설명합니다. 

## 상관관계

두 데이터 열 사이의 상관 관계를 계산하는 것은 Statistics에서 일반적인 작업입니다. `spark.ml` 에서는 많은 시리즈 간의 쌍별 상관관계를 계산할 수 있는 유연성을 지원합니다. 지원되는 상관 관계는 현재는 Pearson 과 Spearman 가 있습니다. 

[Correlation](api/scala/org/apache/spark/ml/stat/Correlation$.html) 은 지정된 방법을 사용하여 벡터의 입력 Dataset에 대한 상관 행렬을 계산합니다. 출력은 벡터 열의 상관 행렬이 포함된 DataFrame이 됩니다. 

{% include_example scala/org/apache/spark/examples/ml/CorrelationExample.scala %}

[Correlation](api/java/org/apache/spark/ml/stat/Correlation.html) 은 지정된 방법을 사용하여 벡터의 입력 Dataset에 대한 상관 행렬을 계산합니다. 출력은 벡터 열의 상관 행렬이 포함된 DataFrame이 됩니다. 

{% include_example java/org/apache/spark/examples/ml/JavaCorrelationExample.java %}

[Correlation](api/python/reference/api/pyspark.ml.stat.Correlation.html) 은 지정된 방법을 사용하여 벡터의 입력 Dataset에 대한 상관 행렬을 계산합니다. 출력은 벡터 열의 상관 행렬이 포함된 DataFrame이 됩니다. 

{% include_example python/ml/correlation_example.py %}

## 가설 검정
가설 검정은 결과가 통계적으로 유의미한지 여부 또는 결과가 우연히 발생했는지 여부를 결정하는 강력한 통계 도구 입니다. `spark.ml`은 독립성에 대해 현제 Pearson의 Chi-Squared ( $\chi^2$)  테스트를 지원합니다.

### ChiSquareTest
ChiSqaureTest는 레이블에 대해 모든 피처에 대해 Pearson의 독립성 검증을 수행합니다. 각 피처에 대해(피처, 레이블) 쌍은 Chi-Squared 통계량이 계산되는 분할 행렬로 변환됩니다. 모든 레이블 및 피처 값은 범주형이어야 합니다. 

API에 대한 자세한 내용은 [`ChiSquareTest` Scala 문서](api/scala/org/apache/spark/ml/stat/ChiSquareTest$.html) 를 참조하세요. 

{% include_example scala/org/apache/spark/examples/ml/ChiSquareTestExample.scala %}

[`ChiSquareTest` Java 문서](api/java/org/apache/spark/ml/stat/ChiSquareTest.html) 를 참조하세요. 

{% include_example java/org/apache/spark/examples/ml/JavaChiSquareTestExample.java %}

[`ChiSquareTest` Python 문서](api/python/reference/api/pyspark.ml.stat.ChiSquareTest.html)를 참조하세요. 

{% include_example python/ml/chi_square_test_example.py %}

## 요약자
`Summarizer(요약자)`를 통해 `Dataframe`에 대한 벡터 열 요약 통계를 제공합니다.  사용 가능한 메트릭은 열 단위 최대값, 최소값, 평균, 합계, 분산, 표준값 및 0이 아닌 값의 수와 총 갯수입니다. 

다음 예는 가중치 열이 있는 경우와 없는 경우 입력  DataFrame의 벡터 열에 대한 평균과 분산을 계산하기 위해 [`Summarizer`](api/scala/org/apache/spark/ml/stat/Summarizer$.html)를 사용하는 것을 보여줍니다. 

{% include_example scala/org/apache/spark/examples/ml/SummarizerExample.scala %}

다음 예는 가중치 열이 있는 경우와 없는 경우 입력  DataFrame의 벡터 열에 대한 평균과 분산을 계산하기 위해 [`Summarizer`](api/java/org/apache/spark/ml/stat/Summarizer.html) 를 사용하는 것을 보여줍니다. 

{% include_example java/org/apache/spark/examples/ml/JavaSummarizerExample.java %}

API에 대한 자세한 내용은 [`Summarizer` Python 문서](api/python/reference/api/pyspark.ml.stat.Summarizer.html) 를 참조하세요. 

{% include_example python/ml/summarizer_example.py %}
