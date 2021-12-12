이 페이지에서는 분류 및 회귀 알고리즘에 대해 설명한다. 
또한 선형 방법, 트리 및 앙상블과 같은 알고리즘의 특정 클래스를 논의하는 섹션도 포함되어 있다.

# Classification - 분류

## Logistic regression - 로지스틱 회귀
--------------------
로지스틱 회귀 분석은 범주형 반응을 예측하는 데 널리 사용되는 방법이다. 
이것은 결과의 확률을 예측하는 일반화 선형 모델의 특별한 경우이다. 
spark.ml에서는 이항 로지스틱 회귀 분석을 사용하여 이항 결과를 예측하거나 다항 로지스틱 회귀 분석을 사용하여 다항 로지스틱 결과를 예측하는 데 사용할 수 있다.
 패밀리 매개변수를 사용하여 두 알고리즘 중 하나를 선택하거나 설정되지 않은 상태로 두면 스파크가 올바른 변형을 유추한다.

> 다항 로지스틱 회귀는 패밀리 파라미터를 "다항"으로 설정하여 이항 분류에 사용할 수 있다. 두 개의 계수 세트와 두 개의 절편이 생성된다.

>일정한 0이 아닌 열이 있는 데이터 집합에 절편 없이 LogisticRegressionModel을 적합시키면 Spark MLlib는 일정한 0이 아닌 열에 대해 0 계수를 출력한다. 이 동작은 R glmnet과 동일하지만 LIBSVM과는 다르다.

### 이항 로지스틱 회귀 분석

이항 로지스틱 회귀 분석의 구현에 대한 자세한 내용은 spark.mlib의 로지스틱 회귀 분석을 참조하십시오.

#### 예시

다음 예제에서는 탄성 순 정규화를 사용하여 이항 및 다항 로지스틱 회귀 분석 모형을 이항 및 다항 로지스틱 회귀 분석으로 학습하는 방법을 보여 준다. 
ElasticNetParam은 $\alpha$에 해당하고 regParam은 $\lambda$에 해당한다.

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/LogisticRegressionWithElasticNetExample.scala %}

매개 변수에 대한 자세한 내용은 Java API 설명서를 참조하십시오.

