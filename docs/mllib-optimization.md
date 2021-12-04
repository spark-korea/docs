---
layout: global
title: 최적화 - RDD 기반 API
displayTitle: 최적화 - RDD 기반 API
license: |
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at
 
     http://www.apache.org/licenses/LICENSE-2.0
 
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
---

* 목차
{:toc}

`\[
\newcommand{\R}{\mathbb{R}}
\newcommand{\E}{\mathbb{E}} 
\newcommand{\x}{\mathbf{x}}
\newcommand{\y}{\mathbf{y}}
\newcommand{\wv}{\mathbf{w}}
\newcommand{\av}{\mathbf{\alpha}}
\newcommand{\bv}{\mathbf{b}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\id}{\mathbf{I}} 
\newcommand{\ind}{\mathbf{1}} 
\newcommand{\0}{\mathbf{0}} 
\newcommand{\unit}{\mathbf{e}} 
\newcommand{\one}{\mathbf{1}} 
\newcommand{\zero}{\mathbf{0}}
\]`



## 수학적 설명

### 경사 하강법
`$\min_{\wv \in\R^d} \; f(\wv)$` 형태의 최적화 문제를 해결하는 가장 단순한 방법 중 하나는 [경사 하강법](http://en.wikipedia.org/wiki/Gradient_descent)이다.
경사 하강법, stochastic variants thereof와 같은 1차 최적화 기법은 대규모, 분산 컴퓨팅에 적합하다.

경사 하강법은 함수의 미분계수에 -1을 곱한 값([gradient](http://en.wikipedia.org/wiki/Gradient))인 가장 가파른 하강 방향으로 반복적으로 전진하면서 그 함수의 지역적 최소값을 찾는 것을 목표로 한다.
목적 함수 `$f$`가 모든 인자로 미분가능하지 않지만 차트가 오목하다면 *하위 그래디언트*가 그래디언트의 자연스러운 일반화일 것이고 전진 방향의 역할을 가정한다.
어떤 경우에서든 모든 손실값을 계산하기위해 데이터셋 전체에 걸쳐 `$f$`의 그래디언트나 하위 그래디언트를 계산하는 연산은 비싸다.

### 스토캐스틱 경사 하강법 (SGD)
목적 함수 `$f$`가 합으로 표현된 최적화 문제는 특히나 *스토캐스틱 경사 하강법*으로 해결하는게 적합하다.
우리의 경우에는 일반적으로 다음 최적화 공식을 <a href="mllib-classification-regression.html">기계 지도 학습</a>에서 일반적으로 사용한다.
`\begin{equation}
    f(\wv) := 
    \lambda\, R(\wv) +
    \frac1n \sum_{i=1}^n L(\wv;\x_i,y_i) 
    \label{eq:regPrimal}
    \ .
\end{equation}`
이 손실 함수는 각 데이터 포인트의 손실값의 평균으로 기술되었기때문에 특히 자연스럽다.

스토캐스틱 하위 그래디언트는 원래의 목적 함수의 하위 그래디언트를 얻을 것을 기대하며 벡터를 무작위로 선택하는 방법이다.
`$L'_{\wv,i} \in \R^d$`를 `$i$`번째 데이터포인트에서 결정되는 손실 함수의 하위 그래디언트로 정의하고 `$\wv$`를 아래와 같이 정의하면 데이터포인트 `$i\in[1..n]$`를 균일하게 무작위로 고르고 `$\eqref{eq:regPrimal}$`의 스토캐스틱 하위 그래디언트를 계산한다.
`\[
f'_{\wv,i} := L'_{\wv,i} + \lambda\, R'_\wv \ ,
\]`
나아가서 `$R'_\wv$`는 `$R(\wv)$`, i.e. `$R'_\wv \in\frac{\partial}{\partial \wv} R(\wv)$`와 같은 정규화 공식 `$R(\wv)$`의 하위 그래디언트이다. `$R'_\wv$`은 데이터포인트 선택과 독립적이다.
`$i\in[1..n]$`에서의 무작위적 선택에서 명확하게 `$f'_{\wv,i}$`는 원래 목적 함수 `$f$`의 하위 그래디언트이고 `$\E\left[f'_{\wv,i}\right] \in\frac{\partial}{\partial \wv} f(\wv)$`이라는 의미가 된다.

SGD를 실행하는 것은 이제 단순히 음의 스토캐스틱 하위 그래디언트 `$f'_{\wv,i}$`의 방향으로 전진하는 것이 되었다.
`\begin{equation}\label{eq:SGDupdate}
\wv^{(t+1)} := \wv^{(t)}  - \gamma \; f'_{\wv,i} \ .
\end{equation}`
**스텝 사이즈.**
`$\gamma$` 파라미터는 스텝의 크기를 나타내는데, 기본 구현에서는 반복 횟수의 제곱근에 반비례하게 결정되고 `$t$`번째 반복에서는 `$s=$ stepSize`파라미터와 함께 `$\gamma := \frac{s}{\sqrt{t}}$`처럼 표현할 수 있다. SGD에서 최선의 스텝 사이즈를 선택하는 것은 대부분의 경우에 섬세한 작업이고 지금까지도 활발한 연구 주제다.


**그래디언트.**
`spark.mllib`에서 구현된 (하위) 그래디언트를 계산하는 머신러닝 기법은 <a href="mllib-classification-regression.html">분류 및 회귀</a> 섹션에서 확인할 수 있다.


**근위 업데이트.**
정규화의 하위 그라디언트 `$R'(\wv)$`를 스텝 방향으로 사용하는 대신 근위 연산을 사용하면 일부 경우에서 더 나은 업데이터 결과를 얻을 수 있다.
L1-정규화의 경우에 근위 연산은 [L1Updater](api/scala/org/apache/spark/mllib/optimization/L1Updater.html)에서 구현된 것처럼 약한 역치로서 주어진다.


### 분산 SGD에서의 스킴 업데이트
[GradientDescent](api/scala/org/apache/spark/mllib/optimization/GradientDescent.html)에서 구현된 SGD는 데이터 예제에 대한 단순한 (분산) 샘플링을 사용한다.
최적화 문제 `$\eqref{eq:regPrimal}$`의 손실 부분 `$\frac1n \sum_{i=1}^n L(\wv;\x_i,y_i)$`을 생각해보면 실제 (하위) 그래디언트는 `$\frac1n \sum_{i=1}^n L'_{\wv,i}$`이다.
SGD는 전체 데이터셋으로의 접근을 필요로하지만 `miniBatchFraction` 파라미터가 전체 데이터에서 사용할 데이터의 비율을 지정한다.
부분집합의 그래디언트의 평균을 스토캐스틱 그래디언트라고한다. `$S$`가 `$|S|=$ miniBatchFraction
$\cdot n$`의 크기만큼 샘플링된 부분집합이라고 하면 부분집합은 아래처럼 정의할 수 있다.
`\[
\frac1{|S|} \sum_{i\in S} L'_{\wv,i} \ ,
\]`

Spark 표준 동작에 의해서 각 반복 차수에서 분산 데이터셋 ([RDD](rdd-programming-guide.html#resilient-distributed-datasets-rdds))의 샘플링은 작업 머신(worker machine)에서 부분 결과의 합을 구하는 연산처럼 동작한다. 

데이터포인트의 비율인 `miniBatchFraction`가 1(기본값)으로 설정되었다면 각 반복 차수의 결과 도출 단계는 일반적인 (하위) 경사 하강법이다. 
극단적인 반대의 경우로 `miniBatchFraction` 값이 `$|S|=$ miniBatchFraction $\cdot n = 1$`처럼 한 개의 
데이터포인트만 샘플링 되도록 매우 작게 설정되었다면 알고리즘은 표준 SGD와 동일하다. 이 경우에는 전진 방향은 균일하게 
무작위로 샘플링된 데이터포인트에의해 결정된다.

### 메모리 제한 BFGS (L-BFGS)
[L-BFGS](http://en.wikipedia.org/wiki/Limited-memory_BFGS) 최적화 알고리즘은 `$\min_{\wv \in\R^d} \; f(\wv)$`형태의 최적화 문제를 풀기위한 유사뉴턴법의 일종이다. 
L-BFGS는 헤세 행렬을 만들기 위해 목적 함수의 이계도함수를 계산하지 않고 이차방정식의 형태로 목적 함수를 추정한다.
헤세 행렬은 이전의 그래디언트 평가에 의해 추정되어 뉴턴법으로 헤세 행렬을 계산할 때 
수직 확장성 문제(학습 형상(feature)의 개수)가 발생하지 않는다. 결과적으로 L-BFGS는 다른 1차 최적화에 비해 
빠른 수렴을 달성한다.

### 최적화 기법 선택
[선형 기법](mllib-linear-methods.html)은 내부적으로 최적화를 사용하고 `spark.mllib`의 몇 선형 기법들은 SGD와 L-BFGS를 모두 지원한다.
다른 최적화 기법들은 목적 함수의 특징에 따라 다르게 수렴을 보장하고 이 문서에서는 그에 대해 설명하지 않는다.
일반적으로 L-BFGS이 사용 가능할 때에는 L-BFGS의 속도가 더 빠르기때문에 (반복 횟수가 적기때문에) 
SGD 대신에 사용하는 것을 권장한다.

## MLlib에서의 구현

### 경사 하강법과 스토캐스틱 경사 하강법
스토캐스틱 경사 하강법을 포함한 경사 하강법들은 다양한 머신러닝 알고리즘 개발 이전에 저수준 
요소로서 `MLlib`에 포함된다. 예시는 <a href="mllib-linear-methods.html">선형 기법</a> 섹션에서 확인할 수 있다.

SGD class
[GradientDescent](api/scala/org/apache/spark/mllib/optimization/GradientDescent.html)
는 다음 파라미터를 사용한다:

* `Gradient` 는 최적화되는 함수의 스토캐스틱 그래디언트를 현재 파라미터 값과 
하나의 학습 예제에 대해 계산하는 클래스다. MLlib는 hinge, logistic, least-squares와 같은 
일반적인 손실 함수를 위한 그래디언트 클래스들을 포함한다. 그래디언트 클래스는 학습 예시, 
레이블 그리고 현재 파라미터 값을 입력으로써 받는다.
* `Updater` 는 각 반복에서 주어진 손실을 가지고 가중치를 업데이트하는 등 실질적으로
경사 하강을 수행하는 클래스다. 또한 updater는 정규화 부분에서 업데이트를 수행하기도 한다.
MLlib는 L1, L2 정규화 같은 정규화가 없는 경우를 위한 updater들을 포함한다.
* `stepSize` 는 경사 하강의 최초 스텝 사이즈를 지정하는 스칼라 값이다. MLlib의 모든 updater는
t번째 스텝사이즈로서 `stepSize $/ \sqrt{t}$`를 사용한다.
* `numIterations` 는 수행할 반복 횟수를 지정한다.
* `regParam` 은 L1 또는 L2 정규화를 사용할 때의 정규화 파라미터이다.
* `miniBatchFraction` 은 각 반복에서 그래디언트 방향을 계산하기 위해 전체 데이터 중 샘플링할
데이터의 비율이다.
  * 여전히 샘플링은 RDD 전체를 훑어야하기때문에 `miniBatchFraction`를 줄이는 것이 최적화 속도를 
  많이 향상시키지는 못할 것이다. 그래디언트를 계산하는 비용이 클 때에 사용자는 그래디언트 계산에 
  선택된 샘플만 사용할 때 가장 큰 속도 향상을 볼 수 있다.

### L-BFGS
L-BFGS는 현재는 저수준 최적화 구성요소로서만 `MLlib`에 포함된다. 선형 회귀나 로지스틱 회귀 같은 다양한 머신러닝 알고리즘에 L-BFGS를 사용하고싶다면 [LogisticRegressionWithSGD](api/scala/org/apache/spark/mllib/classification/LogisticRegressionWithSGD.html) 같은 학습 API를 사용하는 대신에 목적함수의 그래디언트와
업데이터를 옵티마이저에 직접 넘겨주어야한다.
예제는 아래에서 확인할 수 있다. 이는 다음 릴리즈에서 다뤄질 것이다.

[L1Updater](api/scala/org/apache/spark/mllib/optimization/L1Updater.html)를 사용한 L1 정규화는 약한 역치를 사용한 로직이 경사 하강법을 위해 디자인된 이후에는 동작하지 않는다.

L-BFGS 기법
[LBFGS.runLBFGS](api/scala/org/apache/spark/mllib/optimization/LBFGS.html)
는 다음 파라미터를 사용한다:

* `Gradient` 는 최적화되는 함수의 스토캐스틱 그래디언트를 현재 파라미터 값과 
하나의 학습 예제에 대해 계산하는 클래스다. MLlib는 hinge, logistic, least-squares와 같은 
일반적인 손실 함수를 위한 그래디언트 클래스들을 포함한다. 그래디언트 클래스는 학습 예시, 
레이블 그리고 현재 파라미터 값을 입력으로써 받는다.
* `Updater` 는 L-BFGS의 정규화 부분에서 목적 함수의 그래디언트와 손실값을 계산하는 클래스다.
MLlib는 L2 정규화에서와 마찬가지로 정규화가 없는 업데이터를 포함한다.
* `numCorrections` 는 L-BFGS 업데이트에서 사용되는 교정 횟수를 지정한다. 10을 권장한다.
* `maxNumIterations` 는 L-BFGS가 실행될 수 있는 최대 반복 횟수를 지정한다.
* `regParam` 은 L1 또는 L2 정규화를 사용할 때의 정규화 파라미터이다.
* `convergenceTol` 은 L-BFGS가 수렴하는 것으로 간주될 때 여전히 얼마나 많은 상대적 변화가
허용되는지를 제어하는 음이 아닌 실수값이다. 값이 작을수록 허용 오차가 적기 때문에 일반적으로
더 많이 반복한다. [Breeze LBFGS](https://github.com/scalanlp/breeze/blob/master/math/src/main/scala/breeze/optimize/LBFGS.scala)에서 이 값에 대해 평균 개선률과 그래디언트 정규화에 대해 기술한다.

`return`은 두 요소의 튜플이다. 첫 번째 요소는 모든 형상(feature)의 열행렬이고
두 번째 요소는 모든 반복에서 계산된 손실값의 배열이다.

다음은 L2 정규화와 L-BFGS 최적화로 학습한 이진 로지스틱 리그레션에 대한 예제이다.

<div class="codetabs">

<div data-lang="scala" markdown="1">
['LBFGS' 스칼라 문서](api/scala/org/apache/spark/mlib/optimization/LBFGS.html) 및 ['SquaredL2Updater' 스칼라 문서(api/scala/org/ml/ml/optimization/2SquaredDater)를 참조하십시오.

{% include_example scala/org/apache/spark/examples/mllib/LBFGSExample.scala %}
</div>

<div data-lang="java" markdown="1">
['LBFGS' Java 문서](api/java/org/apache/spark/mllib/optimization/LBFGS.html) 및 ['SquaredL2Updater' Java 문서](api/java/org/apache/mlib/optimization/SquaredDater)를 참조하십시오.

{% include_example java/org/apache/spark/examples/mllib/JavaLBFGSExample.java %}
</div>
</div>

## 개발자 노트

헤세 행렬은 이전의 그래디언트 평가에서 대략적으로 만들어지기 때문에 최적화 중에는 목적 함수를 
변경할 수 없다. 결과적으로 스토캐스틱 L-BFGS는 미니배치를 사용하는 것만으로 naive하게 동작하지 
않을 것이기 때문에 우리는 우리가 이에 대해 더 잘 이해할 때까지 이것을 제공하지 않는다.

`Updater`는 실제 경사 하강 스텝을 계산하도록 설계된 클래스이다. 그러나 적응형 단계 크기 재료와 
같은 그레이디언트에 대해서만 로직의 일부를 무시함으로써 L-BFGS에 대한 정규화의 목적 함수의 
그래디언트와 손실을 계산할 수 있다. 우리는 이것을 정규화와 단계 업데이트 사이의 로직을 구분하기 
위해 업데이트 프로그램을 대체하기 위해 정규화로 리팩터링할 것이다.
