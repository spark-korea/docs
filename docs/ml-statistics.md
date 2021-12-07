|layout|title|displayTitle|
|--|--|--|
| global | Basic Statistics |Basic Statistics

해당 페이지에서는 MLlib의 Statistics에 대해 설명합니다. 

## 상관관계

두 데이터 열 사이의 상관 관계를 계산하는 것은 Statistics에서 일반적인 작업입니다. `spark.ml` 에서는 많은 시리즈 간의 쌍별 상관관계를 계산할 수 있는 유연성을 지원합니다. 지원되는 상관 관계는 현재는 Pearson's 와 Spearman's 가 있습니다. 

[Correlation](api/scala/org/apache/spark/ml/stat/Correlation$.html) 은 지정된 방법을 사용하여 벡터의 입력 Dataset에 대한 상관 행렬을 계산합니다. 출력은 벡터 열의 상관 행렬이 포함된 DataFrame이 됩니다. 

{% include_example scala/org/apache/spark/examples/ml/CorrelationExample.scala %}

[Correlation](api/java/org/apache/spark/ml/stat/Correlation.html) 은 지정된 방법을 사용하여 벡터의 입력 Dataset에 대한 상관 행렬을 계산합니다. 출력은 벡터 열의 상관 행렬이 포함된 DataFrame이 됩니다. 

{% include_example java/org/apache/spark/examples/ml/JavaCorrelationExample.java %}

[Correlation](api/python/reference/api/pyspark.ml.stat.Correlation.html) 은 지정된 방법을 사용하여 벡터의 입력 Dataset에 대한 상관 행렬을 계산합니다. 출력은 벡터 열의 상관 행렬이 포함된 DataFrame이 됩니다. 

{% include_example python/ml/correlation_example.py %}