{% include_example java/org/apache/spark/examples/ml/JavaLogisticRegressionWithElasticNetExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서를 참조하십시오.

{% include_example python/ml/logistic_regression_with_elastic_net.py %}

매개 변수에 대한 자세한 내용은 R API 설명서를 참조하십시오.

{% include_example binomial r/ml/logit.R %}

spark.ml 로지스틱 회귀 분석 구현에서는 교육 집합에서 모델 요약을 추출할 수도 있다. LogisticRegressionSummary에서 DataFrame으로 저장된 예측 및 메트릭은 @transient로 주석이 달리기 때문에 드라이버에서만 사용할 수 있다.

LogisticRegressionTraining요약에는 LogisticRegressionModel에 대한 요약이 나와 있다. 이진 분류의 경우 ROC 곡선과 같은 특정 추가 메트릭을 사용할 수 있다. 이진 요약은 binarySummary 메서드를 통해 액세스할 수 있다. BinaryLogisticRegressionTrainingSummary를 참조하십시오.

이전 예를 계속하면 다음과 같습니다.

{% include_example scala/org/apache/spark/examples/ml/LogisticRegressionSummaryExample.scala %}

[LogisticRegressionTrainingSummary]\
(api/java/org/apache/spark/ml/classification/LogisticRegressionSummary.html)는 ['LogisticRegressionModel']\(api/java/org/apache/spark/ml/classification/LogisticRegrationModel.html)에 대한 요약을 제공한다. 
이진 분류의 경우 ROC 곡선과 같은 특정 추가 메트릭을 사용할 수 있다. 
바이너리 요약은 바이너리 요약법을 통해 접근할 수 있다. ['BinaryLogisticRegressionTrainingSummary']\(api/java/org/apache/spark/ml/classification/BinaryLogisticRegressionTrainingSummary.html)를 참조하십시오.

이전 예를 계속하면 다음과 같습니다.

{% include_example java/org/apache/spark/examples/ml/JavaLogisticRegressionSummaryExample.java %}

['LogisticRegressionTrainingSummary']\(api/python/reference/api/pyspark.ml.classification.LogisticRegressionSummary.html)는 ['LogisticRegressionModel']\(api/python/reference/api/pyspark.ml.classification.LogisticRegressionModel.html) 
분류에 대한 요약을 제공한다. 
이진 분류의 경우 ROC 곡선과 같은 특정 추가 메트릭을 사용할 수 있다. ['BinaryLogisticRegressionTrainingSummary']\(api/python/reference/api/pyspark.ml.classification.BinaryLogisticRegressionTrainingSummary.html)을 참조하십시오.

이전 예를 계속하면 다음과 같습니다.

{% include_example python/ml/logistic_regression_summary_example.py %}

### 다항 로지스틱 회귀

다중 클래스 분류는 다항 로지스틱(소프트맥스) 회귀 분석을 통해 지원된다. 
다항 로지스틱 회귀 분석에서 알고리즘은 계수 집합 $K$ 또는 차원 $K\times J$의 행렬을 생성한다. 
여기서 $K$는 결과 클래스의 수이고 $J$는 특징의 수이다. 
알고리즘이 절편 항에 적합하면 절편의 길이 $K$ 벡터를 사용할 수 있다.

> 다항 계수는 cefficientMatrix로 사용할 수 있으며 절편은 intertVector로 사용할 수 있다.

>다항 패밀리로 훈련된 로지스틱 회귀 분석 모형에서는 계수 및 절편 방법이 지원되지 않다. 대신 cefficientMatrix를 사용하고 interceptVector를 사용한다.

결과 클래스 $k \in {1, 2, ..., K}$의 조건부 확률은 소프트맥스 함수를 사용하여 모델링된다.

\[ P(Y=k|\mathbf{X}, \boldsymbol{\beta}_k, \beta_{0k}) = \frac{e^{\boldsymbol{\beta}_k \cdot \mathbf{X} + \beta_{0k}}}{\sum_{k'=0}^{K-1} e^{\boldsymbol{\beta}_{k'} \cdot \mathbf{X} + \beta_{0k'}}} \]

우리는 과적합에 대한 제어를 위해 탄성 순 페널티를 사용하여 다항식 응답 모델을 사용하여 가중 음의 로그 가능성을 최소화한다.

\[ \min_{\beta, \beta_0} -\left[\sum_{i=1}^L w_i \cdot \log P(Y = y_i|\mathbf{x}_i)\right] + \lambda \left[\frac{1}{2}\left(1 - \alpha\right)||\boldsymbol{\beta}||_2^2 + \alpha ||\boldsymbol{\beta}||_1\right] \]

#### 예시

다음 예제에서는 탄성 순 정규화를 사용하여 다중 클래스 로지스틱 회귀 분석 모형을 교육하는 방법과 모형을 평가하기 위한 다중 클래스 교육 요약을 추출하는 방법을 보여 줍니다.

{% include_example scala/org/apache/spark/examples/ml/MulticlassLogisticRegressionWithElasticNetExample.scala %}

{% include_example java/org/apache/spark/examples/ml/JavaMulticlassLogisticRegressionWithElasticNetExample.java %}

{% include_example python/ml/multiclass_logistic_regression_with_elastic_net.py %}

매개 변수에 대한 자세한 내용은 R API 설명서를 참조하십시오.

{% include_example multinomial r/ml/logit.R %}

## 의사결정 트리 분류기
-------------------------
의사 결정 트리는 분류 및 회귀 방법의 인기 있는 메소드이다. 
spark.ml 구현에 대한 자세한 내용은 의사결정 트리에 대한 섹션에서 확인할 수 있다.

#### 예시

다음 예제는 LibSVM 형식으로 데이터 세트를 로드하고, 이를 훈련 및 테스트 세트로 나누고, 첫 번째 데이터 세트에서 학습한 다음, 홀드아웃 테스트 세트에서 평가한다. 
우리는 데이터를 준비하기 위해 두 개의 형상 transformer를 사용한다. 
이러한 former는 레이블 및 범주형 형상에 대한 범주를 색인화하여 의사 결정 트리 알고리즘이 인식할 수 있는 데이터 프레임에 메타데이터를 추가한다.

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/DecisionTreeClassificationExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaDecisionTreeClassificationExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/decision_tree_classification_example.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example classification r/ml/decisionTree.R %}

## 랜덤 포레스트 분류기
-----------------------
랜덤 포레스트는 분류 및 회귀 방법의 인기있는 계열이다. 
spark.ml 구현에 대한 자세한 내용은 랜덤 포리스트에 대한 섹션에서 확인할 수 있다.

#### 예시

다음 예제는 LibSVM 형식으로 데이터 세트를 로드하고, 이를 훈련 및 테스트 세트로 나누고, 첫 번째 데이터 세트에서 학습한 다음, 홀드아웃 테스트 세트에서 평가한다. 
우리는 데이터를 준비하기 위해 두 개의 형상 transformer를 사용한다. 
이러한 transformer는 레이블 및 범주형 형상에 대한 범주를 색인화하여 트리 기반 알고리즘이 인식할 수 있는 메타데이터를 DataFrame에 추가한다.

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/RandomForestClassifierExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaRandomForestClassifierExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/random_forest_classifier_example.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example classification r/ml/randomForest.R %}

## 그레디언트-부스트 트리 분류기
---------------------
GBT(Gradient-Boosted Tree)는 의사 결정 트리의 앙상블을 사용하는 대중적인 분류 및 회귀 방법이다. 
spark.ml 구현에 대한 자세한 내용은 GBT 관련 섹션에서 확인할 수 있다.

#### 예시

다음 예제는 LibSVM 형식으로 데이터 세트를 로드하고, 이를 훈련 및 테스트 세트로 나누고, 첫 번째 데이터 세트에서 학습한 다음, 홀드아웃 테스트 세트에서 평가한다. 
우리는 데이터를 준비하기 위해 두 개의 형상 transformer를 사용한다. 
이러한 transformer는 레이블 및 범주형 형상에 대한 범주를 색인화하여 트리 기반 알고리즘이 인식할 수 있는 메타데이터를 DataFrame에 추가한다.

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/GradientBoostedTreeClassifierExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaGradientBoostedTreeClassifierExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/gradient_boosted_tree_classifier_example.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example classification r/ml/gbt.R %}

## 다중 퍼셉트론 분류기
-------------------------------
다층 퍼셉트론 분류기(MLPC)는 피드포워드 인공 신경망을 기반으로 하는 분류기이다. MLPC는 여러 개의 노드 계층으로 구성된다. 
각 계층은 네트워크의 다음 계층에 완전히 연결된다. 
입력 계층의 노드는 입력 데이터를 나타낸다. 
다른 모든 노드는 노드의 가중치 $wv$ 및 바이어스 $bv$와 입력의 선형 조합에 의해 입력을 출력에 매핑하고 활성화 함수를 적용한다. 
이것은 $K+1$ 레이어가 있는 MLPC에 대해\[ \mathrm{y}(\x) = \mathrm{f_K}(...\mathrm{f_2}(\wv_2^T\mathrm{f_1}(\wv_1^T \x+b_1)+b_2)...+b_K) \]로 행렬 형태로 작성할 수 있다.
중간 층의 노드들은 시그모이드(sigmoid) 함수: \[ \mathrm{f}(z_i) = \frac{1}{1 + e^{-z_i}} \] 
출력 계층의 노드에서는 softmax 함수 : \[ \mathrm{f}(z_i) = \frac{e^{z_i}}{\sum_{k=1}^N e^{z_k}} \]
출력 계층의 노드 수$N$는 클래스 수에 해당한다.

MLPC는 모델을 학습하기 위해 역전파를 사용한다. 최적화에는 로지스틱 손실 함수를 사용하고 최적화 루틴으로는 L-BFGS를 사용한다.

#### 예시

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/MultilayerPerceptronClassifierExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaMultilayerPerceptronClassifierExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/multilayer_perceptron_classification.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example r/ml/mlp.R %}

