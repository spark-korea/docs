---
layout: global
title: "ML Tuning"
displayTitle: "ML Tuning: model selection and hyperparameter tuning"
---


해당 섹션에서는 ML 알고리즘 및 파이프라인을 튜닝하기 위해 MLlib의 툴을 사용하는 방법을 설명합니다.
내장된 교차 검증 및 기타 툴을 통해 사용자는 알고리즘 및 파이프라인에서 하이퍼파라미터를 최적화할 수 있습니다.


# 모델 선택 (a.k.a. 하이퍼파라미터 튜닝)

ML에서 중요한 작업은 *모델 선택* 또는 데이터를 사용하여 주어진 작업에 가장 적합한 모델 혹은 파라미터를 찾는 것입니다. 이것을 *튜닝*이라고도 합니다.
튜닝은 `LogisticRegression`과 같은 개별 `Estimator` 또는 다중 알고리즘, 기능화 및 기타 단계를 포함하는 전체 `Pipeline`에 대해 수행될 수 있습니다. 사용자는 `Pipeline`의 각 요소를 개별적으로 조정하는 대신 전체 `Pipeline`을 한 번에 조정할 수 있습니다.

MLlib는 [`CrossValidator`](api/scala/org/apache/spark/ml/tuning/CrossValidator.html) 및 [`TrainValidationSplit`](api/scala/org/apache/spark/ml/tuning/TrainValidationSplit.html) 과 같은 도구를 사용하여 모델 선택을 지원합니다. 이러한 툴은 다음 항목을 필요로 합니다.

* [`Estimator`](api/scala/org/apache/spark/ml/Estimator.html): 조정할 알고리즘 또는 `Pipeline`
* `ParamMap` 세트: 선택할 파라미터, 검색을 위한 "parameter grid"라고도 함
* [`Evaluator`](api/scala/org/apache/spark/ml/evaluation/Evaluator.html): 적합화된 `Model`이 보류된 테스트 데이터에 대해 얼마나 잘 수행하는지 측정하기 위한 메트릭

상위 수준에서 이러한 모델 선택 툴은 다음과 같이 작동합니다:

* 입력 데이터를 별도의 훈련 및 테스트 데이터셋로 분할합니다.
* 각 (training, test) 쌍에 대해 `ParamMap` 세트를 반복합니다:
  * 각 `ParamMap`에 대해 해당 파라미터를 사용하여 `Estimator`에 적합화하고, 적합화된 `Model`을 가져오고, `Evaluator`를 사용하여 `Model`의 성능을 평가합니다.
* 가장 좋은 성능의 파라미터 집합에 의해 생성된 `Model`을 선택합니다. 

`Evaluator`는 회귀 문제의 경우 [`RegressionEvaluator`](api/scala/org/apache/spark/ml/evaluation/RegressionEvaluator.html), 
이진 데이터의 경우 [`BinaryClassificationEvaluator`](api/scala/org/apache/spark/ml/evaluation/BinaryClassificationEvaluator.html), 
다중 클래스 문제의 경우 [`MulticlassClassificationEvaluator`](api/scala/org/apache/spark/ml/evaluation/MulticlassClassificationEvaluator.html), 
다중 레이블 분류의 경우 [`MultilabelClassificationEvaluator`](api/scala/org/apache/spark/ml/evaluation/MultilabelClassificationEvaluator.html)
또는 순위 문제의 경우 [`RankingEvaluator`](api/scala/org/apache/spark/ml/evaluation/RankingEvaluator.html) 가 될 수 있습니다. 
최상의 `ParamMap`을 선택하는 데 사용되는 기본 메트릭은 이러한 각 `Evaluator`의 `setMetricName` 메소드로 재정의될 수 있습니다.

[`ParamGridBuilder`](api/scala/org/apache/spark/ml/tuning/ParamGridBuilder.html) 유틸리티를 사용하는 것은 파라미터 그리드를 구성하는 데 도움이 됩니다.
기본적으로 파라미터 그리드의 파라미터셋은 직렬로 평가됩니다. `CrossValidator` 또는 `TrainValidationSplit`으로 모델 선택을 진행하기 전에 2 이상의 값(1의 값은 직렬)으로 `parallelism`을 설정하여 파라미터 평가를 병렬로 수행이 가능합니다.
`parallelism`의 값은 클러스터 리소스를 초과하지 않고 병렬 처리를 최대화하기 위해 신중하게 선택해야 하며, 값이 클수록 성능이 항상 향상되는 것은 아닙니다. 일반적으로 대부분의 클러스터에는 최대 10이면 충분합니다.

# Cross-Validation

