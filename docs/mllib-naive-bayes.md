
---

|layout|title|displayTitle|
|--|--|--|
| global | Naive Bayes - RDD-based API|Naive Bayes - RDD-based API

해당 페이지에서는 MLlib의 나이브 베이즈에 대해 설명합니다. 

---
나이브 베이즈는 모든 특징 쌍 사이의 독립성을 가정하는 간단한 다중 클래스 분류 알고리즘입니다. 나이브 베이즈는 매우 효율적으로 훈련될 수 있습니다. 훈련 데이터에 대해 단일 패스 내에서, 이것은 주어진 각 피처의 조건부 확률 분포를 계산한 다음 베이즈의 정리를 적용하여 주어진 관측치의 조건부 확률 분포를 계산하고 예측에 사용합니다. 
`spark.mllib` 은  [다항분포 나이브 베이즈](http://en.wikipedia.org/wiki/Naive_Bayes_classifier#Multinomial_naive_Bayes) 와 [베르누이 나이브 베이즈](http://nlp.stanford.edu/IR-book/html/htmledition/the-bernoulli-model-1.html)를 지원합니다. 이러한 모델은 일반적으로 [문서분류](http://nlp.stanford.edu/IR-book/html/htmledition/naive-bayes-text-classification-1.html) 에서 사용됩니다. 이 맥락에서, 각각의 관측치는 문서이고, 각 특징은 (다항분포 나이브 베이즈에서) 용어의 빈도 또는 (베르누이 나이브베이즈에서) 용어의 발견 여부를 나타내는 0또는 1의 값이 나타나는 항을 표현합니다. 피처 값은 음수가 아니어야 합니다. 모델 유형은 선택적 매개변수인 "다항" 또는 "베르누이"를 기본 값으로 사용하여 선택됩니다. [Additive smoothing](http://en.wikipedia.org/wiki/Lidstone_smoothing) 은 매개변수 
$\lambda$ (default to $1.0$) 를 설정해서 사용합니다. 문서 분류를 위해 입력 특징 벡터는 일반적으로 희소하며 희소성을 이용하기 위해서는 희소 벡터가 입력으로 제공되어야 합니다. 훈련 데이터는 한 번만 사용되므로 캐시할 필요가 없습니다. 