## 선형 서포트 벡터 머신
------------------------
서포트 벡터 머신은 고차원 또는 무한 차원 공간에 초평면 또는 초평면 세트를 구성하며, 이는 분류, 회귀 또는 다른 작업에 사용될 수 있다. 
직관적으로, 좋은 분리는 모든 클래스의 가장 가까운 훈련 데이터 지점(일명 기능적 여유라고 함)까지 가장 큰 거리를 가진 초평면에 의해 달성된다. 
일반적으로 여유가 클수록 분류기의 일반화 오차가 줄어들기 때문이다. 
스파크 ML의 LinearSVC는 선형 SVM을 사용한 이진 분류를 지원한다. 
내부적으로 OWLQN 최적화 도구를 사용하여 힌지 손실을 최적화한다.

#### 예시

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/LinearSVCExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaLinearSVCExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/linearsvc.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example r/ml/svmLinear.R %}

## One-vs-Rest 분류기(일명  1-vs-All 분류기)
----------------------
OneVsRest는 이진 분류를 효율적으로 수행할 수 있는 기본 분류기에서 다중 클래스 분류를 수행하기 위한 기계 학습 감소의 한 예이다. 그것은 "One-vs-All"로도 알려져 있다.

OneVsRest는 Estimator로 구현된다. 
기본 분류기의 경우 분류자의 인스턴스를 사용하고 각 k 클래스에 대한 이진 분류 문제를 생성한다.
클래스 i의 분류기는 레이블이 i인지 아닌지를 예측하도록 훈련되어 클래스 i를 다른 모든 클래스와 구별한다.

예측은 각 이진 분류기를 평가하여 수행되며 가장 신뢰할 수 있는 분류기의 인덱스는 레이블로 출력된다.

#### 예시

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/OneVsRestExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaOneVsRestExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/one_vs_rest_example.py %}

## Naive Bayes
------------------
나이브 베이즈 분류기는 모든 특징 쌍 사이의 강한 (순수한) 독립 가정과 함께 베이즈의 정리를 적용하는 것에 기초한 단순한 확률론적 다중 클래스 분류기 계열이다.

나이브 베이즈는 매우 효율적으로 훈련될 수 있다. 교육 데이터에 대한 단일 패스로 각 레이블이 주어진 각 기능의 조건부 확률 분포를 계산한다. 예측을 위해, 그것은 Bayes의 정리를 주어진 관측치의 각 레이블의 조건부 확률 분포를 계산하기 위해 적용한다.

MLlib는 다항식 순진한 베이즈, 보완적인 순진한 베이즈, 베르누이 순진한 베이즈, 가우스 순진한 베이즈를 지원한다.

입력 데이터: 이러한 다항식, 보완 및 베르누이 모델은 일반적으로 문서 분류에 사용된다.
이 문맥에서 각 관측치는 문서이며 각 피쳐는 용어를 나타낸다. 
특성의 값은 용어의 빈도(다항식 또는 보완 네이브 베이) 또는 용어가 문서에서 발견되었는지 여부를 나타내는 0 또는 1이다(베르누이 네이브 베이). 
다항 및 베르누이 모형에 대한 피쳐 값은 음수가 아니어야 한다. 모델 유형은 선택적 매개변수인 "multinomal - 다항", "complement - 보완", "bernoulli - 베르누이" 또는 "gaussian - 가우스"와 함께 선택되며 "다항"은 기본값으로 지정된다.
문서 분류의 경우 입력 피쳐 벡터는 일반적으로 희소 벡터여야 합니다. 교육 데이터는 한 번만 사용되므로 캐시할 필요가 없다.

