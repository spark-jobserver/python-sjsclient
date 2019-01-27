#!/bin/bash

appdir="/opt/spark-jobserver/bin"
conffile="$appdir/application.conf"
export MANAGER_JAR_FILE="file:$appdir/spark-job-server.jar"
export MANAGER_CONF_FILE="file:$conffile"
export MANAGER_LOGGING_OPTS="-Dlog4j.configuration=file:$appdir/log4j-server.properties"

exec $SPARK_HOME/bin/spark-submit --driver-java-options "-Dlog4j.configuration=file:/opt/spark-jobserver/bin/log4j-server.properties" --class spark.jobserver.JobServer /opt/spark-jobserver/bin/spark-job-server.jar
