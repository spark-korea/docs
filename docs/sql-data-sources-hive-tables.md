---
layout: global
title: Hive 테이블
displayTitle: Hive 테이블
---

* Table of contents
{:toc}

스파크 SQL은 Apache Hive에 저장된 데이터에 대한 읽기/쓰기를 지원합니다. Hive가 이미 많은 의존 라이브러리를 포함하고 있기때문에, 기본 스파크 배포판은 이 의존 라이브러리를 포함하고 있지 않습니다. Hive의 의존성 라이브러리를 classpath에서 찾을 수 있으면, 스파크는 이를 자동으로 로드합니다. 모든 작업 노드가 Hive에 저장된 데이터에 접근하기 위해 Hive 직렬화/역직렬화 라이브러리(SerDe) 그리고 Hive 의존 라이브러리는 모든 작업 노드에서 접근 가능해야 합니다.

Hive 관련 설정을 하기 위해서는 conf/ 안에 `hive-site.xml`, `core-site.xml`(보안 설정용)과 `hdfs-site.xml`(HDFS 설정용)파일을 넣어 주면 됩니다.

Hive를 사용할 때, SparkSession를 객체에 지속되는 Hive 메타스토어로의 연결성, Hive SerDe, Hive 사용자 정의 함수 등의 기능을 설정할 수 있습니다. Hive 배포판이 설치되어 있지 않더라도 Hive 지원을 활성화할 수 있습니다. `hive-site.xml`이 설정되어 있지 않은 경우, 현재 디렉토리에서 `metastore_db`를 자동으로 생성하고 `spark.sql.warehouse.dir`에 설정된 디렉토리를 생성합니다. `spark-warehouse`의 기본 디렉토리는 스파크 애플리케이션을 시작한 현재 디렉토리입니다. `hive-site.xml`의 `hive.metastore.warehouse.dir `속성은 스파크 2.0.0 버전부터 더 이상 지원되지 않으며, 대신 warehouse에서 데이터베이스의 기본 위치를 명시하려면 `spark.sql.warehouse.dir`을 사용해야 합니다. 스파크 애플리케이션을 실행하는 유저에게 쓰기 권한의 승인이 필요할 수 있습니다.

<div class="codetabs">

<div data-lang="scala"  markdown="1">
{% include_example spark_hive scala/org/apache/spark/examples/sql/hive/SparkHiveExample.scala %}
</div>

<div data-lang="python"  markdown="1">
{% include_example spark_hive python/sql/hive.py %}
</div>

</div>

### Hive 테이블의 저장 형식 지정하기

Hive 테이블을 생성할 때, 이 테이블이 어떻게 파일시스템에서/으로 데이터를 읽고/쓸지 정의해야 합니다. 다시 말해 "입력 형식"과 "출력 형식"을 정의해야 합니다. 또한, 이 테이블이 데이터를 로우로 역직렬화하거나 로우를 데이터로 직렬화하는 방식(serde)도 정의해야 합니다. 아래의 옵션("serde", "input format", "output format")을 사용하여 `CREATE TABLE src(id int) USING hive OPTIONS(fileFormat 'parquet') `와 같이 저장 형식을 명시할 수 있습니다. 기본적으로, 테이블 파일은 플레인 텍스트(plain text)로 읽어들입니다. 단, 테이블을 생성할 때 Hive의 스토리지 핸들러 기능은 아직 지원되지 않으므로, Hive에서 직접 저장소 핸들러를 사용하여 테이블을 생성하고 스파크 SQL에서 읽어오는 방법을 사용할 수 있습니다.

<table class="table">
  <tr><th>속성 이름</th><th>의미</th></tr>
  <tr>
    <td><code>fileFormat</code></td>
    <td>fileForamat은 "serde", "input format", "output format"등과 같은 저장 형식 명세의 한 종류입니다. 현재 6가지의 fileFormat을 지원합니다: 'sequencefile', 'rcfile', 'orc', 'parquet', 'textfile', 'avro'</td>
  </tr>
  <tr>
    <td><code>inputFormat, outputFormat</code></td>
    <td>이 두 옵션은 글자 그대로 사용할 `InputFormat`과 `OutputFormat`의 이름을 지정합니다(문자열 타입).예를 들면, `org.apache.hadoop.hive.ql.io.orc.OrcInputFormat`와 같습니다. 이 두 가지 옵션은 한 쌍으로 함께 사용하며, `fileForamt` 옵션을 이미 사용하였다면 이 옵션은 사용할 수 없습니다.</td>
  </tr>
  <tr>
    <td><code>serde</code></td>
    <td>seder 클래스의 이름을 명시합니다. `fileFormat` 옵션이 이미 명시되어 있고 여기에 serde에 대한 정보가 포함되어 있다면 이 옵션을 사용할 수 없습니다. 현재, 6가지의 fileFormat 옵션 중 "sequencefile", "textfile", "rcfile" 세 가지 옵션은 serde에 대한 정보를 포함하지 않으므로, fileFormat에서 이 세 가지 옵션을 사용하고 있을 때는 이 옵션을 사용할 수 있습니다.</td>
  </tr>
  <tr>
    <td><code>fieldDelim, escapeDelim, collectionDelim, mapkeyDelim, lineDelim</code></td>
    <td>fileFormat 옵션으로 "textfile"이 지정되어 있을 때만 사용가능합니다. 필드가 구분된 파일(delimited file)을 로우로 변환하는 방법을 정의합니다.</td>
  </tr>
