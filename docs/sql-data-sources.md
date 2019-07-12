---
layout: global
title: 데이터 소스
displayTitle: 데이터 소스
---


# **데이터 소스**


# 스파크 SQL에서는 DataFrame 인터페이스를 통해 다양한 형태의 데이터 소스를 사용할 수 있습니다. DataFrame은 관계형 변환을 사용하여 동작하며 임시 뷰를 생성하는 것도 가능합니다. DataFrame을 임시 뷰로 등록하면 데이터 자체에서 SQL 쿼리를 실행할 수 있게 됩니다. 이번 섹션에서는 스파크 데이터 소스를 사용하여 데이터를 불러오고 저장하는 일반적인 방법에 대해 배우고 내장 데이터 소스에서 사용할 수 있는 추가 옵션에 대해 배우도록 하겠습니다.


*   [일반 불러오기/저장하기 함수](https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html)
    *   [옵션 명시하기](https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#manually-specifying-options)
    *   [파일 내에서 SQL 바로 실행하기](https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#run-sql-on-files-directly)
    *   [저장 모드](https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#save-modes)
    *   [지속 테이블에 저장하기](https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#saving-to-persistent-tables)
    *   [버킷화, 정렬, 분할](https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#bucketing-sorting-and-partitioning)
*   [Parquet 파일](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html)
    *   [프로그램에서 데이터 불러오기](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#loading-data-programmatically)
    *   [분할 탐색](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#partition-discovery)
    *   [스키마 병합](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#schema-merging)
    *   [Hive 메타스토어의 Parquet 테이블 변환](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#hive-metastore-parquet-table-conversion)
    *   [설정](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#configuration)
*   [ORC 파일](https://spark.apache.org/docs/latest/sql-data-sources-orc.html)
*   [JSON 파일](https://spark.apache.org/docs/latest/sql-data-sources-json.html)
*   [Hive 테이블](https://spark.apache.org/docs/latest/sql-data-sources-hive-tables.html)
    *   [Hive 테이블의 저장 형식 명시하기](https://spark.apache.org/docs/latest/sql-data-sources-hive-tables.html#specifying-storage-format-for-hive-tables)
    *   [다른 버전의 Hive 메타스토어와 인터랙션하기 ](https://spark.apache.org/docs/latest/sql-data-sources-hive-tables.html#interacting-with-different-versions-of-hive-metastore)
*   [JDBC를 통한 다른 데이터베이스 사용하기](https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html)
*   [Avro 파일](https://spark.apache.org/docs/latest/sql-data-sources-avro.html)
    *   [배포하기](https://spark.apache.org/docs/latest/sql-data-sources-avro.html#deploying)
    *   [불러오기와 저장하기 함수](https://spark.apache.org/docs/latest/sql-data-sources-avro.html#load-and-save-functions)
    *   [to_avro()와 from_avro()](https://spark.apache.org/docs/latest/sql-data-sources-avro.html#to_avro-and-from_avro)
    *   [데이터 소스 옵션](https://spark.apache.org/docs/latest/sql-data-sources-avro.html#data-source-option)
    *   [설정](https://spark.apache.org/docs/latest/sql-data-sources-avro.html#configuration)
    *   [Databricks spark-avro와의 호환성](https://spark.apache.org/docs/latest/sql-data-sources-avro.html#compatibility-with-databricks-spark-avro)
    *   [Avro -> Spark SQL conversion 변환에 지원되는 타입](https://spark.apache.org/docs/latest/sql-data-sources-avro.html#supported-types-for-avro---spark-sql-conversion)
    *   [Spark SQL -> Avro conversion 변환에 지원되는 타입](https://spark.apache.org/docs/latest/sql-data-sources-avro.html#supported-types-for-spark-sql---avro-conversion)
*   [문제 해결](https://spark.apache.org/docs/latest/sql-data-sources-troubleshooting.html)
