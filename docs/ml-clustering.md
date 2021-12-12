---
layout: global
title: Clustering
displayTitle: Clustering
---

해당 페이지에서는 MLlib의 클러스터링 알고리즘에 대해 설명합니다.
[RDD 기반 API의 클러스터링 가이드](mllib-clustering.html) 에도 이러한 알고리즘에 대한 관련 정보가 존재합니다.


## K-means

[k-means](http://en.wikipedia.org/wiki/K-means_clustering) 데이터 포인트들을 미리 정의된 클러스터 수로 클러스터링하는
가장 일반적으로 사용되는 클러스터링 알고리즘 중 하나입니다.
MLlib 구현에는 [kmeans||](http://theory.stanford.edu/~sergei/papers/vldb12-kmpar.pdf) 라는 [k-means++](http://en.wikipedia.org/wiki/K-means%2B%2B) 메소드의 병렬화된 변형이 포함됩니다.


`KMeans`는 `Estimator`로 구현되며 기본 모델로 `KMeansModel`을 생성합니다.

### 입력

<table class="table">
  <thead>
    <tr>
      <th align="left">파라미터 이름</th>
      <th align="left">타입</th>
      <th align="left">기본값</th>
      <th align="left">설명</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>featuresCol</td>
      <td>Vector</td>
      <td>"features"</td>
      <td>Feature vector</td>
    </tr>
  </tbody>
</table>

### 출력

<table class="table">
  <thead>
    <tr>
      <th align="left">파라미터 이름</th>
      <th align="left">타입</th>
      <th align="left">기본값</th>
      <th align="left">설명</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>predictionCol</td>
      <td>Int</td>
      <td>"prediction"</td>
      <td>예측된 클러스터 센터</td>
    </tr>
  </tbody>
</table>

**예시**

<div class="codetabs">

<div data-lang="scala" markdown="1">

Refer to the [Scala API docs](api/scala/org/apache/spark/ml/clustering/KMeans.html) 를 참조하십시오.

{% include_example scala/org/apache/spark/examples/ml/KMeansExample.scala %}
</div>

<div data-lang="java" markdown="1">

자세한 내용은 [Java API docs](api/java/org/apache/spark/ml/clustering/KMeans.html) 를 참조하십시오.

{% include_example java/org/apache/spark/examples/ml/JavaKMeansExample.java %}
</div>

<div data-lang="python" markdown="1">

자세한 내용은 [Python API docs](api/python/reference/api/pyspark.ml.clustering.KMeans.html) 를 참조하십시오.

{% include_example python/ml/kmeans_example.py %}
</div>

<div data-lang="r" markdown="1">

자세한 내용은 [R API docs](api/R/spark.kmeans.html) 를 참조하십시오.

{% include_example r/ml/kmeans.R %}
</div>

</div>

## Latent Dirichlet allocation (LDA)

`LDA`는 `EMLDAOptimizer`와 `OnlineLDAOptimizer`를 모두 지원하는 `Estimator`로 구현되며
기본 모델로 `LDAModel`을 생성합니다. 전문가는 필요한 경우 `EMLDAOptimizer`에서 생성된 `LDAModel`를
`DistributedLDAModel`로 캐스트할 수 있습니다.


**예시**

<div class="codetabs">

<div data-lang="scala" markdown="1">

자세한 내용은 [Scala API docs](api/scala/org/apache/spark/ml/clustering/LDA.html) 를 참조하십시오.

{% include_example scala/org/apache/spark/examples/ml/LDAExample.scala %}
</div>

<div data-lang="java" markdown="1">

자세한 내용은 [Java API docs](api/java/org/apache/spark/ml/clustering/LDA.html) 를 참조하십시오.

{% include_example java/org/apache/spark/examples/ml/JavaLDAExample.java %}
</div>

<div data-lang="python" markdown="1">

자세한 내용은 [Python API docs](api/python/reference/api/pyspark.ml.clustering.LDA.html) 를 참조하십시오.

{% include_example python/ml/lda_example.py %}
</div>

<div data-lang="r" markdown="1">

자세한 내용은 [R API docs](api/R/spark.lda.html) 를 참조하십시오.

{% include_example r/ml/lda.R %}
</div>

</div>

## Bisecting k-means

`BisectingKMeans`는 분할(혹은 "top-down") 접근 방식을 사용하는 일종의 [hierarchical clustering](https://en.wikipedia.org/wiki/Hierarchical_clustering) 입니다.
모든 관찰은 하나의 클러스터에서 시작하고 분할은 계층 아래로 이동함에 따라 재귀적으로 수행됩니다.

`BisectingKMeans`는 종종 일반 K-means보다 훨씬 빠를 수 있지만 일반적으로 다른 클러스터를 생성합니다.

`BisectingKMeans`는 `Estimator`로 구현되며 `BisectingKMeansModel`를 기본 모델로 생성합니다.

**예시**

<div class="codetabs">

<div data-lang="scala" markdown="1">

자세한 내용은 [Scala API docs](api/scala/org/apache/spark/ml/clustering/BisectingKMeans.html) 를 참조하십시오.

{% include_example scala/org/apache/spark/examples/ml/BisectingKMeansExample.scala %}
</div>

<div data-lang="java" markdown="1">

자세한 내용은 [Java API docs](api/java/org/apache/spark/ml/clustering/BisectingKMeans.html) 를 참조하십시오.

{% include_example java/org/apache/spark/examples/ml/JavaBisectingKMeansExample.java %}
</div>

<div data-lang="python" markdown="1">

자세한 내용은 [Python API docs](api/python/reference/api/pyspark.ml.clustering.BisectingKMeans.html) 를 참조하십시오.

{% include_example python/ml/bisecting_k_means_example.py %}
</div>

<div data-lang="r" markdown="1">

자세한 내용은 [R API docs](api/R/spark.bisectingKmeans.html) 를 참조하십시오.

{% include_example r/ml/bisectingKmeans.R %}
</div>
</div>

## Gaussian Mixture Model (GMM)

[Gaussian Mixture Model](http://en.wikipedia.org/wiki/Mixture_model#Multivariate_Gaussian_mixture_model)은
각각 고유한 확률을 가진 *k*개의 가우시안 하위 분포 중 하나에서 점이 추출되는 복합 분포를 나타냅니다.
`spark.ml` 구현은 [expectation-maximization](http://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm) 
알고리즘을 사용하여 주어진 샘플 세트에서 maximum-likelihood 모델을 유도합니다.

`GaussianMixture`는 `Estimator`로 구현되며 기본 모델로 `GaussianMixtureModel`을 생성합니다.

### Input Columns

<table class="table">
  <thead>
    <tr>
      <th align="left">파라미터 이름</th>
      <th align="left">타입</th>
      <th align="left">기본값</th>
      <th align="left">설명</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>featuresCol</td>
      <td>Vector</td>
      <td>"features"</td>
      <td>Feature vector</td>
    </tr>
  </tbody>
</table>

### Output Columns

<table class="table">
  <thead>
    <tr>
      <th align="left">파라미터 이름</th>
      <th align="left">타입</th>
      <th align="left">기본값</th>
      <th align="left">설명</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>predictionCol</td>
      <td>Int</td>
      <td>"prediction"</td>
      <td>예측된 클러스터 센터</td>
    </tr>
    <tr>
      <td>probabilityCol</td>
      <td>Vector</td>
      <td>"probability"</td>
      <td>각 클러스터의 확률</td>
    </tr>
  </tbody>
</table>

**Examples**

<div class="codetabs">

<div data-lang="scala" markdown="1">

자세한 내용은 [Scala API docs](api/scala/org/apache/spark/ml/clustering/GaussianMixture.html) 를 참조하십시오.

{% include_example scala/org/apache/spark/examples/ml/GaussianMixtureExample.scala %}
</div>

<div data-lang="java" markdown="1">

자세한 내용은 [Java API docs](api/java/org/apache/spark/ml/clustering/GaussianMixture.html) 를 참조하십시오.

{% include_example java/org/apache/spark/examples/ml/JavaGaussianMixtureExample.java %}
</div>

<div data-lang="python" markdown="1">

자세한 내용은 [Python API docs](api/python/reference/api/pyspark.ml.clustering.GaussianMixture.html) 를 참조하십시오.

{% include_example python/ml/gaussian_mixture_example.py %}
</div>

<div data-lang="r" markdown="1">

자세한 내용은 [R API docs](api/R/spark.gaussianMixture.html) 를 참조하십시오.

{% include_example r/ml/gaussianMixture.R %}
</div>

</div>

## Power Iteration Clustering (PIC)

Power Iteration Clustering (PIC)는 [Lin and Cohen](http://www.cs.cmu.edu/~frank/papers/icml2010-pic-final.pdf)이 개발한
확장 가능한 그래프 클러스터링 알고리즘입니다.
요약 발췌: PIC는 데이터의 정규화된 쌍(pair)별 유사성 매트릭스에서 잘린 거듭제곱 반복을 사용하여 데이터셋의 매우 낮은 차원의 임베딩을 찾습니다.

`spark.ml`의 PowerIterationClustering 구현은 다음 파라미터를 사용합니다:

* `k`: 생성할 클러스터의 수
* `initMode`: 초기화 알고리즘의 파라미터
* `maxIter`: 최대 반복 횟수에 대한 파라미터
* `srcCol`: source vertex ID에 대한 입력 열 이름의 파라미터
* `dstCol`: destination vertex ID에 대한 입력 열의 이름
* `weightCol`: 가중치 열 이름의 파라미터

**예시**

<div class="codetabs">

<div data-lang="scala" markdown="1">

자세한 내용은 [Scala API docs](api/scala/org/apache/spark/ml/clustering/PowerIterationClustering.html) 를 참조하십시오.

{% include_example scala/org/apache/spark/examples/ml/PowerIterationClusteringExample.scala %}
</div>

<div data-lang="java" markdown="1">

자세한 내용은 [Java API docs](api/java/org/apache/spark/ml/clustering/PowerIterationClustering.html) 를 참조하십시오.

{% include_example java/org/apache/spark/examples/ml/JavaPowerIterationClusteringExample.java %}
</div>

<div data-lang="python" markdown="1">

자세한 내용은 [Python API docs](api/python/reference/api/pyspark.ml.clustering.PowerIterationClustering.html) 를 참조하십시오.

{% include_example python/ml/power_iteration_clustering_example.py %}
</div>

<div data-lang="r" markdown="1">

자세한 내용은 [R API docs](api/R/spark.powerIterationClustering.html) 를 참조하십시오.

{% include_example r/ml/powerIterationClustering.R %}
</div>

</div>
