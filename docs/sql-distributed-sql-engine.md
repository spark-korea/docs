---
layout: global
title: Distributed SQL Engine
displayTitle: Distributed SQL Engine
---

# **분산 SQL 엔진**



*  [Thrift JDBC/ODBC 서버 실행](#heading=h.3wyu8rtlpti6)
*  [ SQL CLI 실행](#heading=h.6a0gm3dsg4f8)


스파크 SQL은 JDBC/ODBC나 커맨드 라인 인터페이스를 사용하여 분산 쿼리 엔진처럼 사용할 수도 있습니다. 이 모드를 사용하면 사용자 혹은 독립 애플리케이션은 SQL 쿼리를 실행하는 코드를 작성할 필요 없이 스파크 SQL과 직접 상호작용 할 수 있습니다.


## **Thrift JDBC/ODBC 서버 실행**

여기서 구현된 Thrift JDBC/ODBC 서버는 Hive 1.2.1의 `HiveServer2`에 해당합니다. 스파크나 Hive 1.2.1과 함께 제공되는 beeline 스크립트로 JDBC 서버를 테스트해 볼 수 있습니다. 

JDBC/ODBC 서버를 시작하기 위해 스파크 디렉토리에 있는 다음 스크립트를 실행해보세요:


```
./sbin/start-thriftserver.s
```


이 스크립트는 모든 `bin/spark-submit `커맨드 라인 옵션과 Hive 속성을 지정하는 `--hiveconf `옵션을 허용합니다. `./sbin/start-thriftserver.sh --help` 를 실행해 사용 가능한 옵션의 전체 리스트를 볼 수 있습니다. 기본적으로, 서버는 localhost:10000에서 연결이 들어오 기다립니다. 이를 수정하기 위해, 다음과 같이 환경 변수를 이용할 수 있으며:


```
export HIVE_SERVER2_THRIFT_PORT=<listening-port>
export HIVE_SERVER2_THRIFT_BIND_HOST=<listening-host>
./sbin/start-thriftserver.sh \
  --master <master-uri> \
  ...
```


또는 시스템 속성을 수정할 수도 있습니다:


```
./sbin/start-thriftserver.sh \
  --hiveconf hive.server2.thrift.port=<listening-port> \
  --hiveconf hive.server2.thrift.bind.host=<listening-host> \
  --master <master-uri>
  ...
```


이제 beeline을 이용해 Thrift JDBC/ODBC 서버를 테스트해 볼 수 있습니다:


```
./bin/beeline
```


beeline에서 JDBC/ODBC 서버에 연결하세요:


```
beeline> !connect jdbc:hive2://localhost:10000
```


Beeline이 사용자 이름과 패스워드를 물을 것입니다. 비보안 모드(non-secure mode)에서는 사용자 이름만 입력하고 패스워드는 빈칸을 입력하면 됩니다. 보안 모드에서는 [beeline 문서](https://cwiki.apache.org/confluence/display/Hive/HiveServer2+Clients)의 지시 사항을 따르세요. 

`hive-site.xml`, `core-site.xml`과 `hdfs-site.xml`파일을 `conf/`에 넣어 Hive를 설정합니다.

Hive와 함께 제공되는 beeline 스크립트도 사용할 수 있습니다. 

Thrift JDBC 서버는 HTTP 전송을 통해 thrift RPC 메시지를 보내는 기능도 지원합니다. 다음 설정을 사용하여 HTTP 모드를 시스템 속성으로 활성화하거나 `conf/`: 의 `hive-site.xml`에서 활성화합니다. 


```
hive.server2.transport.mode - 이 값을 http 로 설정합니다.
hive.server2.thrift.http.port - 수신할 HTTP 포트 숫자; 기본값은 10001.
hive.server2.http.endpoint - HTTP 엔드포인트; 기본값은 cliservice.
```


beeline을 사용해 http 모드에서의 JDBC/ODBC 서버 연결을 테스트해 보세요:


```
beeline> !connect jdbc:hive2://<host>:<port>/<database>?hive.server2.transport.mode=http;hive.server2.thrift.http.path=<http_endpoint>
```



## **스파크 SQL CLI 실행**

스파크 SQL CLI은 로컬 모드에서 Hive metastore 서비스를 실행하고 커맨드 라인에서 쿼리 입력을 실행하는 편리한 도구입니다. 스파크 SQL CLI는 Thrift JDBC 서버와 통신할 수 없습니다.

스파크 SQL CLI을 시작하기위해, Spark 디렉토리에서 다음 명령어를 실행하세요:


```
./bin/spark-sql
```


`hive-site.xml`, `core-site.xml`과 `hdfs-site.xml` 파일을 `conf/`에 넣어 Hive를 설정합니다. `./bin/spark-sql --help` 를 실행해 사용 가능한 옵션의 전체 리스트를 볼 수 있습니다. 
