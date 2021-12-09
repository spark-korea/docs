---
layout: global
title: ML `Pipeline`
displayTitle: ML `Pipeline`
---


* Table of contents
{:toc}


이 섹션에서는 **ML `Pipeline`**의 개념을 소개하겠습니다. ML `Pipeline`은 사용자가 실용적인 머신러닝 `Pipeline`을 만들고 조정하는 데 도움이 되는 [DataFrames](https://spark.apache.org/docs/latest/sql-programming-guide.html) 위에 구축된 통일된 고급 API 세트를 제공합니다.

# `Pipeline`의 주요 개념
MLlib은 머신러닝 알고리즘용 API를 표준화하여 여러 알고리즘을 단일 `Pipeline` 또는 워크플로우에 쉽게 결합할 수 있도록 합니다. 이 섹션에서는 주로 [scikit-learn](https://scikit-learn.org/stable/) 프로젝트에서 영감을 받았던, Pipeline API에서 소개된 `Pipeline` 주요 개념입니다.

* `DataFrame`: 이 ML API는 Spark SQL의 `DataFrame`을 다양한 데이터 유형을 저장할 수 있는 ML 데이터 세트로 사용합니다. 예를 들어, `DataFrame`은 text, feature vertors, true labels 및 predictions을 저장하는 다른 열을 가질 수 있습니다.

* `Transformer`: `Transformer`는 하나의 `DataFrame`을 다른 `DataFrame`로 변환할 수 있는 알고리즘이다. 예를 들어, ML 모델은 특징이 있는 `DataFrame`을 예측이 있는 `DataFrame`으로 변환하는 `Transformer`이다.

* `Estimator`: `Estimator`는 `Transformer`를 생성하기 위해 `DataFrame`에 적합할 수 있는 알고리즘입니다. 예를 들어, 학습 알고리즘은 `DataFrame`에서 훈련하고 모델을 생성하는 `Estimator`이다.

* `Pipeline`: `Pipeline`은 ML 워크플로우를 지정하기 위해 여러 `Transformer`와 `Estimator`를 서로 연결합니다.

* `Parameter`: 모든 `Transformer`와 `Estimator`는 매개 변수를 지정하기 위한 공통 API를 공유합니다.

## DataFrame
머신러닝은 vectors, text, images, 구조화된 데이터(structured data) 와 같은 다양한 데이터 유형에 적용할 수 있습니다. 이 API는 다양한 데이터 유형을 지원하기 위해 Spark SQL의 `DataFrame`을 채택했습니다.

`DataFrame`은 많은 기본 및 구조화된 유형을 지원합니다. 지원되는 유형의 목록은 [Spark SQL 데이터 유형 참조](https://spark.apache.org/sql-ref.html) 에서 확인할 수 있습니다. `DataFrame`은 Spark SQL 가이드에 나와 있는 타입 외에도 ML [Vector](https://spark.apache.org/docs/latest/mllib-data-types.html#local-vector) 타입을 사용할 수 있습니다.

`DataFrame`은 일반 `RDD`로부터 암시적으로 또는 명시적으로 생성될 수 있습니다. 아래의 코드 예제와 [Spark SQL 프로그래밍 가이드](https://spark.apache.org/docs/latest/sql-programming-guide.html) 를 참조할 수 있습니다.

`DataFrame`의 열에는 이름이 지정됩니다. 아래의 코드 예제는 "text", "features" 및 "label"과 같은 이름을 사용합니다.

## `Pipeline`의 요소
### Transformers

`Transformer`는 feature transformers와 학습된 모델을 포함하는 추상화입니다. 기술적으로 `Transformer`는  `transformer()` 메소드를 구현하며, 일반적으로 하나 이상의 열을 추가함으로써 하나의 `DataFrame`을 다른 `DataFrame`으로 변환한다. 예를 들면,

* feature transformer는 `DataFrame`을 사용하고, column(예: text)을 읽고, 이를 새로운 column(예: feature vectors)로 매핑하고, 매핑된 column이 추가된 새 `DataFrame`을 출력할 수 있습니다.

* 학습 모델은 `DataFrame`을 사용하고, feature vectors가 들어 있는 column을 읽고, 각 feature vectors의 label을 예측하고, 예측한 label이 column로 추가된 새 DataFrame을 출력할 수 있습니다.

### Estimators
`Estimator`는 학습 알고리즘 또는 데이터에 적합하거나 훈련하는 알고리즘의 개념을 추상화합니다. 기술적으로 `Estimator`는 `fit()` 메소드를 구현하는데, 이 메소드는 `DataFrame`을 수용하고 `Transformer`인 모델을 생성합니다. 예를 들어, `LogisticRegression`과 같은 학습 알고리즘은 `Estimator`이고 `fit()`을 호출하면 모델인 `LigisticRegressionModel`을 학습하며, 이는 `Transformer`가 됩니다.

### `Pipeline` 구성 요소의 속성
`Transformer.transform()`와 `Estimator.fit()`는 모두 상태를 저장하지 않습니다. 후에 상태 저장 알고리즘이 대체 개념을 통해 지원될 수 있습니다.

각 `Transformer` 또는 `Estimator` 인스턴스는 매개 변수를 지정하는 데 유용한 고유한 ID를 가집니다.(아래에서 설명)

## `Pipeline`
머신러닝에서는 일련의 알고리즘을 실행하여 데이터를 처리하고 학습하는 것이 일반적입니다. 예를 들어, 간단한 텍스트 문서 처리 워크플로우에는 다음과 같은 여러 단계가 포함될 수 있습니다.

* 각 문서의 텍스트를 단어로 분할합니다.
* 각 문서의 단어를 숫자 피쳐 벡터로 변환합니다.
* feature vectors와 labels를 사용하여 예측 모델을 학습합니다.

MLlib는 `Pipeline`과 같은 워크플로를 나타내며, `Pipeline`은 특정 순서로 실행될 `PipelineStages`(`Transformers` 및 `Estimators`)의 시퀀스로 구성됩니다. 이 섹션에서는 이 간단한 워크플로우를 실행 예제로 사용할 것입니다.

### 작동 방식
`Pipeline`은 일련의 단계로 지정되며, 각 단계는 `Transformer` 또는 `Estimator`입니다. 이 단계들은 순서대로 실행되며, 입력 `DataFrame`은 각 단계를 통과하면서 변환됩니다. `Transformer` 단계의 경우, `DataFrame`에서 `transform()` 메소드가 호출됩니다. `Estimator` 단계의 경우, `fit()` 메소드는 `Transformer`를 생성하기 위해 호출되며 (`PipelineModel` 또는 `Pipeline`의 일부가 됨), `Transformer`의 `transform()` 메소드는 `DataFrame`에서 호출됩니다.

간단한 텍스트 문서 워크플로우에 대해 설명하겠습니다. 아래 그림은 `Pipeline`의 _training time_ 사용에 대한 것입니다.


![image](https://user-images.githubusercontent.com/63892688/145415890-9b4b8d2e-9d3f-471c-a151-0cbd65bcb46b.png)

위쪽 행은 3단계로 구성된 `Pipeline`을 나타냅니다. 처음 두 가지(`Tokenizer` 및 `HashingTF`)는 `Transformers`(파란색)이고 세 번째(`LogisticRegression`)는 `Estimator`(빨간색)입니다. 아래쪽 행은 `Pipeline`을 통과하는 데이터를 나타내며, 여기서 원기둥은 `DataFrames`를 나타냅니다. `Pipeline.fit()` 메소드는 기존 텍스트 문서와 레이블이 있는 원본 `DataFrame`에서 호출됩니다. `Tokenizer.transform()` 메소드는 기존 텍스트 문서를 단어로 분할하여 단어가 포함된 새 열을 `DataFrame`에 추가합니다. `HashingTF.transform()` 방법은 단어 열을 feature vectors로 변환하고 이러한 벡터가 있는 새 열을 데이터 프레임에 추가합니다. 이제 `LogisticRegression``은 `Estimator`이므로 `Pipeline`은 먼저 LogisticRegression.fit()`을 호출하여 `LogisticRegressionModel`을 생성합니다. `Pipeline`에 `Estimator`가 더 많으면 `DataFrame`을 다음 단계로 전달하기 전에 `DataFrame`에서 `LogisticRegressionModel`의 `transform()` 메소드를  호출합니다.

`Pipeline`은 `Estimator`입니다. 따라서 `Pipeline`의 `fit()` 메소드가 실행된 후 `Transformer`인 `PipelineModel`을 생성합니다. 이 `PipelineModel`은 _test time_ 에 사용되며, 아래 그림은 해당 사용을 보여줍니다.
![image](https://user-images.githubusercontent.com/63892688/145417762-383139a2-e101-451c-8fc6-473e852158d4.png)

위의 그림에서 `PipelineModel`은 원래 `Pipeline`과 단계 수가 동일하지만, 기존 `Pipeline`의 모든 `Estimators`가 `Transformers`로 되었습니다. 테스트 데이터 세트에서 `PipelineModel`의 `transform()` 메소드가 호출되면, 데이터가 적합한 파이프라인을 순서대로 통과합니다. 각 단계의 `transform()` 메소드는 데이터 집합을 갱신하고 다음 단계로 전달합니다.

`Pipeline` 및 `PipelineModels`는 트레이닝 및 테스트 데이터가 동일한 기능 처리 단계를 거치도록 지원합니다.