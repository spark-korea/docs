---
layout: global
title: Troubleshooting
displayTitle: Troubleshooting
---

# **문제 해결**



*   JDBC 드라이버 클래스는 클라이언트 세션과 모든 익스큐터(executor)에서 사용되는 초기 클래스 로더(Primordial ClassLoader, JVM 초기화시 처음으로 설정되는 클래스 로더)에서 접근할 수 있어야 합니다. 그 이유는 JDBC 연결을 생성할 때 Java의 DriverManager 클래스가 보안 체크를 수행하면서 초기 클래스 로더가 접근할 수 없는 모든 드라이버를 무시해버리기 때문입니다. 이 문제를 해결하는 간편한 방법으로는 모든 worker 노드에서 compute_classpath.sh가 사용하려는 JDBC 드라이버의 JAR 파일을 포함하도록 수정하는 방법이 있습니다.
*   H2와 같은 특정 데이터베이스는 모든 이름을 대문자로 변환합니다. 스파크 SQL에서 이러한 이름을 참조하려면 대문자를 써야 합니다. 
*   사용자는 특별한 처리가 필요한 경우, 데이터 소스 옵션에서 벤더별 특정 JDBC 연결 속성을 지정할 수 있습니다. 예를 들어, `spark.read.format("jdbc").option("url", oracleJdbcUrl).option("oracle.jdbc.mapDateToTimestamp", "false")`. `oracle.jdbc.mapDateToTimestamp` 의 기본값은 true이지만 사용자는 Oracle의 date가 timestamp로 정해지지 않도록 이 flag를 비활성화해야 하는 경우도 있습니다.