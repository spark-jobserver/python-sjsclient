SJS_JAR_PATH=$(find `pwd` -name spark-job-server.jar)
exec $SPARK_HOME/bin/spark-submit --class spark.jobserver.JobServer ${SJS_JAR_PATH}
