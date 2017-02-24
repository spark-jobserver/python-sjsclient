#!/bin/bash
exec $SPARK_HOME/bin/spark-submit --driver-java-options "-Dlog4j.configuration=file:/opt/spark-jobserver/bin/log4j-server.properties" --class spark.jobserver.JobServer /opt/spark-jobserver/bin/spark-job-server.jar
