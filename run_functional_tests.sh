#!/bin/bash

export TESTSJS_SPARKJOB_SERVER_URL=${TESTSJS_SPARKJOB_SERVER_URL:-http://localhost:8090}
export TESTSJS_SPARK_TEST_CTX=${TESTSJS_SPARK_TEST_CTX:-python-sjsclient-ft}
export TESTSJS_SPARKJOB_JAR_URL=${TESTSJS_SPARKJOB_JAR_URL:-http://localhost/job-server-tests_2.10-0.6.1-SNAPSHOT.jar}
export TESTSJS_SPARKJOB_JARS_DIR=/tmp/testsjs_sparkjob_jars
export TESTSJS_SPARKJOB_SERVER_AUTH_ENABLED=${TESTSJS_SPARKJOB_SERVER_AUTH_ENABLED:-1}
if [ $TESTSJS_SPARKJOB_SERVER_AUTH_ENABLED -eq 1 ]; then
   export TESTSJS_SPARKJOB_SERVER_USERNAME=sjs
   export TESTSJS_SPARKJOB_SERVER_PASSWORD=sjs
else
   unset TESTSJS_SPARKJOB_SERVER_USERNAME
   unset TESTSJS_SPARKJOB_SERVER_PASSWORD
fi

echo "Running functonal tests against spark job server, $TESTSJS_SPARKJOB_SERVER_URL"

# Download the spark job jars archive.
if ! curl -s -o $TESTSJS_SPARKJOB_JARS_DIR/$(basename $TESTSJS_SPARKJOB_JAR_URL) --create-dirs $TESTSJS_SPARKJOB_JAR_URL; then
    echo "Failed to connect to Spark job Jars archive server $TESTSJS_SPARKJOB_JAR_URL"
    exit 1
fi

# Check whether Spark Job Server is up and running, if not fail.
if ! curl -s -o /dev/null $TESTSJS_SPARKJOB_SERVER_URL/contexts; then
    echo "Failed to connect to Spark Job Server API $TESTSJS_SPARKJOB_SERVER_URL"
    exit 1
fi

python setup.py install

# Setup test bed
python -c "from sjsclient.tests.functional import base; base.bootstrap_testbed()"

python setup.py testr $@
