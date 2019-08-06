docs
=====

Spark 공식 문서 한국어 번역입니다. 2019년 7월 현재 Spark 2.4.3 버전의 공식 문서가 번역되어 있습니다. ([commit c3e32bf](https://github.com/apache/spark/releases/tag/v2.4.3))

이 저장소에는 Spark 전체 프로젝트 파일 중 문서와 예제를 담는 부분, 그 중에서도 한국어 번역이 완료된 파일만을 저장합니다.

# 빌드하기

문서를 수정한 내역을 개발 환경에서 확인하려면 문서를 먼저 빌드해야 합니다. 이를 위해서는 시스템에 ruby 2.0과 python 그리고 몇몇 추가 패키지가 필요합니다.

먼저 ruby 2.0과 python을 설치한 뒤, 아래와 같이 추가 패키지를 설치합니다:

```sh
$ gem install jekyll jekyll-redirect-from pygments.rb
$ pip install Pygments
```

jekyll에 대해 자세한 내용은 아래 웹사이트를 참고하세요:

- https://jekyllrb.com/docs/installation/ (영어)
- https://jekyllrb-ko.github.io/docs/installation/ (한글)

\* 주의: ruby 1.9와 2.0이 동시에 설치되어 있는 시스템일 경우 gem을 2.0으로 교체하셔야 합니다.

지금부터 다음과 같이 문서를 빌드할 수 있습니다.

```sh
cd docs/
jekyll build # 문서 빌드
jekyll serve --watch # localhost:4000에 문서를 띄움
```

