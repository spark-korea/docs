---
layout: global
displayTitle: Spark Overview
title: Overview
description: Apache Spark SPARK_VERSION_SHORT documentation homepage
---

**Programming Guides:**

* [빠른 시작](quick-start.html): a quick introduction to the Spark API; start here!
* [RDD Programming Guide](rdd-programming-guide.html): overview of Spark basics - RDDs (core but old API), accumulators, and broadcast variables
* [스파크 SQL, DataFrame, Dataset 가이드](sql-programming-guide.html): processing structured data with relational queries (newer API than RDDs)
* [구조화된 스트리밍](structured-streaming-programming-guide.html): processing structured data streams with relation queries (using Datasets and DataFrames, newer API than DStreams)
* [Spark Streaming](streaming-programming-guide.html): processing data streams using DStreams (old API)
* [MLlib](ml-guide.html): applying machine learning algorithms
* [GraphX](graphx-programming-guide.html): processing graphs 

**API Docs:**

* [Spark Scala API (Scaladoc)](api/scala/index.html#org.apache.spark.package)
* [Spark Java API (Javadoc)](api/java/index.html)
* [Spark Python API (Sphinx)](api/python/index.html)
* [Spark R API (Roxygen2)](api/R/index.html)
* [Spark SQL, Built-in Functions (MkDocs)](api/sql/index.html)

**Deployment Guides:**

* [Cluster Overview](cluster-overview.html): overview of concepts and components when running on a cluster
* [Submitting Applications](submitting-applications.html): packaging and deploying applications
* Deployment modes:
  * [Amazon EC2](https://github.com/amplab/spark-ec2): scripts that let you launch a cluster on EC2 in about 5 minutes
  * [Standalone Deploy Mode](spark-standalone.html): launch a standalone cluster quickly without a third-party cluster manager
  * [Mesos](running-on-mesos.html): deploy a private cluster using
      [Apache Mesos](https://mesos.apache.org)
  * [YARN](running-on-yarn.html): deploy Spark on top of Hadoop NextGen (YARN)
  * [Kubernetes](running-on-kubernetes.html): deploy Spark on top of Kubernetes

**Other Documents:**

* [Configuration](configuration.html): customize Spark via its configuration system
* [Monitoring](monitoring.html): track the behavior of your applications
* [Tuning Guide](tuning.html): best practices to optimize performance and memory use
* [Job Scheduling](job-scheduling.html): scheduling resources across and within Spark applications
* [Security](security.html): Spark security support
* [Hardware Provisioning](hardware-provisioning.html): recommendations for cluster hardware
* Integration with other storage systems:
  * [Cloud Infrastructures](cloud-integration.html)
  * [OpenStack Swift](storage-openstack-swift.html)
* [Building Spark](building-spark.html): build Spark using the Maven system
* [Contributing to Spark](https://spark.apache.org/contributing.html)
* [Third Party Projects](https://spark.apache.org/third-party-projects.html): related third party Spark projects

**External Resources:**

* [Spark Homepage](https://spark.apache.org)
* [Spark Community](https://spark.apache.org/community.html) resources, including local meetups
* [StackOverflow tag `apache-spark`](http://stackoverflow.com/questions/tagged/apache-spark)
* [Mailing Lists](https://spark.apache.org/mailing-lists.html): ask questions about Spark here
* [AMP Camps](http://ampcamp.berkeley.edu/): a series of training camps at UC Berkeley that featured talks and
  exercises about Spark, Spark Streaming, Mesos, and more. [Videos](http://ampcamp.berkeley.edu/6/),
  [slides](http://ampcamp.berkeley.edu/6/) and [exercises](http://ampcamp.berkeley.edu/6/exercises/) are
  available online for free.
* [Code Examples](https://spark.apache.org/examples.html): more are also available in the `examples` subfolder of Spark ([Scala]({{site.SPARK_GITHUB_URL}}/tree/master/examples/src/main/scala/org/apache/spark/examples),
 [Java]({{site.SPARK_GITHUB_URL}}/tree/master/examples/src/main/java/org/apache/spark/examples),
 [Python]({{site.SPARK_GITHUB_URL}}/tree/master/examples/src/main/python),
 [R]({{site.SPARK_GITHUB_URL}}/tree/master/examples/src/main/r))
