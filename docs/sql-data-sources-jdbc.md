---
layout: global
title: JDBC To Other Databases
displayTitle: JDBC To Other Databases
---
# **JDBC를 통한 다른 데이터베이스 사용하기**

스파크 SQL은 JDBC를 이용하여 다른 데이터베이스에서 데이터를 읽을 수 있는 데이터 소스 역시 포함하고 있습니다. JdbcRDD를 사용하는 것보다 이 기능을 사용하는 것이 더 좋습니다. 결과 값이 DataFrame으로 반환되기 때문에, 이를 스파크 SQL에서 처리하거나 다른 데이터 소스에서 읽어들인 값과 결합(Join)해서 사용하기가 쉽기 때문입니다. JDBC 데이터 소스는 사용자가 ClassTag를 사용하지 않아도 되기 때문에 Java나 Python에서 사용하기 쉽습니다. (이는 다른 애플리케이션이 스파크 SQL을 이용하여 쿼리를 실행할 수 있게 해주는 스파크 SQL JDBC 서버와는 다릅니다).

시작에 앞서, 여러분의 데이터베이스에 맞는 JDBC 드라이버를 스파크 클래스 패스(classpath)에 포함시켜야 합니다. 예를 들어, 스파크 셸에서 postgres를 연결하려면 다음 명령을 실행하면 됩니다:


```
bin/spark-shell --driver-class-path postgresql-9.4.1207.jar --jars postgresql-9.4.1207.jar
```


원격 데이터베이스의 테이블은 데이터 소스 API를 사용하여 DataFrame 또는 스파크 SQL 임시 뷰(temporary view)로 불러올 수 있습니다. 사용자는 데이터 소스 옵션에서 JDBC 연결 속성을 지정할 수 있습니다. `user` 및 `password`는 일반적으로 데이터 소스에 로그인하기 위한 연결 등록 정보로 제공됩니다. 스파크는 연결 속성 외에도 대소문자를 구분하지 않는 다음 옵션을 지원합니다:


<table>
  <tr>
   <td><strong>속성 이름</strong>
   </td>
   <td><strong>의미</strong>
   </td>
  </tr>
  <tr>
   <td><code>url</code>
   </td>
   <td>연결할 JDBC URL입니다. 특정한 연결 속성은 URL에서 바로 지정 될 수 있습니다. \
예: \
<code>jdbc:postgresql://localhost/test?user=fred&password=secret</code>
   </td>
  </tr>
  <tr>
   <td><code>dbtable</code>
   </td>
   <td>읽거나 쓰기를 위한 JDBC 테이블. 읽기 경로에서 사용할 때 SQL 쿼리의 FROM 절에서 유효한 것은 모두 사용할 수 있습니다. 예를 들어, 전체 테이블 대신 괄호 안에 하위 쿼리를 사용할 수도 있습니다. 단, `dbtable`과`query` 옵션은 동시에 지정할 수 없습니다.
   </td>
  </tr>
  <tr>
   <td><code>query</code>
   </td>
   <td>스파크로 데이터를 읽어 들이는데 사용할 쿼리입니다. 지정된 쿼리는 괄호로 묶여 FROM 절의 하위 쿼리로 사용됩니다. 또한 스파크는 하위 쿼리 절에 별칭(alias)을 설정합니다. 예를 들어, 스파크는 다음 형식의 쿼리를 JDBC 소스로 보냅니다.
<p>
<code>SELECT <columns> FROM (<user_specified_query>) spark_gen_alias</code>
<p>
아래는 옵션 사용 시 몇 가지 제한 사항입니다.
<ol>

<li>`dbtable` 과 `query` 옵션을 동시에 지정할 수 없습니다.