추가 smoothing은 매개 변수 $\lambda$(기본값 $1.0$)를 설정하여 사용할 수 있다.

#### 예시

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/NaiveBayesExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaNaiveBayesExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/naive_bayes_example.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example python/ml/naive_bayes_example.py %}

## Factorization 머신 분류기
---------------------
Factorization 시스템의 구현에 대한 자세한 배경과 자세한 내용은 Factorization 시스템 섹션을 참조하십시오.

#### 예시

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/FMClassifierExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaFMClassifierExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/fm_classifier_example.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example r/ml/fmClassifier.R %}

# Regression - 회귀

## 선형회귀
----------------------
선형 회귀 모형 및 모형 요약에 대한 작업 인터페이스는 로지스틱 회귀 분석의 경우와 유사하다.

>"l-bfgs" solver에 의해 일정한 0이 아닌 컬럼을 가진 데이터셋에 절편 없이 LinearRegressionModel을 적합시킬 때, Spark MLlib는 일정한 0이 아닌 컬럼에 대해 0 계수를 출력한다. 
이 동작은 R glmnet과 동일하지만 LIBSVM과는 다릅니다.

#### 예시

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/LinearRegressionWithElasticNetExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaLinearRegressionWithElasticNetExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/linear_regression_with_elastic_net.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example r/ml/lm_with_elastic_net.R %}

## 일반화된 선형 회귀
------------------------
출력이 가우스 분포를 따르는 것으로 가정되는 선형 회귀 분석과 대조적으로, 일반화 선형 모델(GLM)은 반응 변수 $Y_i$가 지수 분포군의 일부 분포를 따르는 선형 모델의 사양이다. 
스파크의 일반화 선형 회귀 인터페이스를 사용하면 선형 회귀 분석, 포아송 회귀 분석, 로지스틱 회귀 분석 등을 포함한 다양한 유형의 예측 문제에 사용할 수 있는 GLM을 유연하게 지정할 수 있다. 
현재 spark.ml에서는 지수 계열 분포의 하위 집합만 지원되며 아래 나열되어 있다.

참고: 스파크는 현재 GeneralizedLinearRegression 인터페이스를 통해 최대 4096개의 기능만 지원하며, 이 제약 조건이 초과되면 예외가 발생한다.
자세한 내용은 고급 섹션을 참조하십시오. 
선형 및 로지스틱 회귀 분석의 경우 선형 회귀 및 로지스틱 회귀 추정기를 사용하여 형상 수가 증가한 모형을 학습할 수 있다.

GLM은 자연 지수 계열 분포라고 불리는 "규범적" 또는 "자연적" 형태로 작성될 수 있는 지수 계열 분포를 필요로 한다. 
자연 지수 계열 분포의 형태는 다음과 같다.

$$ f_Y(y|\theta, \tau) = h(y, \tau)\exp{\left( \frac{\theta \cdot y - A(\theta)}{d(\tau)} \right)} $$

여기서 $\theta$는 관심 있는 매개 변수이고 $\theta$는 분산 매개 변수이다. GLM에서 반응 변수 $Y_i$는 자연 지수 계열 분포에서 도출된 것으로 가정한다.

$$ Y_i \sim f\left(\cdot|\theta_i, \tau \right) $$

여기서 관심 있는 매개 변수인 $\theta_i$는 다음과 같은 방법으로 반응 변수 $\mu_i$의 예상 값과 관련이 있다.

$$ \mu_i = A'(\theta_i) $$

여기서 $A'(\theta_i)$는 선택한 분포의 형태로 정의된다. GLM은 또한 반응 변수 $\mu_i$의 기대값과 소위 선형 예측 변수 $\eta_i$ 사이의 관계를 정의하는 링크 함수를 지정할 수 있다.

$$ g(\mu_i) = \eta_i = \vec{x_i}^T \cdot \vec{\beta} $$

종종 링크 함수는 $A' = g^{-1}$이(가) 관심 매개 변수 $\theta$와 선형 예측 변수 $\eta$ 사이에 단순화된 관계를 산출하도록 선택된다. 이 경우, 연결 함수 $g(\mu)$는 "카노니컬" 연결 함수라고 한다.

$$ \theta_i = A'^{-1}(\mu_i) = g(g^{-1}(\eta_i)) = \eta_i $$

GLM은 우도 함수를 최대화하는 회귀 계수 $\vec{\beta}$를 찾는다.

$$ \max_{\vec{\beta}} \mathcal{L}(\vec{\theta}|\vec{y},X) = \prod_{i=1}^{N} h(y_i, \tau) \exp{\left(\frac{y_i\theta_i - A(\theta_i)}{d(\tau)}\right)} $$

여기서 관심 있는 매개 변수인 $\theta_i$는 다음과 같은 회귀 계수와 관련이 있다.

$$ \theta_i = A'^{-1}(g^{-1}(\vec{x_i} \cdot \vec{\beta})) $$

스파크의 일반화된 선형 회귀 인터페이스는 잔차, p-값, 이탈도, Akaike 정보 기준 등을 포함하여 GLM 모형의 적합성을 진단하기 위한 요약 통계량도 제공한다.

