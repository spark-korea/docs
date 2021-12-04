# Collaborative filtering - 협업필터링

협업 필터링은 일반적으로 추천 시스템에 사용된다. 
이러한 기술은 사용자 항목 연관 매트릭스의 누락된 항목을 채우는 것을 목표로 한다. 
spark.ml은 현재 모델 기반 협업 필터링을 지원하며, 사용자와 제품은 누락된 항목을 예측하는 데 사용될 수 있는 작은 잠재 요인 집합에 의해 설명된다. 
spark.ml은 이러한 잠재 요인을 학습하기 위해 교대 최소 제곱(ALS) 알고리즘을 사용한다.
spark.ml의 구현에는 다음과 같은 매개 변수가 있습니다.

* numBlocks : 계산을 병렬화하기 위해 분할될 블록의 수(기본값 : 10)
* rank : 모형에 있는 잠재 요인의 수(기본값 : 10)
* maxIter : 실행할 최대 반복 횟수(기본값 : 10)
* regParam : 정규화 매개변수를 ALS로 지정(기본값 : 1.0)
* implicitPrefs : 시적 피드백 ALS 변형을 사용할지 또는 암시적 피드백 데이터에 맞게 조정된 변형을 사용할지 여부를 지정
* alpha : 선호 관측치에 대한 기준 신뢰도를 지배하는 ALS의 암묵적 피드백 변형에 적용할 수 있는 매개변수(기본값 : 1.0)
* nonnegative : 최소 제곱에 음이 아닌 구속조건을 사용할지 여부를 지정(기본값 : False)

참고: ALS용 DataFrame 기반 API는 현재 사용자 및 항목 ID에 대한 정수만 지원한다. 사용자 및 항목 ID 열에 대해 다른 숫자 유형이 지원되지만 ID는 정수 값 범위 내에 있어야 한다.

## 명시적 vs 암묵적 피드백
--------------------------
매트릭스 인수 분해 기반 협업 필터링에 대한 표준 접근법은 사용자 항목 매트릭스의 항목을 사용자가 항목에 대해 제공하는 명시적 선호 사항으로 취급한다.

많은 실제 사용 사례에서 암묵적 피드백(예: 보기, 클릭, 구매, 좋아요, 공유)에만 액세스하는 것이 일반적이다. 
이러한 데이터를 처리하기 위해 spark.ml에서 사용되는 접근 방식은 암시적 피드백 데이터 세트를 위한 협업 필터링에서 가져온 것이다. 
특히, 등급 매트릭스를 직접 모델링하려고 시도하는 대신, 이 접근법은 데이터를 사용자 동작 관찰의 강도(클릭 횟수 또는 누군가 영화를 보는 데 사용한 누적 지속시간 등)를 나타내는 숫자로 취급한다. 
그러한 수치는 항목에 부여되는 명시적인 등급이 아니라 관찰된 이용자 선호도에 대한 신뢰 수준과 관련이 있다. 
그런 다음 모델은 항목에 대한 사용자의 예상 선호도를 예측하는 데 사용할 수 있는 잠재 요인을 찾고자 한다.

## 정규화 매개 변수의 스케일링
---------------------------
사용자가 사용자 요인 업데이트에서 생성한 등급 수 또는 제품 요인 업데이트에서 제품이 받은 등급 수에 따라 각 최소 제곱 문제를 해결하는 데 정규화 매개 변수 regParam을 척도화한다. 
이 접근법의 이름은 "ALS-WR"이며 "Netflix Prize를 위한 대규모 병렬 협업 필터링"이라는 논문에서 논의된다. 
이를 통해 regParam은 데이터 세트의 규모에 덜 의존하게 되므로 샘플링된 하위 집합에서 학습한 최상의 매개 변수를 전체 데이터 집합에 적용할 수 있으며 유사한 성능을 기대할 수 있다.

## Cold-start 전략
----------------------------
ALSModel을 사용하여 예측할 때, 모델 훈련 중에 존재하지 않았던 테스트 데이터 세트의 사용자 또는 항목을 만나는 것이 일반적이다. 
이 문제는 일반적으로 두 가지 시나리오에서 발생합니다.

1. 프로덕션에서 등급 기록이 없고 모델이 교육되지 않은 새로운 사용자 또는 항목의 경우(콜드 스타트 문제)

2. 교차 검증 중에 데이터는 교육 세트와 평가 세트 간에 분할된다. 
Spark의 CrossValidator 또는 TrainValidationSplit에서와 같이 간단한 무작위 분할을 사용하는 경우, 실제로 교육 세트에 없는 사용자 및/또는 평가 세트의 항목을 만나는 것이 매우 일반적이다.

