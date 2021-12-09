---
layout: global
title: ML `Pipeline`
displayTitle: ML `Pipeline`
---


* Table of contents
{:toc}


이 섹션에서는 `ML Pipeline`의 개념을 소개하겠습니다. ML Pipelin은 사용자가 실용적인 머신러닝 파이프라인을 만들고 조정하는 데 도움이 되는 [DataFrames](https://spark.apache.org/docs/latest/sql-programming-guide.html) 위에 구축된 통일된 고급 API 세트를 제공합니다.

# Pipeline의 주요 개념
MLlib은 머신러닝 알고리즘용 API를 표준화하여 여러 알고리즘을 단일 파이프라인 또는 워크플로우에 쉽게 결합할 수 있도록 합니다. 이 섹션에서는 주로 [scikit-learn](https://scikit-learn.org/stable/) 프로젝트에서 영감을 받았던, Pipeline API에서 소개된 파이프라인의 주요 개념입니다.

* `DataFrame`: 이 ML API는 Spark SQL의 DataFrame을 다양한 데이터 유형을 저장할 수 있는 ML 데이터 세트로 사용합니다. 예를 들어, DataFrame은 text, feature vertors, true labels 및 예측(predictions)을 저장하는 다른 열을 가질 수 있습니다.

* `Transformer`: Transformer는 하나의 데이터프레임을 다른 데이터프레임으로 변환할 수 있는 알고리즘입니다. 예를 들어, ML 모델은 feature가 있는 데이터프레임을 예측 값이 있는 데이터프레임으로 변환하는 Transformer입니다.

* `Estimator`: Estimator는 Transformer를 생성하기 위해 데이터프레임에 적합할 수 있는 알고리즘입니다. 예를 들어, 학습 알고리즘은 데이터프레임에서 훈련하고 모델을 생성하는 Estimator입니다.

* `Pipeline`: 파이프라인은 ML 워크플로우를 지정하기 위해 여러 Transformer와 Estimator를 서로 연결합니다.

* `Parameter`: 모든 Transformer와 Estimator는 매개 변수를 지정하기 위한 공통 API를 공유합니다.

## DataFrame
머신러닝은 vectors, text, images, 구조화된 데이터(structured data) 와 같은 다양한 데이터 유형에 적용할 수 있습니다. 이 API는 다양한 데이터 유형을 지원하기 위해 Spark SQL의 `DataFrame`을 채택했습니다.

데이터프레임은 많은 기본 및 구조화된 유형을 지원합니다. 지원되는 유형의 목록은 [Spark SQL 데이터 유형 참조](https://spark.apache.org/sql-ref.html) 에서 확인할 수 있습니다. 데이터프레임은 Spark SQL 가이드에 나와 있는 타입 외에도 ML [Vector](https://spark.apache.org/docs/latest/mllib-data-types.html#local-vector) 타입을 사용할 수 있습니다.

데이터프레임은 일반 `RDD`로부터 암시적으로 또는 명시적으로 생성될 수 있습니다. 아래의 코드 예제와 [Spark SQL 프로그래밍 가이드](https://spark.apache.org/docs/latest/sql-programming-guide.html) 를 참조할 수 있습니다.

데이터프레임의 열에는 이름이 지정됩니다. 아래의 코드 예제는 "text", "features" 및 "label"과 같은 이름을 사용합니다.

## Pipeline의 요소
### Transformers

`Transformer`는 feature transformers와 학습된 모델을 포함하는 추상화입니다. 기술적으로 Transformer는  `transformer()` 메소드를 구현하며, 일반적으로 하나 이상의 열을 추가함으로써 하나의 데이터프레임을 다른 데이터프레임으로 변환합니다. 예를 들면,

* feature transformer는 데이터프레임을 사용하고, 열(예: text)을 읽습니다. 이를 새로운 열(예: feature vectors)로 매핑하고, 매핑된 열이 추가된 새 데이터프레임을 출력할 수 있습니다.

* 학습 모델은 데이터프레임을 사용하고, feature vectors가 들어 있는 열을 읽고, 각 feature vectors의 label을 예측하고, 예측한 label이 열로 추가된 새 데이터프레임을 출력할 수 있습니다.

### Estimators
`Estimator`는 학습 알고리즘 또는 데이터에 적합하거나 훈련하는 알고리즘의 개념을 추상화합니다. 기술적으로 Estimator는 `fit()` 메소드를 구현하는데, 이 메소드는 데이터프레임을 수용하고 Transformer인 모델을 생성합니다. 예를 들어, `LogisticRegression`과 같은 학습 알고리즘은 Estimator이고, `fit()`을 호출하면 모델인 `LigisticRegressionModel`을 학습하여 Transformer가 됩니다.

### Pipeline 구성 요소의 속성
`Transformer.transform()`와 `Estimator.fit()`는 모두 상태를 저장하지 않습니다. 후에 상태 저장 알고리즘이 대체 개념을 통해 지원될 수 있습니다.

각 Transformer 또는 Estimator 인스턴스는 매개 변수를 지정하는 데 유용한 고유한 ID를 가집니다.(아래에서 설명)

## Pipeline
머신러닝에서는 일련의 알고리즘을 실행하여 데이터를 처리하고 학습하는 것이 일반적입니다. 예를 들어, 간단한 텍스트 문서 처리 워크플로우에는 다음과 같은 여러 단계가 포함될 수 있습니다.

* 각 문서의 텍스트를 단어로 분할합니다.
* 각 문서의 단어를 숫자 피쳐 벡터로 변환합니다.
* feature vectors와 labels를 사용하여 예측 모델을 학습합니다.

MLlib는 파이프라인과 같은 워크플로를 나타내며, 파이프라인은 특정 순서로 실행될 `PipelineStages` (Transformers 및 Estimators)의 시퀀스로 구성됩니다. 이 섹션에서는 이 간단한 워크플로우를 실행 예제로 사용할 것입니다.

### 작동 방식
파이프라인은 일련의 단계로 지정되며, 각 단계는 Transformer 또는 Estimator로 나뉩니다. 이 단계들은 순서대로 실행되며, 입력 데이터프레임은 각 단계를 통과하면서 변환됩니다. Transformer 단계의 경우, 데이터프레임에서 `transform()` 메소드가 호출됩니다. Estimator 단계의 경우, `fit()` 메소드는 Transformer를 생성하기 위해 호출되며 (파이프라인 모델 또는 파이프라인의 일부가 됨), Transformer의 `transform()` 메소드는 데이터프레임에서 호출됩니다.

간단한 텍스트 문서 워크플로우에 대해 설명하겠습니다. 아래 그림은 파이프라인의 _training time_ 사용에 대한 것입니다.

![image](https://user-images.githubusercontent.com/63892688/145415890-9b4b8d2e-9d3f-471c-a151-0cbd65bcb46b.png)

위쪽 행은 3단계로 구성된 파이프라인을 나타냅니다. 처음 두 가지(`Tokenizer` 및 `HashingTF`)는 Transformers (파란색)이고 세 번째(`LogisticRegression`)는 Estimator (빨간색)입니다. 아래쪽 행은 파이프라인을 통과하는 데이터를 나타내며, 여기서 원기둥은 데이터프레임을 나타냅니다. `Pipeline.fit()` 메소드는 기존 텍스트 문서와 레이블이 있는 기존 데이터프레임에서 호출됩니다. `Tokenizer.transform()` 메소드는 기존 텍스트 문서를 단어로 분할하여 단어가 포함된 새 열을 데이터프레임에 추가합니다. `HashingTF.transform()` 방법은 단어 열을 feature vectors로 변환하고 이러한 벡터가 있는 새 열을 데이터 프레임에 추가합니다. 이제 LogisticRegression은 Estimator이므로 파이프라인은 먼저 `LogisticRegression.fit()`을 호출하여 LogisticRegressionModel을 생성합니다. 파이프라인에 Estimator가 더 많으면 데이터프레임을 다음 단계로 전달하기 전에 데이터프레임에서 `LogisticRegressionModel`의 `transform()` 메소드를  호출합니다.

파이프라인은 Estimator입니다. 따라서 파이프라인의 `fit()` 메소드가 실행된 후 Transformer인 `PipelineModel`을 생성합니다. 이 파이프라인 모델은 _test time_ 에 사용되며, 아래 그림은 해당 사용을 보여줍니다.

![image](https://user-images.githubusercontent.com/63892688/145417762-383139a2-e101-451c-8fc6-473e852158d4.png)

위의 그림에서 파이프라인 모델은 원래 파이프라인과 단계 수가 동일하지만, 기존 파이프라인의 모든 Estimators가 Transformers로 되었습니다. 테스트 데이터 세트에서 파이프라인 모델의 `transform()` 메소드가 호출되면, 데이터가 적합한 파이프라인을 순서대로 통과합니다. 각 단계의 `transform()` 메소드는 데이터 집합을 갱신하고 다음 단계로 전달합니다.

파이프라인 및 파이프라인 모델들은 학습 및 테스트 데이터가 동일한 기능 처리 단계를 거치도록 지원합니다.

### 세부 사항
`DAG pipelines` (DAG 파이프라인): 파이프라인의 단계가 순서 배열로 지정됩니다. 여기에 제시된 예는 모두 선형 파이프라인, 즉 각 단계가 이전 단계에서 생성된 데이터를 사용하는 파이프라인에 대한 것입니다. 데이터 흐름 그래프가 `DAG(Directed Acyclic Graph)`를 형성하는 하나의 비선형 파이프라인을 만들 수 있습니다. 이 그래프는 현재 각 단계의 입력 및 출력 열 이름(일반적으로 파라미터로 지정)을 기반으로 암시적으로 지정됩니다. 파이프라인이 DAG를 형성하는 경우, 단계를 위상 순서(topological order)로 지정해야 합니다.

`Runtime checking` (런타임 검사): 파이프라인은 다양한 타입의 데이터프레임에서 동작할 수 있기 때문에, 컴파일-타임 타입 체크를 사용할 수 없습니다. 파이프라인 및 파이프라인 모델은 실제로 파이프라인을 실행하기 전에 런타임 검사를 대신 수행합니다. 이 검사는 데이터 프레임에 있는 열의 데이터 유형에 대한 설명인 데이터 프레임 스키마를 사용하여 수행됩니다.

`Unique Pipeline stages` (고유 파이프라인 단계): 파이프라인의 단계는 고유한 인스턴스여야 합니다. 예를 들면, 동일한 인스턴스인 myHashingTF가 고유 ID를 가져야 하므로 파이프라인에 두 번 삽입하면 안 됩니다. 그러나 다른 경우, myHashingTF1 및 myHashingTF2 (HashingTF 유형 모두)는 다른 ID로 다른 인스턴스가 생성되므로 동일한 파이프라인에 넣을 수 있습니다.

## 매개 변수
MLlib Estimator 및 Transformer는 매개 변수를 지정하기 위해 균일한 API를 사용합니다.

`Param`은 자체적으로 설명서가 포함되어 있는 명명된 매개 변수입니다. `ParamMap`은 (parameter, value) 쌍의 집합입니다.

알고리즘에 매개 변수를 전달하는 방법에는 두 가지가 있습니다.

1. 인스턴스의 매개 변수를 설정합니다. 예를 들어 lr이 LogisticRegression의 인스턴스인 경우, `lr.setMaxIter(10)`를 호출하여 `lr.fit()`을 최대 10회 반복 사용하도록 할 수 있습니다. 이 API는 `spark.mllib` 패키지에 사용되는 API와 유사합니다.

2. ParamMap을 전달하여 `fit()` 또는 `transform()`합니다. ParamMap의 모든 매개 변수는 `setter` 메서드를 통해 이전에 지정한 매개 변수를 재정의합니다.

매개 변수는 Estimators 및 Transformers의 특정 인스턴스에 속합니다. 예를 들어, 두 개의 LogisticRegression 인스턴스 lr1과 lr2가 있는 경우 `ParamMap(lr1.maxIter -> 10, lr2.maxIter -> 20)`과 같이 두 개의 `maxIter ` 매개 변수를 모두 지정하여 ParamMap을 작성할 수 있습니다. 파이프라인에 maxIter 매개 변수를 가진 알고리즘이 두 개 있는 경우 유용하게 사용될 수 있습니다.

## ML 지속성: 파이프라인 저장 및 로드

모델이나 파이프라인을 나중에 사용할 수 있도록 디스크에 저장하는 것이 유용한 경우가 많습니다. Spark 1.6에서는 모델 가져오기/내보내기 기능이 파이프라인 API에 추가되었습니다. Spark 2.3 기준으로 `spark.ml` 및 `pyspark.ml`의 DataFrame 기반 API는 완전한 커버리지를 제공합니다.

ML 지속성(persistence)은 Scala, Java 및 Python 전체에서 작동합니다. 그러나 R은 현재 수정된 형식을 사용하므로 R에 저장된 모델은 R에서만 다시 로드할 수 있습니다. 이 작업은 나중에 수정되어야 하며 [SPARK-15572](https://issues.apache.org/jira/browse/SPARK-15572r) 에서 확인할 수 있습니다.

### ML 지속성을 위한 하위 호환성
일반적으로 MLlib는 ML 지속성을 위해 하위 호환성을 유지합니다. 즉, ML 모델 또는 Pipeline을 한 버전의 Spark에 저장한 경우 다시 로드하여 향후 버전의 Spark에서 사용할 수 있습니다. 그러나 아래에 설명된 드문 예외가 있습니다.

Model persistence (모델 지속성): Spark 버전 X에서 Apache Spark ML 지속성을 사용하여 저장한 모델 또는 Pipeline은 Spark 버전 Y에서 로드할 수 있습니까?

* 주 버전: 보장은 없지만 최선의 노력입니다.
* 부 버전 및 패치 버전: 예, 이것들은 역호환성이 있습니다.
* 형식에 대한 참고: 안정적인 지속성 포맷에 대한 보장은 없지만 모델 로딩 자체는 역호환성을 갖도록 설계되었습니다.

Model behavior (모델 동작): 스파크 버전 X의 모델이나 파이프라인은 스파크 버전 Y에서도 동일하게 동작합니까?

* 주 버전: 보장은 없지만 최선의 노력입니다.
* 부 버전 및 패치 버전: 버그 수정을 제외하고 동일한 동작입니다.

모델 지속성과 모델 동작 모두에 대해 부 버전 또는 패치 버전 간에 변경된 내용이 Spark 버전 릴리스 정보에 보고됩니다. 릴리스 노트에 파손이 보고되지 않은 경우 수정해야 할 버그로 간주해야 합니다.

# 예제 코드
이 섹션에서는 위에서 설명한 기능을 설명하는 코드 예를 제공합니다. 자세한 내용은 API 설명서 ([Scala](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/ml/package.html), [Java](https://spark.apache.org/docs/latest/api/java/org/apache/spark/ml/package-summary.html) 및 [Python](https://spark.apache.org/docs/latest/api/python/reference/pyspark.ml.html)) 를 참조할 수 있습니다.

## 예제: Estimator, Transformer 와 Param
이 예제는 Estimator, Transformer 와 Param에 대해 다룹니다.


Scala 예제는 다음과 같습니다. API에 대한 자세한 내용은 [Estimator Scala 문서](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/ml/Estimator.html), [Transformer Scala 문서](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/ml/Transformer.html) 및 [Params Scala 문서](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/ml/param/Params.html)를 확인하세요.

{% include_example examples/src/main/scala/org/apache/spark/examples/ml/PipelineExample.scala %}

Java 예제는 다음과 같습니다. API에 대한 자세한 내용은 [Estimator Java 문서](https://spark.apache.org/docs/latest/api/java/org/apache/spark/ml/Estimator.html), [Transformer Java 문서](https://spark.apache.org/docs/latest/api/java/org/apache/spark/ml/Transformer.html) 및 [Params Java 문서](https://spark.apache.org/docs/latest/api/java/org/apache/spark/ml/param/Params.html)를 확인하세요.

{% include_example examples/src/main/java/org/apache/spark/examples/ml/JavaEstimatorTransformerParamExample.java %}

Python 예제는 다음과 같습니다. API에 대한 자세한 내용은 [Estimator Python 문서](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.Estimator.html), [Transformer Python 문서](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.Transformer.html) 및 [Params Python 문서](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.param.Params.html)를 확인하세요.

{% include_example examples/src/main/python/ml/estimator_transformer_param_example.py %}

## 예제: Pipeline
이 예제는 위의 그림에 설명된 간단한 텍스트 문서 Pipeline에 대해 다룹니다.

Scala 예제는 다음과 같습니다. API에 대한 자세한 내용은 [Pipeline Scala 문서](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/ml/Pipeline.html) 를 확인하세요.

{% include_example examples/src/main/scala/org/apache/spark/examples/ml/PipelineExample.scala %}

Java 예제는 다음과 같습니다. API에 대한 자세한 내용은 [Pipeline Java 문서](https://spark.apache.org/docs/latest/api/java/org/apache/spark/ml/Pipeline.html) 를 확인하세요.

{% include_example examples/src/main/java/org/apache/spark/examples/ml/JavaPipelineExample.java %}

Python 예제는 다음과 같습니다. API에 대한 자세한 내용은 [Pipeline Python 문서](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.Pipeline.html) 를 확인하세요.

{% include_example examples/src/main/python/ml/pipeline_example.py %}

## 모델 선택 (하이퍼파라미터 조정)
ML 파이프라인 사용의 큰 이점은 하이퍼 파라미터 최적화입니다. 자동 모델 선택에 대한 자세한 내용은 [ML Tuning Guide](https://spark.apache.org/docs/latest/ml-tuning.html) 를 참조하세요.