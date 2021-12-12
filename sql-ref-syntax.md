---
layout: global
title: SQL 구문
displayTitle: SQL 구문

---

Spark SQL은 Apache Spark의 구조화된 데이터 작업 모듈입니다. 
SQL 구문 섹션에서는 해당되는 경우 사용 예제와 함께 SQL 구문에 대해 자세히 설명합니다. 
이 문서는 데이터 검색 및 보조 문뿐만 아니라 데이터 정의 및 데이터 조작 문 목록을 제공합니다.

### 데이터 정의 구문

데이터 정의 문은 데이터베이스에서 데이터베이스 개체의 구조를 만들거나 수정하는 데 사용됩니다. Spark SQL은 다음과 같은 데이터 정의 문을 지원합니다:

 * [ALTER DATABASE](sql-ref-syntax-ddl-alter-database.html)
 * [ALTER TABLE](sql-ref-syntax-ddl-alter-table.html)
 * [ALTER VIEW](sql-ref-syntax-ddl-alter-view.html)
 * [CREATE DATABASE](sql-ref-syntax-ddl-create-database.html)
 * [CREATE FUNCTION](sql-ref-syntax-ddl-create-function.html)
 * [CREATE TABLE](sql-ref-syntax-ddl-create-table.html)
 * [CREATE VIEW](sql-ref-syntax-ddl-create-view.html)
 * [DROP DATABASE](sql-ref-syntax-ddl-drop-database.html)
 * [DROP FUNCTION](sql-ref-syntax-ddl-drop-function.html)
 * [DROP TABLE](sql-ref-syntax-ddl-drop-table.html)
 * [DROP VIEW](sql-ref-syntax-ddl-drop-view.html)
 * [REPAIR TABLE](sql-ref-syntax-ddl-repair-table.html)
 * [TRUNCATE TABLE](sql-ref-syntax-ddl-truncate-table.html)
 * [USE DATABASE](sql-ref-syntax-ddl-usedb.html)

### 데이터 조작 구문

데이터 조작 문은 데이터를 추가, 변경 또는 삭제하는 데 사용됩니다. Spark SQL은 다음과 같은 데이터 조작 문을 지원합니다:

 * [INSERT TABLE](sql-ref-syntax-dml-insert-table.html)
 * [INSERT OVERWRITE DIRECTORY](sql-ref-syntax-dml-insert-overwrite-directory.html)
 * [LOAD](sql-ref-syntax-dml-load.html)

### 데이터 반환 구문

Spark는 지정된 절에 따라 하나 이상의 테이블에서 행을 검색하는 데 사용되는 <code>SELECT</code> 문을 지원합니다
지원되는 절의 전체 구문과 간략한 설명은 [SELECT](sql-ref-syntax-qry-select.html) 섹션에 설명되어 있습니다. 
SELECT와 관련된 SQL 문도 이 섹션에 포함되어 있습니다. 
또한 Spark는 [EXPLAIN](sql-ref-syntax-qry-explain.html) 문을 사용하여 주어진 쿼리에 대한 논리적 및 물리적 계획을 생성할 수 있는 기능을 제공합니다.

 * [SELECT Statement](sql-ref-syntax-qry-select.html)
   * [Common Table Expression](sql-ref-syntax-qry-select-cte.html)
   * [CLUSTER BY Clause](sql-ref-syntax-qry-select-clusterby.html)
   * [DISTRIBUTE BY Clause](sql-ref-syntax-qry-select-distribute-by.html)
   * [GROUP BY Clause](sql-ref-syntax-qry-select-groupby.html)
   * [HAVING Clause](sql-ref-syntax-qry-select-having.html)
   * [Hints](sql-ref-syntax-qry-select-hints.html)
   * [Inline Table](sql-ref-syntax-qry-select-inline-table.html)
   * [File](sql-ref-syntax-qry-select-file.html)
   * [JOIN](sql-ref-syntax-qry-select-join.html)
   * [LIKE Predicate](sql-ref-syntax-qry-select-like.html)
   * [LIMIT Clause](sql-ref-syntax-qry-select-limit.html)
   * [ORDER BY Clause](sql-ref-syntax-qry-select-orderby.html)
   * [Set Operators](sql-ref-syntax-qry-select-setops.html)
   * [SORT BY Clause](sql-ref-syntax-qry-select-sortby.html)
   * [TABLESAMPLE](sql-ref-syntax-qry-select-sampling.html)
   * [Table-valued Function](sql-ref-syntax-qry-select-tvf.html)
   * [WHERE Clause](sql-ref-syntax-qry-select-where.html)
   * [Window Function](sql-ref-syntax-qry-select-window.html)
   * [CASE Clause](sql-ref-syntax-qry-select-case.html)
   * [PIVOT Clause](sql-ref-syntax-qry-select-pivot.html)
   * [LATERAL VIEW Clause](sql-ref-syntax-qry-select-lateral-view.html)
   * [TRANSFORM Clause](sql-ref-syntax-qry-select-transform.html)
 * [EXPLAIN](sql-ref-syntax-qry-explain.html)

### 보조문

 * [ADD FILE](sql-ref-syntax-aux-resource-mgmt-add-file.html)
 * [ADD JAR](sql-ref-syntax-aux-resource-mgmt-add-jar.html)
 * [ANALYZE TABLE](sql-ref-syntax-aux-analyze-table.html)
 * [CACHE TABLE](sql-ref-syntax-aux-cache-cache-table.html)
 * [CLEAR CACHE](sql-ref-syntax-aux-cache-clear-cache.html)
 * [DESCRIBE DATABASE](sql-ref-syntax-aux-describe-database.html)
 * [DESCRIBE FUNCTION](sql-ref-syntax-aux-describe-function.html)
 * [DESCRIBE QUERY](sql-ref-syntax-aux-describe-query.html)
 * [DESCRIBE TABLE](sql-ref-syntax-aux-describe-table.html)
 * [LIST FILE](sql-ref-syntax-aux-resource-mgmt-list-file.html)
 * [LIST JAR](sql-ref-syntax-aux-resource-mgmt-list-jar.html)
 * [REFRESH](sql-ref-syntax-aux-cache-refresh.html)
 * [REFRESH TABLE](sql-ref-syntax-aux-cache-refresh-table.html)
 * [REFRESH FUNCTION](sql-ref-syntax-aux-cache-refresh-function.html)
 * [RESET](sql-ref-syntax-aux-conf-mgmt-reset.html)
 * [SET](sql-ref-syntax-aux-conf-mgmt-set.html)
 * [SHOW COLUMNS](sql-ref-syntax-aux-show-columns.html)
 * [SHOW CREATE TABLE](sql-ref-syntax-aux-show-create-table.html)
 * [SHOW DATABASES](sql-ref-syntax-aux-show-databases.html)
 * [SHOW FUNCTIONS](sql-ref-syntax-aux-show-functions.html)
 * [SHOW PARTITIONS](sql-ref-syntax-aux-show-partitions.html)
 * [SHOW TABLE EXTENDED](sql-ref-syntax-aux-show-table.html)
 * [SHOW TABLES](sql-ref-syntax-aux-show-tables.html)
 * [SHOW TBLPROPERTIES](sql-ref-syntax-aux-show-tblproperties.html)
 * [SHOW VIEWS](sql-ref-syntax-aux-show-views.html)
 * [UNCACHE TABLE](sql-ref-syntax-aux-cache-uncache-table.html)
