---
layout: global
title: MLlib 선형 대수 가속 가이드
displayTitle: MLlib 선형 대수 가속 가이드
---

## 소개

해당 가이드는 Spark MLlib에 대한 가속 선형 대수 처리를 활성화하는 데 필요한 정보를 제공합니다.

Spark MLlib는 벡터 및 매트릭스를 머신러닝 알고리즘의 기본 데이터 타입으로 정의합니다. 그 위에 [BLAS](https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms) 및 [LAPACK](https://en.wikipedia.org/wiki/LAPACK) 연산은 [dev.ludovic.netlib](https://github.com/luhenry/netlib) 에서 구현 및 지원됩니다(알고리즘은 [Breeze](https://github.com/scalanlp/breeze) 를 호출할 수도 있습니다). `dev.ludovic.netlib`는 보다 빠른 수치 처리를 위해 최적화된 기본 선형 대수학 라이브러리(이하 "기본 라이브러리" 또는 "BLAS 라이브러리")를 사용할 수 있습니다. [Intel MKL](https://software.intel.com/content/www/us/en/develop/tools/math-kernel-library.html) 와 [OpenBLAS](http://www.openblas.net) 는 널리 사용되는 두 가지입니다.

공식 출시된 Spark binary에는 이러한 기본 라이브러리가 포함되어 있지 않습니다.

다음 섹션에서 기본 라이브러리를 설치하고 적절하게 구성하는 방법과 이러한 기본 라이브러리를 `dev.ludovic.netlib`에 지정하는 방법을 설명하겠습니다.

## 기본 선형 대수 라이브러리 설치

Intel MKL 및 OpenBLAS는 널리 사용되는 두 가지 기본 선형 대수 라이브러리입니다. 당신의 선호에 따라 하나를 선택할 수 있습니다. 아래와 같이 기본적인 안내를 드리겠습니다.

### Intel MKL

- Intel MKL을 다운로드하여 설치합니다. 클러스터의 모든 노드에서 설치가 진행되어야 합니다. 설치 위치는 $MKLROOT (e.g. /opt/intel/mkl) 라고 가정하겠습니다.
- 시스템 라이브러리 설치 경로에 특정 이름을 사용하여 `libmkl_rt.so`에 대한 소프트 링크를 생성합니다. 예를들어 `/usr/local/lib`가 시스템 라이브러리 검색 경로에 있는지 확인하고 다음 명령을 실행합니다.
```
$ ln -sf $MKLROOT/lib/intel64/libmkl_rt.so /usr/local/lib/libblas.so.3
$ ln -sf $MKLROOT/lib/intel64/libmkl_rt.so /usr/local/lib/liblapack.so.3
```

### OpenBLAS

클러스터의 모든 노드에서 설치가 진행되어야 합니다. OpenBLAS의 일반 버전은 대부분의 배포에서 사용할 수 있습니다. `apt` 혹은 `yum` 과 같은 배포 패키지 관리자를 사용하여 설치가 가능합니다.

Debian / Ubuntu 의 경우:
```
sudo apt-get install libopenblas-base
sudo update-alternatives --config libblas.so.3
```
CentOS / RHEL 의 경우:
```
sudo yum install openblas
```

## MLlib에 대해 기본 라이브러리가 활성화되어 있는지 확인

기본 라이브러리가 제대로 로드되어있는지 확인하기 위해 `spark-shell`을 시작하고 다음 코드를 실행하십시오.
```
scala> import dev.ludovic.netlib.NativeBLAS
scala> NativeBLAS.getInstance()
```

올바르게 로드된 경우 `dev.ludovic.netlib.NativeBLAS = dev.ludovic.netlib.blas.JNIBLAS@...`를 출력해야 합니다. 그렇지 않으면 경고가 출력되어야 합니다.
```
WARN NativeBLAS: Failed to load implementation from:dev.ludovic.netlib.blas.JNIBLAS
java.lang.RuntimeException: Unable to load native implementation
  at dev.ludovic.netlib.NativeBLAS.getInstance(NativeBLAS.java:44)
  ...
```

`dev.ludovic.netlib`가 특정 라이브러리 이름과 경로를 가리키도록 할 수도 있습니다. 예를 들어 Intel MKL의 경우 `-Ddev.ludovic.netlib.blas.nativeLib=libmkl_rt.so` 혹은 `-Ddev.ludovic.netlib.blas.nativeLibPath=$MKLROOT/lib/intel64/libmkl_rt.so`입니다. LAPACK과 ARPACK에 대해 유사한 파라미터가 있습니다. `-Ddev.ludovic.netlib.lapack.nativeLib=...`, `-Ddev.ludovic.netlib.lapack.nativeLibPath=...`, `-Ddev.ludovic.netlib.arpack.nativeLib=...`, 및 `-Ddev.ludovic.netlib.arpack.nativeLibPath=...`. 

시스템에서 기본 라이브러리가 올바르게 구성되지 않은 경우 Java 구현(JavaBLAS)이 대체 옵션으로 사용됩니다.

## Spark 구성

Intel MKL 또는 OpenBLAS에서 멀티 스레딩의 기본 동작은 Spark의 실행 모델[^1]에서 최적이 아닐 수 있습니다.

따라서 작업에 단일 스레드를 사용하도록 기본 라이브러리를 구성하면 실제로 성능이 향상될 수 있습니다. ([SPARK-21305](https://issues.apache.org/jira/browse/SPARK-21305) 참조) 기본적으로 `1`이고 일반적으로 `1`로 유지되는 `spark.task.cpus`의 수와 일치시키는 것이 일반적으로 최적입니다.

`config/spark-env.sh`의 옵션을 사용하여 Intel MKL 또는 OpenBLAS에 대한 스레드의 수를 설정할 수 있습니다.
* Intel MKL의 경우:
```
MKL_NUM_THREADS=1
```
* OpenBLAS의 경우:
```
OPENBLAS_NUM_THREADS=1
```

[^1]: BLAS 구현에 대한 스레드 수를 구성하는 방법을 이해하시려면 [Intel MKL](https://software.intel.com/en-us/articles/recommended-settings-for-calling-intel-mkl-routines-from-multi-threaded-applications) 또는 [Intel oneMKL](https://software.intel.com/en-us/onemkl-linux-developer-guide-improving-performance-with-threading) 및 [OpenBLAS](https://github.com/xianyi/OpenBLAS/wiki/faq#multi-threaded) 리소스를 참고하십시오. 