### Available families
|기법|응답 type|지원되는 link|
|----|-------|--------------|
|Gaussian|continuous|Identity*, Log, Inverse|
|Binomial|binary|Logit*, Probit, CLogLog|
|Poisson|count|Log*, Identity, Sqrt|
|Gamma|continuous|Inverse*, Identity, Log|
|Tweedie|0-팽창 continuous|Power link function|
|* Canonical Link|

#### 예시

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/GeneralizedLinearRegressionExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaGeneralizedLinearRegressionExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/generalized_linear_regression_example.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example r/ml/glm.R %}

## 의사결정 트리 회귀
-------------------
의사 결정 트리는 분류 및 회귀 방법의 인기 있는 제품군이다. 
spark.ml 구현에 대한 자세한 내용은 의사결정 트리에 대한 섹션에서 확인할 수 있다.

#### 예시

다음 예제는 LibSVM 형식으로 데이터 세트를 로드하고, 이를 훈련 및 테스트 세트로 나누고, 첫 번째 데이터 세트에서 학습한 다음, 홀드아웃 테스트 세트에서 평가한다. 
우리는 feature transformer를 사용하여 범주형 피처를 인덱싱하여 의사 결정 트리 알고리즘이 인식할 수 있는 메타데이터를 데이터 프레임에 추가한다.

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/DecisionTreeRegressionExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaDecisionTreeRegressionExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/decision_tree_regression_example.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example regression r/ml/decisionTree.R %}

## 랜덤 포레스트 회귀
-------------------

랜덤 포레스트는 분류 및 회귀 방법의 인기있는 계열이다. 
spark.ml 구현에 대한 자세한 내용은 랜덤 포리스트에 대한 섹션에서 확인할 수 있다.

#### 예시

다음 예제는 LibSVM 형식으로 데이터 세트를 로드하고, 이를 훈련 및 테스트 세트로 나누고, 첫 번째 데이터 세트에서 학습한 다음, 홀드아웃 테스트 세트에서 평가한다. 
우리는 feature transformer를 사용하여 범주형 피쳐를 인덱싱하여 트리 기반 알고리즘이 인식할 수 있는 메타데이터를 DataFrame에 추가한다.

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/RandomForestRegressorExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaRandomForestRegressorExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/random_forest_regressor_example.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example regression r/ml/randomForest.R %}

## 그레디언트 부스트 트리 회귀
---------------
GBT(Gradient-Boosted Tree)는 의사 결정 트리의 앙상블을 사용하는 일반적인 회귀 방법이다. 
spark.ml 구현에 대한 자세한 내용은 GBT 관련 섹션에서 확인할 수 있다.

#### 예시

참고: 이 예제 데이터 집합의 경우 GBTRegressor는 실제로 한 번만 반복하면 되지만 일반적으로는 그렇지 않다.

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/GradientBoostedTreeRegressorExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaGradientBoostedTreeRegressorExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/gradient_boosted_tree_regressor_example.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example regression r/ml/gbt.R %}

## Survival 회귀
---------
spark.ml에서는 검열 데이터에 대한 파라메트릭 생존 회귀 모델인 Accelerated failure time(AFT) 모델을 구현한다. 
생존 시간 로그 모델을 설명하므로 생존 분석에서는 로그 선형 모델이라고 합니다. 
동일한 목적을 위해 설계된 비례 위험 모델과 달리, AFT 모델은 각 사례가 객관적 기능에 독립적으로 기여하기 때문에 병렬화가 더 쉽다.

