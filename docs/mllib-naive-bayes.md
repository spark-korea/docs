|layout|title|displayTitle|
|--|--|--|
| global | Naive Bayes - RDD-based API|Naive Bayes - RDD-based API

해당 페이지에서는 MLlib의 Naive Bayes에 대해 설명합니다. 

##

Naive Bayes는 모든 특징 쌍 사이의 독립성을 가정하는 간단한 다중 클래스 분류 알고리즘입니다. Naive Bayes는 매우 효율적으로 훈련될 수 있습니다. 훈련 데이터에 대해 단일 패스 내에서, 이것은 주어진 각 피처의 조건부 확률 분포를 계산한 다음 Bayes' theorem를 적용하여 주어진 관측치의 조건부 확률 분포를 계산하고 예측에 사용합니다. 

`spark.mllib` 은  [multinomial navie Bayes](http://en.wikipedia.org/wiki/Naive_Bayes_classifier#Multinomial_naive_Bayes) 와 [Bernoulli navie Bayes](http://nlp.stanford.edu/IR-book/html/htmledition/the-bernoulli-model-1.html)를 지원합니다. 이러한 모델은 일반적으로 [document classification](http://nlp.stanford.edu/IR-book/html/htmledition/naive-bayes-text-classification-1.html) 에서 사용됩니다. 이 맥락에서, 각각의 관측치는 문서이고, 각 특징은 (multinomial navie Bayes) 용어의 빈도 또는 (Bernoulli navie Bayes) 용어의 발견 여부를 나타내는 0또는 1의 값이 나타나는 항을 표현합니다. 피처 값은 음수가 아니어야 합니다. 모델 유형은 선택적 매개변수인 "multinomial" 또는 "bernoulli"를 기본 값으로 사용하여 선택됩니다. [Additive smoothing](http://en.wikipedia.org/wiki/Lidstone_smoothing) 은 매개변수 
$\lambda$ (default to $1.0$) 를 설정해서 사용합니다. 문서 분류를 위해 입력 특징 벡터는 일반적으로 희소하며 희소성을 이용하기 위해서는 희소 벡터가 입력으로 제공되어야 합니다. 훈련 데이터는 한 번만 사용되므로 캐시할 필요가 없습니다. 

## 예제
<div class="codetabs">
<div data-lang="scala" markdown="1">

[NaiveBayes](https://github.com/apache/spark/blob/master/docs/api/scala/org/apache/spark/mllib/classification/NaiveBayes$.html) 는 multinomial naive Bayes를 구현합니다. 이것은 
[LabeledPoint](https://github.com/apache/spark/blob/master/docs/api/scala/org/apache/spark/mllib/regression/LabeledPoint.html)의 RDD와 선택적 평활 매개변수 `lambda`를 입력으로 사용하고, 선택적 모델 유형 매개변수 (기본값 "다항식")를 사용하며, 평가 및 예측에 사용할 수 있는 [NaiveBayesModel](https://github.com/apache/spark/blob/master/docs/api/scala/org/apache/spark/mllib/classification/NaiveBayesModel.html)을 출력합니다.

API에 대한 자세한 내용은 [`NaiveBayes`  Scala 문서](https://github.com/apache/spark/blob/master/docs/api/scala/org/apache/spark/mllib/classification/NaiveBayes$.html) 와 [`NaiveBayesModel`  Scala 문서](https://github.com/apache/spark/blob/master/docs/api/scala/org/apache/spark/mllib/classification/NaiveBayesModel.html)를 참조하세요.

{% include_example scala/org/apache/spark/examples/mllib/NaiveBayesExample.scala %}

[NaiveBayes](https://github.com/apache/spark/blob/master/docs/api/java/org/apache/spark/mllib/classification/NaiveBayes.html) 는 
multinomial naive Bayes를 구현합니다. [LabeledPoint](https://github.com/apache/spark/blob/master/docs/api/java/org/apache/spark/mllib/regression/LabeledPoint.html)의 RDD와 선택적으로 평활화 매개 변수 람다를 입력으로 사용하고 평가 및 예측에 사용할 수 있는 [NaiveBayesModel](https://github.com/apache/spark/blob/master/docs/api/java/org/apache/spark/mllib/classification/NaiveBayesModel.html)을 출력합니다. 

Python API는 아직 모델 저장/로드 기능을 지원하지 않지만 향후 지원될 예정입니다. 

API에 대한 자세한 내용은 [`NaiveBayes`  Python 문서](https://github.com/apache/spark/blob/master/docs/api/python/reference/api/pyspark.mllib.classification.NaiveBayes.html) and [`NaiveBayesModel`  Python 문서](https://github.com/apache/spark/blob/master/docs/api/python/reference/api/pyspark.mllib.classification.NaiveBayesModel.html)를 참조하세요. 

{% include_bython python/mllib/mlib_bayes_byes_py %}