`CrossValidator`는 데이터셋을 별도의 훈련 및 테스트 데이터셋으로 사용되는 *folds*의 셋으로 분할하는 것으로 시작합니다. 예를 들어 `$k=3$` fold의 경우 `CrossValidator`는 3개의 (training, test) 데이터셋 쌍을 생성하며, 각 데이터셋은 데이터의 2/3를 훈련에 사용하고 1/3을 테스트에 사용합니다. 특정 `ParamMap`을 평가하기 위해 `CrossValidator`는 3개의 다른 (training, test) 데이터셋 쌍에 `Estimator`를 적합화하여 생성된 3개의 `Model`에 대한 평균 평가 메트릭을 계산합니다.

최고의 `ParamMap`을 식별한 후, `CrossValidator`는 최종적으로 최고의 `ParamMap`과 전체 데이터셋을 사용하여 `Estimator`를 다시 적합화합니다.

**예: 교차 검증을 통한 모델 선택**

다음 예는 `CrossValidator`를 사용하여 파라미터 그리드에서 선택하는 방법을 보여줍니다.

파라미터 그리드에 대한 교차 검증은 비용이 많이 듭니다.
예를 들어 아래의 예에서 파라미터 그리드는 `hashingTF.numFeatures`에 대해 3개의 값과 `lr.regParam`에 대해 2개의 값을 가지며 `CrossValidator`는 2개의 fold를 사용합니다. 이는 훈련되는 다른 모델에 `$(3 \times 2) \times 2 = 12$`를 곱합니다.
실제 설정에서는 더 많은 파라미터를 시도하고 더 많은 fold를 사용하는 것이 일반적일 수 있습니다(`$k=3$`와 `$k=10$`이 일반적입니다).
즉, `CrossValidator`를 사용하는 것은 매우 많은 비용을 필요로 할 수 있다는 것입니다.
그러나 이는 `heuristic hand-tuning`보다 통계적으로 더 타당한 파라미터를 선택하는 잘 정립된 방법이기도 합니다.

<div class="codetabs">

<div data-lang="scala" markdown="1">

API에 대한 자세한 내용은 [`CrossValidator` Scala docs](api/scala/org/apache/spark/ml/tuning/CrossValidator.html) 를 참조하십시오.

{% include_example scala/org/apache/spark/examples/ml/ModelSelectionViaCrossValidationExample.scala %}
</div>

<div data-lang="java" markdown="1">

API에 대한 자세한 내용은 [`CrossValidator` Java docs](api/java/org/apache/spark/ml/tuning/CrossValidator.html) 를 참조하십시오.

{% include_example java/org/apache/spark/examples/ml/JavaModelSelectionViaCrossValidationExample.java %}
</div>

<div data-lang="python" markdown="1">

API에 대한 자세한 내용은 [`CrossValidator` Python docs](api/python/reference/api/pyspark.ml.tuning.CrossValidator.html) 를 참조하십시오.

{% include_example python/ml/cross_validator.py %}
</div>

</div>

# Train-Validation Split

`CrossValidator` 외에도 Spark는 하이퍼파라미터 튜닝을 위한 `TrainValidationSplit`도 제공합니다.
`CrossValidator`의 경우 k번인 것과 달리 `TrainValidationSplit`은 파라미터의 각 조합을 한 번만 평가합니다.
따라서 비용은 저렴하지만 훈련 데이터셋이 충분히 크지 않으면 신뢰할 수 있는 결과를 생성할 수 없습니다.

`CrossValidator`와 달리 `TrainValidationSplit`은 단일(training, test) 데이터셋 쌍을 생성합니다.
`trainRatio` 파라미터를 사용하여 데이터셋을 해당 두 파트로 분할합니다.
예를 들어 `$trainRatio=0.75$`인 경우 `TrainValidationSplit`은 데이터의 75%를 훈련 데이터셋으로, 25%를 검증 데이터셋으로 데이터셋 쌍을 생성합니다.

`CrossValidator`와 같이 최종적으로 `TrainValidationSplit`은 최고의 `ParamMap`과 전체 데이터셋을 사용하여 `Estimator`를 적합화합니다.

**예: 학습 검증 분할을 통한 모델 선택**

<div class="codetabs">

<div data-lang="scala" markdown="1">

API에 대한 자세한 내용은 [`TrainValidationSplit` Scala docs](api/scala/org/apache/spark/ml/tuning/TrainValidationSplit.html) 를 참조하십시오.

{% include_example scala/org/apache/spark/examples/ml/ModelSelectionViaTrainValidationSplitExample.scala %}
</div>

<div data-lang="java" markdown="1">

API에 대한 자세한 내용은 [`TrainValidationSplit` Java docs](api/java/org/apache/spark/ml/tuning/TrainValidationSplit.html) 를 참조하십시오.

{% include_example java/org/apache/spark/examples/ml/JavaModelSelectionViaTrainValidationSplitExample.java %}
</div>

<div data-lang="python" markdown="1">

API에 대한 자세한 내용은 [`TrainValidationSplit` Python docs](api/python/reference/api/pyspark.ml.tuning.TrainValidationSplit.html) 를 참조하십시오.

{% include_example python/ml/train_validation_split.py %}
</div>

</div>
