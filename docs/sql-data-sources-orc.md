---
layout: global
title: ORC Files
displayTitle: ORC Files
---

# **ORC 파일**

스파크 2.3 버전부터 스파크는 새로운 ORC 파일 포맷과 함께 벡터화된 ORC 읽기 기능을 지원합니다. 이 기능을 위해 아래의 설정이 새로 추가되었습니다. `spark.sql.orc.impl`이 `native` 로 설정되어 있고 `spark.sql.orc.enableVectorizedReader`이 `true로` 설정된 경우, 네이티브 ORC 테이블(즉, 사용자가 `USING ORC`를 사용하여 생성한 테이블)에서 벡터화된 리더를 사용할 수 있습니다. Hive ORC SerDe 테이블(즉, 사용자가 `USING HIVE OPTIONS (fileFormat 'ORC')`를 사용하여 생성한 테이블)에서는  `spark.sql.hive.convertMetastoreOrc`을 `true`로 설정하였을 때 벡터화된 리더를 사용할 수 있습니다.


<table>
  <tr>
   <td><strong>속성 이름</strong>
   </td>
   <td><strong>기본값</strong>
   </td>
   <td><strong>의미</strong>
   </td>
  </tr>
  <tr>
   <td><code>spark.sql.orc.impl</code>
   </td>
   <td><code>native</code>
   </td>
   <td>사용할 ORC 구현체 이름. <code>native</code> 또는 <code>hive</code>를 사용할 수 있습니다.  <code>native</code>는 아파치 ORC 1.4에 내장된 네이티브 ORC를 의미하며 <code>hive</code>는 Hive 1.2.1의 ORC 라이브러리를 의미합니다.
   </td>
  </tr>
  <tr>
   <td><code>spark.sql.orc.enableVectorizedReader</code>
   </td>
   <td><code>true</code>
   </td>
   <td><code>native</code> 구현체에서 벡터화된 ORC 읽기 기능을 활성화합니다.  <code>false</code>인 경우, 벡터화되지 않은 ORC 리더를 사용합니다. <code>hive </code>구현체에는 적용되지 않습니다.
   </td>
  </tr>
</table>