</table>

`OPTIONS` 구문으로 정의되는 다른 모든 속성은 Hive serde 속성으로 간주됩니다.

### 서로 다른 버전의 Hive 메타스토어와 연동하기

스파크 SQL의 Hive 지원에서 가장 중요한 부분 중 하나는, 스파크 SQL이 Hive 테이블의 메타데이터에 접근할 수 있도록 하는 Hive 메타스토어와의 연동 기능입니다. 스파크 1.4.0 버전부터, 아래에 설명된 설정을 사용하면, 단일 스파크 SQL 빌드에서 서로 다른 버전의 Hive 메타스토어에 쿼리를 실행할 수 있습니다. 연동하는 메타스토어 Hive의 버전과는 별개로, 스파크 SQL은 Hive 1.2.1 버전을 기준으로 컴파일되며 이 버전에 포함된 클래스(serde, UDF, UDAF 등)를 내부적으로 사용합니다.

아래의 옵션을 사용하여 메타데이터를 받아올 때 사용되는 Hive 버전을 설정할 수 있습니다:


<table class="table">
  <tr><th>속성 이름</th><th>기본값</th><th>의미</th></tr>
  <tr>
    <td><code>spark.sql.hive.metastore.version</code></td>
    <td><code>1.2.1</code></td>
    <td>Hive 메타스토어의 버전. <code>0.12.0</code> 버전부터 <code>2.3.3</code> 버전까지 사용할 수 있습니다.</td>
  </tr>
  <tr>
    <td><code>spark.sql.hive.metastore.jars</code></td>
    <td><code>builtin</code></td>
    <td>
      Hive 메타스토어에 연결할 때 사용하는 HiveMetastoreClient 객체를 생성하는데 사용될 jar 파일의 위치. 다음 세 가지 옵션이 사용 가능합니다:
      <ol>
        <li><code>builtin</code></li>
        <code>-Phive</code>이 활성화되어 있을 때 스파크에 포함되어 있는 Hive 1.2.1을 사용합니다. 이 옵션을 사용하면 <code>spark.sql.hive.metastore.version</code>는 1.2.1이 되거나 정의되지 않아야 합니다.
        <li><code>maven</code></li>
        Maven 저장소에서 명시된 버전의 Hive jar를 다운로드하여 사용합니다. 이 설정을 운영 환경(production environment)에서 사용하는 것은 추천하지 않습니다.
        <li>JVM의 표준 형식 classpath. 이 classpath는 Hive와 올바른 버전의 Hadoop을 포함한 모든 의존 라이브러리를 포함해야 합니다. 이 jar 파일은 드라이버에서 접근 가능해야하며, yarn 클러스터 모드에서 실행하고자 한다면 애플케이션으로 패키지화되어 있어야 합니다.</li>
      </ol>
    </td>
  </tr>
  <tr>
    <td><code>spark.sql.hive.metastore.sharedPrefixes</code></td>
    <td><code>com.mysql.jdbc,<br/>org.postgresql,<br/>com.microsoft.sqlserver,<br/>oracle.jdbc</code></td>
    <td>
      <p>스파크 SQL과 (특정 버전의) Hive 사이에 공유되는 classloader를 사용하여 로드해야 하는 클래스들의 접두사 목록(쉼표로 구분). 예를 들면, Hive 메타스토어와 연결하는 데 사용되는 JDBC 드라이버 목록 같은 경우입니다. (역자 주: Hive의 메타스토어로는 MySQL, PostgreSQL 등의 데이터베이스를 사용할 수 있습니다. MySQL에 연결하려면 <code>com.mysql.jdbc</code> 패키지의 클래스가, PostgreSQL에 연결하려면 <code>org.postgresql</code> 패키지의 클래스를 사용해야 합니다. 각각의 경우 <code>com.mysql.jdbc</code>, <code>org.postgresql</code>가 지정되어야 합니다.) 이미 공유되고 있는 클래스와의 상호작용을 위해 필요한 클래스의 접두사들 역시 명시되어야 합니다. (예: log4j에서 사용하는 사용자 정의 Appender)
      </p>
    </td>
  </tr>
  <tr>
    <td><code>spark.sql.hive.metastore.barrierPrefixes</code></td>
    <td><code>(empty)</code></td>
    <td>
      <p>
        스파크 SQL이 붙는 Hive 각각의 버전에 따라 명시적으로 로드되어야 하는 클래스 접두사 목록(쉼표로 구분). 예를 들어 접두사를 공유하는 식으로 선언되는 게 보통인 Hive UDF가 여기에 포함됩니다. (예: <code>org.apache.spark.*</code>)
      </p>
    </td>
  </tr>
</table>
