---
layout: global
title: PMML 모델 출력 - RDD 기반 API
displayTitle: PMML 모델 출력 - RDD 기반 API
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

## spark.mllib 지원 모델

`spark.mllib`는 Predictive Model Markup Language ([PMML](http://en.wikipedia.org/wiki/Predictive_Model_Markup_Language))로의 모델 출력을 지원한다.

아래 표는 PMML로 출력할 수 있는 `spark.mllib` 모델과 그에 대응되는 PMML 모델을 나열한다. 

<table class="table">
  <thead>
    <tr><th>spark.mllib 모델</th><th>PMML 모델</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>KMeansModel</td><td>ClusteringModel</td>
    </tr>    
    <tr>
      <td>LinearRegressionModel</td><td>RegressionModel (functionName="regression")</td>
    </tr>
    <tr>
      <td>RidgeRegressionModel</td><td>RegressionModel (functionName="regression")</td>
    </tr>
    <tr>
      <td>LassoModel</td><td>RegressionModel (functionName="regression")</td>
    </tr>
    <tr>
      <td>SVMModel</td><td>RegressionModel (functionName="classification" normalizationMethod="none")</td>
    </tr>
    <tr>
      <td>Binary LogisticRegressionModel</td><td>RegressionModel (functionName="classification" normalizationMethod="logit")</td>
    </tr>
  </tbody>
</table>

## 예제
<div class="codetabs">

<div data-lang="scala" markdown="1">
위 표에 있는 출력할 수 있는 모델을 PMML로 출력하는 것을 `model.toPMML` 이라고 부른다.

PMML 모델을 문자열('model.toPMML')로 출력할 뿐만 아니라 PMML 모델을 다른 형식으로 출력할 수도 있다.

API에 대한 자세한 내용은 ['KMeans' Scala docs](api/scala/org/apache/spark/mllib/clustering/KMeans.html) 및 [Vectors` Scala docs](api/scala/org/apache/spark/mllib/linalg/Vectors$.html)를 참조하십시오.

다음은 KMeansModel을 빌드하고 PMML 형식으로 출력하는 예제이다.
{% include_example scala/org/apache/spark/examples/mllib/PMMLModelExportExample.scala %}

지원되지 않은 모델의 경우에는 `.toPMML` 메서드를 찾을 수 없거나 `IllegalArgumentException` 예외가 throw 될 것이다.

</div>

</div>