가능한 우측 편차가 있는 대상의 임의의 수명 $t_{i}$에 대해 공변량 $x^{'}$의 값이 주어지면, AFT 모델 아래의 우도 함수는 \[ L(\beta,\sigma)=\prod_{i=1}^n[\frac{1}{\sigma}f_{0}(\frac{\log{t_{i}}-x^{'}\beta}{\sigma})]^{\delta_{i}}S_{0}(\frac{\log{t_{i}}-x^{'}\beta}{\sigma})^{1-\delta_{i}} \]
여기서 $\delta_{i}$는 이벤트가 발생했음을 나타내는 지표이다. 
즉, 감지되지 않은 상태다.
로그 우도 함수는 \[ \iota(\beta,\sigma)=\sum_{i=1}^{n}[-\delta_{i}\log\sigma+\delta_{i}\log{f_{0}}(\epsilon_{i})+(1-\delta_{i})\log{S_{0}(\epsilon_{i})}] \]
여기서 $S_{0}(\epsilon_{i})$는 기본 생존 함수이고, $f_{0}(\epsilon_{i})$는 해당하는 밀도 함수이다.

가장 일반적으로 사용되는 AFT 모형은 생존 시간의 Weibull 분포를 기반으로 한다. 
수명에 대한 Weibull 분포는 수명의 로그에 대한 극단값 분포에 해당하며, $S_{0}(\epsilon_{i})$ 함수는 \[ S_{0}(\epsilon_{i})=\exp(-e^{\epsilon_{i}}) \]이고, $f_{0}(\epsilon_{i})$ 함수는 \[ f_{0}(\epsilon_{i})=e^{\epsilon_{i}}\exp(-e^{\epsilon_{i}}) \]이다. Weibull 분포가 평생인 AFT 모델의 로그 우도 함수는 
\[ \iota(\beta,\sigma)= -\sum_{i=1}^n[\delta_{i}\log\sigma-\delta_{i}\epsilon_{i}+e^{\epsilon_{i}}] \]이다.

최대 사후 확률에 해당하는 음의 로그 우도를 최소화하기 때문에, 최적화하기 위해 사용하는 손실 함수는 $-\iota(\beta,\sigma)$이다. 

각각 $\beta$ 및 $\log\sigma$에 대한 그레이디언트 함수는 다음과 같다.
\[ \frac{\partial (-\iota)}{\partial \beta}=\sum_{1=1}^{n}[\delta_{i}-e^{\epsilon_{i}}]\frac{x_{i}}{\sigma} \] 
\[ \frac{\partial (-\iota)}{\partial (\log\sigma)}=\sum_{i=1}^{n}[\delta_{i}+(\delta_{i}-e^{\epsilon_{i}})\epsilon_{i}] \]

AFT 모델은 볼록 최적화 문제, 즉 계수 벡터 $\beta$와 스케일 매개 변수 $\log\sigma$의 로그에 의존하는 볼록 함수 $-\iota(\beta,\sigma)$의 최소화기를 찾는 작업으로 공식화할 수 있다. 
구현의 기초가 되는 최적화 알고리즘은 L-BFGS이다. 
구현은 R의 생존 함수 생존의 결과와 일치한다.

> 일정한 0이 아닌 열이 있는 데이터 집합에 인터셉트 없이 AFTSurvivalRegressionModel을 적합시키면 Spark MLlib는 일정한 0이 아닌 열에 대해 0 계수를 출력한다. 
이 동작은 R 생존::surverg와 다릅니다.

#### 예시

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/AFTSurvivalRegressionExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaAFTSurvivalRegressionExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/aft_survival_regression.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example r/ml/survreg.R %}

## Isotonic(등방) 회귀
-----------------
등방 회귀는 회귀 알고리즘 계열에 속한다. 공식적으로 등방 회귀는 관측된 반응을 나타내는 유한한 실수 $Y = {y_1, y_2, ..., y_n}$과 $X = {x_1, x_2, ..., x_n}$이 주어진다면 $x_1\le x_2\le ...\le x_n$에 따른 완전한 차수를 최소화하는 함수를 찾는 문제이다. 여기서 $w_i$는 양의 가중치이다.

\begin{equation} f(x) = \sum_{i=1}^n w_i (y_i - x_i)^2 \end{equation}

그 결과 발생하는 함수를 등방 회귀라고 하며 고유하다. 
순서 제한 하에서는 최소 제곱 문제로 볼 수 있다. 
본질적으로 등방성 회귀는 원래 데이터 점에 가장 적합한 단조 함수다.

우리는 등방 회귀를 병렬화하는 접근법을 사용하는 풀 인접 위반 알고리즘을 구현한다. 
교육 입력은 세 개의 열 레이블, 특징 및 가중치를 포함하는 DataFrame이다. 
또한 IsoconicRegression 알고리즘에는 $isotonic$ defaulting to true라는 선택적 매개 변수가 있다. 
이 인수는 등방 회귀가 등방성(단조적으로 증가)인지 아니면 반동성(단조적으로 감소)인지를 지정한다.

교육에서는 알려진 기능과 알려지지 않은 기능 모두에 대한 레이블을 예측하는 데 사용할 수 있는 IsoconicRegressionModel을 반환한다. 
등방 회귀의 결과는 부분적 선형 함수로 취급된다. 따라서 예측의 규칙은 다음과 같다.

* 예측 입력이 교육 기능과 정확히 일치하면 관련 예측이 반환된다. 
동일한 형상을 가진 예측이 여러 개 있을 경우 그 중 하나가 반환된다. 
정의되지 않은 항목(java.util.Arrays.binarySearch와 동일함)
* 예측 입력이 모든 훈련 특성보다 낮거나 높으면 각각 가장 낮거나 가장 높은 특징을 가진 예측이 반환된다. 
동일한 특징을 가진 예측이 여러 개 있을 경우 각각 가장 낮은 예측 또는 가장 높은 예측이 반환된다.
* 예측 입력이 두 교육 특성 사이에 있으면 예측은 부분 선형 함수로 처리되고 보간된 값은 가장 가까운 두 형상의 예측으로부터 계산된다. 
동일한 형상의 값이 여러 개 있는 경우 이전 점과 동일한 규칙이 사용된다.

#### 예시

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/IsotonicRegressionExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaIsotonicRegressionExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/isotonic_regression_example.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example r/ml/isoreg.R %}

## Factorization machine regressor
----------------
Factorization 시스템의 구현에 대한 자세한 배경과 자세한 내용은 Factorization 시스템 섹션을 참조하십시오.

#### 예시

다음 예제는 LibSVM 형식으로 데이터 세트를 로드하고, 이를 훈련 및 테스트 세트로 나누고, 첫 번째 데이터 세트에서 학습한 다음, 홀드아웃 테스트 세트에서 평가한다. 
폭발적인 기울기 문제를 방지하기 위해 특징을 0과 1 사이로 확장한다.

매개변수에 대한 자세한 내용은 Scala API 설명서에서 확인할 수 있다.

{% include_example scala/org/apache/spark/examples/ml/FMRegressorExample.scala %}

매개변수에 대한 자세한 내용은 JAVA API 설명서에서 확인할 수 있다.

{% include_example java/org/apache/spark/examples/ml/JavaFMRegressorExample.java %}

매개변수에 대한 자세한 내용은 Python API 설명서에서 확인할 수 있다.

{% include_example python/ml/fm_regressor_example.py %}

매개변수에 대한 자세한 내용은 R API 설명서에서 확인할 수 있다.

{% include_example r/ml/fmRegressor.R %}

# Linear methods

우리는 $L_1$ 또는 $L_2$ 정규화를 사용하는 로지스틱 회귀 및 선형 최소 제곱과 같이 널리 사용되는 선형 방법을 구현한다.
구현 및 조정에 대한 자세한 내용은 RDD 기반 API에 대한 선형 메서드 가이드를 참조하십시오. 이 정보는 여전히 관련이 있다.

또한 Zou 등에서 제안된 $L_1$ 및 $L_2$ 정규화의 하이브리드인 탄력적 망을 위한 DataFrame API를 포함하며, 탄력적 망을 통한 정규화 및 변수 선택도 포함한다. 
수학적으로, 이것은 $L_1$과 $L_2$ 정규화 항의 볼록한 조합으로 정의된다:\[ \alpha \left( \lambda \|\wv\|_1 \right) + (1-\alpha) \left( \frac{\lambda}{2}\|\wv\|_2^2 \right) , \alpha \in [0, 1], \lambda \geq 0 \].

$\alpha$를 올바르게 설정하면 탄성 망은 $L_1$ 및 $L_2$ 정규화를 모두 특수 사례로 포함한다.
예를 들어, 선형 회귀 모델이 $1$로 설정된 탄성 순 매개 변수 $\alpha$로 훈련되는 경우, 이는 라소 모델과 동일하다. 
반면에, $\alpha$가 $0$로 설정된 경우 훈련된 모델은 능선 회귀 모델로 감소한다. 
우리는 탄력적인 순 정규화를 통한 선형 회귀와 로지스틱 회귀를 모두 위한 파이프라인 API를 구현한다.

# Factorization Machines

인수분해 기계는 (광고 및 추천 시스템과 같은) 큰 희소성을 가진 문제에서도 특징 간의 상호작용을 추정할 수 있다. 
spark.ml 구현은 이진 분류 및 회귀 분석을 위한 인수 분해 기계를 지원한다.

인수분해 기계 공식은 다음과 같다.

$$ \hat{y} = w_0 + \sum\limits^n_{i-1} w_i x_i + \sum\limits^n_{i=1} \sum\limits^n_{j=i+1} \langle v_i, v_j \rangle x_i x_j $$

처음 두 항은 절편 및 선형 항(선형 회귀 분석에서와 동일)을 나타내고 마지막 항은 쌍방향 교호작용 항을 나타낸다. $$v_i$$는 k개의 인자가 있는 i번째 변수를 설명한다.

FM은 회귀에 사용할 수 있으며 최적화 기준은 평균 제곱 오차다. FM은 시그모이드 함수를 통한 이진 분류에도 사용할 수 있다. 최적화 기준은 로지스틱 손실다.

쌍들의 상호작용은 다음과 같이 재구성할 수 있다.

$$ \sum\limits^n_{i=1} \sum\limits^n_{j=i+1} \langle v_i, v_j \rangle x_i x_j = \frac{1}{2}\sum\limits^k_{f=1} \left(\left( \sum\limits^n_{i=1}v_{i,f}x_i \right)^2 - \sum\limits^n_{i=1}v_{i,f}^2x_i^2 \right) $$

이 방정식은 k와 n 모두에서 선형 복잡성만 가지고 있다. 
즉, 계산은 $$O(kn)$$이다.

일반적으로 폭발적 기울기 문제를 방지하기 위해서는 연속 피쳐를 0과 1 사이로 확장하거나 연속 피쳐와 원핫 인코딩을 하는 것이 가장 좋다.

# Decision trees
의사 결정 트리와 그 앙상블은 분류와 회귀의 기계 학습 작업에 널리 사용되는 방법이다. 
의사결정 트리는 해석하기 쉽고, 범주형 특징을 처리하고, 다중 클래스 분류 설정으로 확장되며, 형상 배율이 필요하지 않고, 비선형성과 형상 상호작용을 캡처할 수 있기 때문에 널리 사용된다. 랜덤 포레스트 및 부스팅과 같은 트리 앙상블 알고리즘은 분류 및 회귀 작업에 대해 가장 높은 성능을 발휘한다.

spark.ml 구현은 연속 및 범주형 특징을 모두 사용하여 이진 및 다중 클래스 분류와 회귀를 위한 의사결정 트리를 지원한다. 
이 구현은 데이터를 행별로 분할하여 수백만 또는 수십억 개의 인스턴스로 분산 교육을 수행할 수 있다.

사용자는 MLlib 의사 결정 트리 안내서에서 의사 결정 트리 알고리즘에 대한 자세한 정보를 확인할 수 있다. 이 API와 원본 MLlib 의사 결정 트리 API의 주요 차이점은 다음과 같다.

* ML 파이프라인 지원
* 분류를 위한 의사결정 트리 분리 대 회귀 분석
* DataFrame 메타데이터를 사용하여 연속 및 범주형 기능 구분

의사 결정 트리를 위한 파이프라인 API는 원래 API보다 조금 더 많은 기능을 제공한다.
특히 분류의 경우 사용자는 각 클래스의 예측 확률(일명 클래스 조건부 확률)을 얻을 수 있으며 회귀의 경우 사용자는 예측의 편향된 표본 분산을 얻을 수 있다.

트리 앙상블(Random Forests and Gradient-Boosted Tree)은 아래 트리 앙상블 섹션에 설명되어 있다.

## Input과 Output
---------------

여기에는 입력 및 출력(예측) 열 유형을 나열합니다. 모든 출력 열은 선택 사항이다. 
출력 열을 제외하려면 해당하는 파라미터를 빈 문자열로 설정하십시오.

### Input Columns
|Param 이름|Type|기본값|설명|
|------|-----|----|--|
|labelCol|Double|"label"|Label to predict|
|featuresCol|Vector|"features"|Feature vector|

### Output Columns
|Param 이름|Type|기본값|설명|노트|
|--|--|--|-------------------|--|
|predictionCol|Double|"predicton"|Predicted label|
|rawPredictionCol|Vecotr|"rawPrediction"|트리 노드에 교육 인스턴스 레이블의 수를 갖는 길이 # 클래스의 벡터이며, 이를 예측하는 데 사용된다|Classification만 가능|
|probabilityCol|Vector|"probability"|다항 분포로 정규화된 원시 예측과 같은 길이 # 클래스의 벡터|Classification만 가능|
|varianceCol|Double||예측의 편향된 표본 분산|Regression만 가능|

# Tree Ensembles
DataFrame API는 Random Forests와 Gradient-Boosted Tree(GBT)라는 두 가지 주요 트리 앙상블 알고리즘을 지원한다. 
둘 다 기본 모델로 spark.ml 의사결정 트리를 사용한다.

사용자는 MLlib Ensemble 가이드에서 앙상블 알고리즘에 대한 자세한 내용을 확인할 수 있다.
이 섹션에서는 앙상블을 위한 DataFrame API를 시연한다.

이 API와 원본 MLlib 앙상블 API의 주요 차이점은 다음과 같다.

* DataFrames 및 ML 파이프라인 지원
* 분류 vs 회귀 분석
* DataFrame 메타데이터를 사용하여 연속 및 범주형 기능 구분
* 무작위 포레스트에 대한 기능성 향상: 기능 중요도의 추정치 및 분류에 대한 각 클래스의 예측 확률(일명 클래스 조건부 확률)

## Random Forests
------------------
랜덤 포레스트는 의사 결정 트리의 앙상블이다. 랜덤 포레스트는 과적합 위험을 줄이기 위해 많은 의사 결정 트리를 결합한다. 
spark.ml 구현은 연속 및 범주형 기능을 모두 사용하여 이진 및 다중 클래스 분류와 회귀를 위한 랜덤 포리스트를 지원한다.

알고리즘 자체에 대한 자세한 내용은 랜덤 포리스트에 대한 spark.mlib 설명서를 참조하십시오.


### Input과 Output
---------------
여기에는 입력 및 출력(예측) 열 유형을 나열한다. 모든 출력 열은 선택 사항이다. 출력 열을 제외하려면 해당하는 파라미터를 빈 문자열로 설정하십시오.

#### Input Columns
|Param 이름|Type|기본값|설명|
|------|-----|----|--|
|labelCol|Double|"label"|Label to predict|
|featuresCol|Vector|"features"|Feature vector|

#### Output Columns (Predictions)
|Param 이름|Type|기본값|설명|노트|
|--|--|--|-------------------|--|
|predictionCol|Double|"predicton"|Predicted label|
|rawPredictionCol|Vecotr|"rawPrediction"|트리 노드에 교육 인스턴스 레이블의 수를 갖는 길이 # 클래스의 벡터이며, 이를 예측하는 데 사용된다|Classification만 가능|
|probabilityCol|Vector|"probability"|다항 분포로 정규화된 원시 예측과 같은 길이 # 클래스의 벡터|Classification만 가능|

## Gradient-Boosted Trees (GBTs)
------------------
GBT(Gradient-Boosted Tree)는 의사 결정 트리의 앙상블이다. GBT는 손실 함수를 최소화하기 위해 의사 결정 트리를 반복적으로 훈련한다. 
spark.ml 구현은 연속 및 범주형 기능을 모두 사용하여 이진 분류 및 회귀를 위한 GBT를 지원한다.

알고리즘 자체에 대한 자세한 내용은 GBT에 대한 spark.mlib 문서를 참조하십시오.

### Inputs and Outputs
-------------

여기에는 입력 및 출력(예측) 열 유형을 나열한다. 모든 출력 열은 선택 사항이다. 출력 열을 제외하려면 해당하는 파라미터를 빈 문자열로 설정하십시오.

#### Input Columns
|Param 이름|Type|기본값|설명|
|------|-----|----|--|
|labelCol|Double|"label"|Label to predict|
|featuresCol|Vector|"features"|Feature vector|

GBTClassifier는 현재 이진 레이블만 지원한다.

#### Output Columns (Predictions)
|Param 이름|Type|기본값|설명|노트|
|--|--|--|-------------------|--|
|predictionCol|Double|"predicton"|Predicted label|

향후 GBTClassifier는 RandomForestClassifier와 마찬가지로 원시 예측 및 확률에 대한 열을 출력한다.