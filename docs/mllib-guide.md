---
layout: global
title: "MLlib: RDD 기반 API"
displayTitle: "MLlib: RDD 기반 API"
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

본 섹션은 RDD 기반의 API에 대한 MLlib(`spark.mllib` 패키지)의 사용 가이드입니다.
현재 MLlib의 주요 API인 DataFrame 기반의 API(`spark.ml` 패키지)에 대한 문서는 [MLlib Main Guide](ml-guide.html)를 확인해주세요.

* [데이터 타입/Data types](mllib-data-types.html)
* [통계 기본/Basic statistics](mllib-statistics.html)
  * [통계 요약/summary statistics](mllib-statistics.html#summary-statistics)
  * [상관관계/correlation](mllib-statistics.html#correlations)
  * [계층 샘플링/stratified sampling](mllib-statistics.html#stratified-sampling)
  * [이론 검증/hypothesis testing](mllib-statistics.html#hypothesis-testing)
  * [스트리밍 밀도 검증/streaming significance testing](mllib-statistics.html#streaming-significance-testing)
  * [무작위 데이터 생성/random data generation](mllib-statistics.html#random-data-generation)
* [분류와 회귀/Classification and regression](mllib-classification-regression.html)
  * [선형 모델/linear models (SVMs, 로지스틱 회귀/logistic regression, 선형 회귀/linear regression)](mllib-linear-methods.html)
  * [나이브 베이즈/naive Bayes](mllib-naive-bayes.html)
  * [의사결정 트리/decision trees](mllib-decision-tree.html)
  * [트리 구조의 앙상블/ensembles of trees (랜덤 포레스트와 그래디언트-부스트 트리)](mllib-ensembles.html)
  * [등회귀/isotonic regression](mllib-isotonic-regression.html)
* [협엽 필터링/Collaborative filtering](mllib-collaborative-filtering.html)
  * [alternating least squares (ALS)](mllib-collaborative-filtering.html#collaborative-filtering)
* [군집화/Clustering](mllib-clustering.html)
  * [k-평균/k-means](mllib-clustering.html#k-means)
  * [가우시안 혼합/Gaussian mixture](mllib-clustering.html#gaussian-mixture)
  * [거듭제곱 반복 군집화/power iteration clustering (PIC)](mllib-clustering.html#power-iteration-clustering-pic)
  * [잠재 디리클레 할당/latent Dirichlet allocation (LDA)](mllib-clustering.html#latent-dirichlet-allocation-lda)
  * [이등분 k-평균/bisecting k-means](mllib-clustering.html#bisecting-kmeans)
  * [스트리밍 k-평균/streaming k-means](mllib-clustering.html#streaming-k-means)
* [차원 축소/Dimensionality reduction](mllib-dimensionality-reduction.html)
  * [특잇값 분해/singular value decomposition (SVD)](mllib-dimensionality-reduction.html#singular-value-decomposition-svd)
  * [주성분 분석/principal component analysis (PCA)](mllib-dimensionality-reduction.html#principal-component-analysis-pca)
* [형상 추출 및 변환/Feature extraction and transformation](mllib-feature-extraction.html)
* [빈발 패턴 마이닝/Frequent pattern mining](mllib-frequent-pattern-mining.html)
  * [빈발 패턴 성장/FP-growth](mllib-frequent-pattern-mining.html#fp-growth)
  * [연관 규칙/association rules](mllib-frequent-pattern-mining.html#association-rules)
  * [PrefixSpan](mllib-frequent-pattern-mining.html#prefix-span)
* [평가 지표/Evaluation metrics](mllib-evaluation-metrics.html)
* [PMML 모델 내보내기/PMML model export](mllib-pmml-model-export.html)
* [최적화/Optimization (developer)](mllib-optimization.html)
  * [스토캐스틱 경사하강법/stochastic gradient descent](mllib-optimization.html#stochastic-gradient-descent-sgd)
  * [메모리 제한 BFGS/limited-memory BFGS (L-BFGS)](mllib-optimization.html#limited-memory-bfgs-l-bfgs)

