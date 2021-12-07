|layout|title|displayTitle|
|--|--|--|
| global | Basic Statistics |Basic Statistics

해당 페이지에서는 MLlib의 Statistics에 대해 설명합니다. 

## 상관관계

두 데이터 열 사이의 상관 관계를 계산하는 것은 Statistics에서 일반적인 작업입니다. `spark.ml` 에서는 많은 시리즈 간의 쌍별 상관관계를 계산할 수 있는 유연성을 지원합니다. 지원되는 상관 관계는 현재는 Pearson's 와 Spearman's 가 있습니다. 

[Correlation](https://spark.apache.org/docs/2.2.0/api/java/org/apache/spark/ml/stat/Correlation.html) 
