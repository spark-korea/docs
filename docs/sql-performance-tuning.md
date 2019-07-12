---
layout: global
title: Performance Tuning
displayTitle: Performance Tuning
---
# **성능 튜닝**



*  [메모리에 데이터 캐싱하기](#heading=h.e8fg10my1tk0)
*  [다른 설정 옵션](#heading=h.sozkz6n81w0)
*   [SQL 쿼리를 위한 Broadcast 힌트](#heading=h.j9vv7j9d4oqa)

작업 부하가 있는 경우 메모리에 데이터를 캐싱하거나 일부 실험적인 옵션을 켜서 성능을 향상시킬 수 있습니다. 


## **메모리에 데이터 캐싱하기**

스파크 SQL은 `spark.catalog.cacheTable("tableName")` 이나 `dataFrame.cache()`호출을 통해 인메모리 컬럼 형식으로 테이블을 캐시할 수 있습니다. 스파크 SQL은 필수 컬럼만 스캔하며 메모리 사용과 GC 영향을 최소화하기 위해 자동으로 압축을 조정합니다. `spark.catalog.uncacheTable("tableName")`을 호출하여 메모리에서 테이블을 제거할 수 있습니다.

`SparkSession`에서 `setConf` 메소드를 사용하거나 SQL에서 `SET key=value를 `실행하여 인메모리 캐싱을 설정할 수 있습니다.


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
   <td><code>spark.sql.inMemoryColumnarStorage.compressed</code>
   </td>
   <td>true
   </td>
   <td>true로 설정 시 스파크 SQL은 데이터에 대한 통계를 기반으로 각 컬럼마다 압축 코덱을 자동으로 선택합니다.
   </td>
  </tr>
  <tr>
   <td><code>spark.sql.inMemoryColumnarStorage.batchSize</code>
   </td>
   <td>10000
   </td>
   <td>컬럼 기반 캐싱의 배치 사이즈를 조절합니다. 더 큰 배치 사이즈는 메모리 활용성과 압축률을 개선시킬 수 있으나 데이터를 캐시할 때 메모리 부족(Out Of Memory)이 발생할 위험이 있습니다. 
   </td>
  </tr>
</table>



## **기타 설정 옵션**

쿼리 실행의 성능을 조정하기 위해 다음 옵션을 사용할 수 있습니다. 향후 버전에서는 더 많은 최적화가 자동으로 수행될 것이므로 이 옵션들은 더 이상 사용되지 않을 수 있습니다.


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
   <td><code>spark.sql.files.maxPartitionBytes</code>
   </td>
   <td>134217728 (128 MB)
   </td>
   <td>파일을 읽을 때 파티션 하나에 들어갈 최대 바이트 수.
   </td>
  </tr>
  <tr>
   <td><code>spark.sql.files.openCostInBytes</code>
   </td>
   <td>4194304 (4 MB)
   </td>
   <td>파일을 열 때 계산되는 비용인 바이트 수를 동시에 스캔할 수 있습니다. 파티션 하나에 여러 파일을 넣을 때 사용됩니다. 더 크게 측정될 수록 더 좋으며, 작은 파일들로 구성된 파티션이 큰 파일(먼저 처리가 예정된 파일)로 구성된 파티션보다 더 빠를 것입니다. 
   </td>
  </tr>
  <tr>
   <td><code>spark.sql.broadcastTimeout</code>
   </td>
   <td>300
   </td>
   <td>브로드캐스트조인에서 브로드캐스트대기 시간의 타임 아웃 초.
   </td>
  </tr>
  <tr>
   <td><code>spark.sql.autoBroadcastJoinThreshold</code>
   </td>
   <td>10485760 (10 MB)
   </td>
   <td>조인을 수행 시, 모든 작업 노드에 브로드캐스트될 테이블의  최대 바이트 사이즈를 설정합니다. 이 값을 -1로 설정하면 브로드캐스팅이 비활성화 됩니다. 현재, 통계는 명령어 <code>ANALYZE TABLE <tableName> COMPUTE STATISTICS noscan </code>가 적용된 Hive 메타스토어 테이블에서만 지원됩니다. 
   </td>
  </tr>
  <tr>
   <td><code>spark.sql.shuffle.partitions</code>
   </td>
   <td>200
   </td>
   <td>조인이나 집계를 위해 데이터를 셔플링(shuffling)할 때 사용될 파티션 수를 설정합니다. 
   </td>
  </tr>
</table>



## **SQL 쿼리를 위한 브로드캐스트 힌트**

`BROADCAST `힌트는 각 지정된 테이블을 다른 테이블이나 뷰와 조인할 때 스파크가 해당 테이블을 브로드캐스트하도록 안내합니다. 스파크가 조인 연산을 수행할 구체적인 방법을 정할 때 통계값이 `spark.sql.autoBroadcastJoinThreshold `설정값보다 크더라도 브로드캐스트 해시 조인(BHJ)이 더 선호됩니다. 조인할 두 테이블이 지정되었을 때 스파크는 통계값이 더 적은 쪽을 브로드캐스트합니다. 모든 케이스 (예. full outer join)가 BHJ를 지원하지는 않기 때문에 스파크가 BHJ 선택을 항상 보장하지는 않습니다. 중첩 루프 조인(nested loop join)이 선택될 때도 힌트를 참고합니다.



*   **Scala**


```
import org.apache.spark.sql.functions.broadcast
broadcast(spark.table("src")).join(spark.table("records"), "key").show()

```



*   **Python**


```
from pyspark.sql.functions import broadcast
broadcast(spark.table("src")).join(spark.table("records"), "key").show()