<li>`query` 와 `partitionColumn` 옵션을 동시에 지정할 수 없습니다. `partitionColumn` 옵션을 지정해야 할 때는, `dbtable` 옵션을 사용하여 하위 쿼리를 지정할 수 있으며 `dbtable`의 일부로 제시된 하위 쿼리 별칭(alias)을 사용하여 파티션 컬럼을 지정할 수 있습니다. \
예: \
<code>spark.read.format("jdbc") \
&nbsp&nbsp .option("dbtable", "(select c1, c2 from t1) as subq") \
&nbsp&nbsp .option("partitionColumn", "subq.c1" \
&nbsp&nbsp .load()</code>
</li>
</ol>
   </td>
  </tr>
  <tr>
   <td><code>driver</code>
   </td>
   <td>URL에 연결할 때 사용하는 JDBC 드라이버의 클래스 이름.
   </td>
  </tr>
  <tr>
   <td><code>partitionColumn, lowerBound, upperBound</code>
   </td>
   <td>이 옵션 중 하나가 지정되면 다른 옵션 모두 지정되어야 합니다. 또한, <code>numPartitions</code> 도 지정되어야 합니다. 작업을 수행하는 여러 대의 호스트가 병렬로 읽을 때 테이블을 분할하는 법을 설정합니다. <code>partitionColumn</code>은 해당 테이블에서 숫자, 날짜, 타임스탬프 컬럼 중 하나여야 합니다. <code>lowerBound</code> 와 <code>upperBound</code> 는 테이블의 로우을 필터링하는데 사용되는 것이 아니라 파티션 의 분할 영역을 결정하는데 사용합니다. 그러므로 테이블의 모든 로우는 분할되어 반환될 것입니다. 이 옵션은 읽기에만 적용됩니다. 
   </td>
  </tr>
  <tr>
   <td><code>numPartitions</code>
   </td>
   <td>테이블의 읽기/쓰기를 병렬로 수행할 수 있는  파티션의 최대 개수입니다. 이 수는 동시에 발생하는 JDBC 연결의 최대 개수를 정합니다. 만약 쓰기용 파티션의 개수가 이 제한을 초과한다면 쓰기를 실행하기 전에 <code>coalesce(numPartitions)</code>를 호출하여 외부 데이터베이스에 대한 연결 개수를 지정된 값까지 줄입니다.
   </td>
  </tr>
  <tr>
   <td><code>queryTimeout</code>
   </td>
   <td>드라이버가 명령문(Statement) 객체의 실행을 위해 기다리는 시간(초)입니다. 0은 제한이 없음을 의미합니다. 쓰기 작업을 수행할 때, 이 옵션은 JDBC 드라이버가 API <code>setQueryTimeout</code>를 어떻게 구현했는지에 따라 다르게 동작합니다. 예를 들어 h2 JDBC 드라이버는 전체 JDBC 배치(batch) 대신 각 쿼리의 타임 아웃을 체크합니다. 기본값은 0입니다.
   </td>
  </tr>
  <tr>
   <td><code>fetchsize</code>
   </td>
   <td>한번에 가져올 로우의 수를 결정하는 JDBC 페치(fetch) 크기입니다. 이를 이용해 기본 페치 크기가 작은 JCBC 드라이버(예. Oracle은 10로우)의 성능을 향상할 수 있습니다. 이 옵션은 읽기에만 적용됩니다.
   </td>
  </tr>
  <tr>
   <td><code>batchsize</code>
   </td>
   <td>한번에 삽입할 수 있는 로우의 수를 결정하는 JDBC 배치(batch) 크기입니다. 이를 이용해  JDBC 드라이버의 성능을 향상할 수 있습니다. 이 옵션은 쓰기에만 적용됩니다. 기본값은 <code>1000입니다</code>.
   </td>
  </tr>
  <tr>
   <td><code>isolationLevel</code>
   </td>
   <td>현재 연결에 적용되는 트랜잭션 격리 수준입니다. JDBC의 연결 객체에 의해 정의된 표준 트랜잭션 격리 수준에 따라 <code>NONE</code>, <code>READ_COMMITTED</code>, <code>READ_UNCOMMITTED</code>, <code>REPEATABLE_READ</code>, 또는 <code>SERIALIZABLE</code> 중에 하나로 설정될 수 있으며 기본값은 <code>READ_UNCOMMITTED</code>입니다. 이 옵션은 쓰기에만 적용됩니다. 자세한 내용은 <code>java.sql.Connection</code>의 문서를 참조하세요.
   </td>
  </tr>
  <tr>
   <td><code>sessionInitStatement</code>
   </td>
   <td>이 옵션은 원격 데이터베이스에 대한 세션이 열린 뒤, 읽기 작업을 수행하기 전에 실행되는 SQL 명령문 (또는 PL/SQL 블록)을 지정합니다. 이를 이용하여 세션 초기화 코드를 실행하세요. 예: <code>option("sessionInitStatement", """BEGIN execute immediate 'alter session set "_serial_direct_read"=true'; END;""")</code>
   </td>
  </tr>
  <tr>
   <td><code>truncate</code>
   </td>
   <td>JDBC writer와 관련된 옵션입니다. <code>SaveMode.Overwrite</code>가 활성화 된 상태일 때, 이 옵션은 스파크가 기존 테이블을 삭제(drop)하고 재생성(create)하는 대신에 포함된 레코드만 전부 삭제(truncate)하도록 합니다. 이는 더 효율적일 수 있으며 테이블 메타데이터 (예: 인덱스)가 제거되는 것을 방지합니다. 그러나 새로운 데이터가 다른 스키마를 가질 때와 같은 경우에서는 동작하지 않습니다. 기본값은 <code>false</code>입니다. 이 옵션은 쓰기에만 적용됩니다.
   </td>
  </tr>
  <tr>
   <td><code>cascadeTruncate</code>
   </td>
   <td>JDBC writer와 관련된 옵션입니다. JDBC 데이터베이스(여기서는 PostgreSQL과 Oracle)에서 해당 기능이 지원되고 또 해당 기능이 사용 가능하도록 켜져 있을 경우, 이 옵션은 <code>TRUNCATE TABLE t CASCADE</code> 을 실행하게 합니다 (PostgreSQL의 경우 <code>TRUNCATE TABLE ONLY t CASCADE</code> 는 실수로 자손(descendant) 테이블을 삭제(truncate)하는 것을 막기 위해서 실행됩니다). 이 옵션은 다른 테이블에 영향을 주기 때문에 주의해서 사용해야 합니다. 이 옵션은 쓰기에만 적용됩니다. 기본값은 해당 JDBC 데이터베이스의 기본 cascading truncate 동작이며 각 JDBCDialect의 <code>isCascadeTruncate</code>에서 지정되어 있습니다.
   </td>
  </tr>
  <tr>
   <td><code>createTableOptions</code>
   </td>
   <td>JDBC writer와 관련된 옵션입니다. 이 옵션을 지정하면 테이블을 만들 때 특정 데이터베이스의 테이블과 파티션 옵션을 설정할 수 있습니다. (예. <code>CREATE TABLE t (name string) ENGINE=InnoDB.</code>). 이 옵션은 쓰기에만 적용됩니다.
   </td>
  </tr>
  <tr>
   <td><code>createTableColumnTypes</code>
   </td>
   <td>테이블을 만들 때 기본값 대신에 사용하는 데이터베이스 컬럼 데이터 타입입니다. 데이터 타입 정보는 CREATE TABLE 컬럼 구문와 같은 형식 (예: <code>"name CHAR(64), comments VARCHAR(1024)")</code>으로 지정되어야 합니다. 지정된 타입은 유효한 스파크 sql 데이터 타입이어야 합니다. 이 옵션은 쓰기에만 적용됩니다.
   </td>
  </tr>
  <tr>
   <td><code>customSchema</code>
   </td>
   <td>JDBC 커넥터에서 데이터를 읽는 데 사용하는 사용자 정의 스키마입니다. 예: <code>"id DECIMAL(38, 0), name STRING"</code>. 일부 필드만 지정하고 다른 필드는 기본 타입 맵핑을 사용할 수 있습니다. 예: <code>"id DECIMAL(38, 0)"</code>. 컬럼 이름은 JDBC 테이블의 해당 컬럼 이름과 동일해야 합니다. 이 기능을 사용하면 기본 매핑으로 결정되는 Spark SQL 타입이 아닌 사용자가 지정한 타입을 사용할 수 있습니다. 이 옵션은 읽기에만 적용됩니다.
   </td>
  </tr>
  <tr>
   <td><code>pushDownPredicate</code>
   </td>
   <td>조건절을 JDBC 데이터 소스로 푸시다운(push-down)하는 것을 활성화 또는 비활성화하는 옵션입니다. 기본값은 true이며, 이 경우 스파크는 JDBC 데이터 소스로 가능한 많은 필터를 푸쉬 다운할 것입니다. 값이 false로 설정된다면, JDBC 데이터 소스에 푸시다운하는 필터가 없을 것이며 스파크가 모든 필터를 처리할 것입니다. 조건절 필터링이 JDBC 데이터 소스로 실행할 때보다 스파크로 실행할 때 더 빠르다면 Predicate push-down 옵션은 보통 꺼져있습니다. 
   </td>
  </tr>
</table>




*   **Scala**


```
// 주의: JDBC 불러오기와 저장하기는 load/save나 jdbc 메소드로 할 수 있습니다
// JDBC 소스에서 데이터 불러오기
val jdbcDF = spark.read
  .format("jdbc")
  .option("url", "jdbc:postgresql:dbserver")
  .option("dbtable", "schema.tablename")
  .option("user", "username")
  .option("password", "password")
  .load()

val connectionProperties = new Properties()
connectionProperties.put("user", "username")
connectionProperties.put("password", "password")
val jdbcDF2 = spark.read
  .jdbc("jdbc:postgresql:dbserver", "schema.tablename", connectionProperties)
// 읽기 스키마의 사용자 지정 데이터 유형 지정하기
connectionProperties.put("customSchema", "id DECIMAL(38, 0), name STRING")
val jdbcDF3 = spark.read
  .jdbc("jdbc:postgresql:dbserver", "schema.tablename", connectionProperties)

// JDBC 소스로 데이터 저장하기
jdbcDF.write
  .format("jdbc")
  .option("url", "jdbc:postgresql:dbserver")
  .option("dbtable", "schema.tablename")
  .option("user", "username")
  .option("password", "password")
  .save()

jdbcDF2.write
  .jdbc("jdbc:postgresql:dbserver", "schema.tablename", connectionProperties)

// 쓰기의 테이블 생성시 컬럼 데이터 유형 지정하기
jdbcDF.write
  .option("createTableColumnTypes", "name CHAR(64), comments VARCHAR(1024)")
  .jdbc("jdbc:postgresql:dbserver", "schema.tablename", connectionProperties)
```


스파크 저장소의 "examples/src/main/scala/org/apache/spark/examples/sql/SQLDataSourceExample.scala"에서 전체 예제 코드를 찾아보세요.



*   **Python**


```
# 주의: JDBC 불러오기와 저장하기는 load/save나 jdbc 메소드로 할 수 있습니다
# JDBC 소스에서 데이터 불러오기
jdbcDF = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql:dbserver") \
    .option("dbtable", "schema.tablename") \
    .option("user", "username") \
    .option("password", "password") \
    .load()

jdbcDF2 = spark.read \
    .jdbc("jdbc:postgresql:dbserver", "schema.tablename",
          properties={"user": "username", "password": "password"})

# 읽기 DataFrame의 컬럼 데이터 유형 지정하기
jdbcDF3 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql:dbserver") \
    .option("dbtable", "schema.tablename") \
    .option("user", "username") \
    .option("password", "password") \
    .option("customSchema", "id DECIMAL(38, 0), name STRING") \
    .load()

# JDBC 소스로 데이터 저장하기
jdbcDF.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql:dbserver") \
    .option("dbtable", "schema.tablename") \
    .option("user", "username") \
    .option("password", "password") \
    .save()

jdbcDF2.write \
    .jdbc("jdbc:postgresql:dbserver", "schema.tablename",
          properties={"user": "username", "password": "password"})

# 쓰기의 테이블 생성시 컬럼 데이터 유형 지정하기
jdbcDF.write \
    .option("createTableColumnTypes", "name CHAR(64), comments VARCHAR(1024)") \
    .jdbc("jdbc:postgresql:dbserver", "schema.tablename",
          properties={"user": "username", "password": "password"})
```


스파크 저장소의  "examples/src/main/python/sql/datasource.py"에서 전체 예제 코드를 찾아보세요.