기본적으로 스파크는 ALSModel.transform 진행되는 동안 사용자 또는 항목 요인이 모형에 없을 때 NaN 예측을 할당한다. 
이것은 새로운 사용자나 항목을 나타내며, 시스템이 예측으로 사용할 일부 예비 항목을 결정할 수 있기 때문에 프로덕션 시스템에서 유용할 수 있다.

그러나 NaN 예측 값은 평가 메트릭에 대해 NaN 결과를 초래하기 때문에(예를 들어 RegressionEvaluator 사용 시) 교차 검증 중에는 바람직하지 않다. 
이로 인해 모델 선택이 불가능하다.

Spark는 사용자가 NaN 값을 포함하는 예측의 데이터 프레임에 있는 행을 삭제하기 위해 coldStartStrategy 파라미터를 "drop"으로 설정할 수 있도록 한다. 
그런 다음 평가 지표가 NaN이 아닌 데이터에 대해 계산되고 유효하다. 이 매개 변수의 사용은 아래 예에 나와 있다.

참고: 현재 지원되는 콜드 스타트 전략은 "nan"(위에서 언급한 기본 동작)과 "drop"입니다. 향후 추가 전략이 지원될 수 있다.

### 예시
다음 예에서는 MovieLens 데이터 집합에서 등급 데이터를 로드하며, 각 행은 사용자, 동영상, 등급 및 타임스탬프로 구성된다. 
그런 다음 기본적으로 등급이 명시적이라고 가정하는 ALS 모델을 교육한다(implicitPrefs = False). 
우리는 등급 예측의 평균 제곱근 오류를 측정하여 권장 모델을 평가한다.

API에 대한 자세한 내용은 ALS Scala 문서를 참조하십시오.

{% include_example scala/org/apache/spark/examples/ml/ALSExample.scala %}

등급 매트릭스가 다른 정보 근원(즉, 다른 신호에서 추론됨)에서 파생된 경우 implicitPrefs를 true로 설정하여 더 나은 결과를 얻을 수 있다.

{% highlight scala %} val als = new ALS() .setMaxIter(5) .setRegParam(0.01) .setImplicitPrefs(true) .setUserCol("userId") .setItemCol("movieId") .setRatingCol("rating") {% endhighlight %}

다음 예에서는 MovieLens 데이터 집합에서 등급 데이터를 로드하며, 각 행은 사용자, 동영상, 등급 및 타임스탬프로 구성된다. 
그런 다음 기본적으로 등급이 명시적이라고 가정하는 ALS 모델을 교육한다(implicitPrefs = False). 
우리는 등급 예측의 평균 제곱근 오류(RMSE)를 측정하여 권장 모델을 평가한다.

API에 대한 자세한 내용은 ALS Java 문서를 참조하십시오.

{% include_example java/org/apache/spark/examples/ml/JavaALSExample.java %}

등급 매트릭스가 다른 정보 소스(즉, 다른 신호에서 추론됨)에서 파생된 경우 implicitPrefs를 true로 설정하여 더 나은 결과를 얻을 수 있다.

{% highlight java %} ALS als = new ALS() .setMaxIter(5) .setRegParam(0.01) .setImplicitPrefs(true) .setUserCol("userId") .setItemCol("movieId") .setRatingCol("rating"); {% endhighlight %}

다음 예에서는 MovieLens 데이터 집합에서 등급 데이터를 로드하며, 각 행은 사용자, 동영상, 등급 및 타임스탬프로 구성된다. 
그런 다음 기본적으로 등급이 명시적이라고 가정하는 ALS 모델을 교육한다(implicitPrefs = False). 
우리는 등급 예측의 평균 제곱근 오류(RMSE)를 측정하여 권장 모델을 평가한다.

API에 대한 자세한 내용은 ALS Python 문서를 참조하십시오.

{% include_example python/ml/als_example.py %}

등급 매트릭스가 다른 정보 소스(즉, 다른 신호에서 추론됨)에서 파생된 경우 implicitPrefs를 True로 설정하여 더 나은 결과를 얻을 수 있다.

{% highlight python %} als = ALS(maxIter=5, regParam=0.01, implicitPrefs=True, userCol="userId", itemCol="movieId", ratingCol="rating") {% endhighlight %}

자세한 내용은 R API 문서를 참조하십시오.

{% include_example r/ml/als.R %}