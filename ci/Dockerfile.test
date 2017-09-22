FROM noorul/python-sjsclient-ft

RUN git clone https://github.com/spark-jobserver/spark-jobserver /opt/spark-jobserver

WORKDIR /opt/spark-jobserver

COPY ci/application.conf /opt/spark-jobserver/job-server/src/main/resources/application.conf
COPY ci/start.sh start.sh
COPY ci/log4j-server.properties /opt/spark-jobserver/bin/log4j-server.properties
COPY ci/application.conf /opt/spark-jobserver/bin/application.conf

RUN sbt job-server-extras/assembly job-server-tests/package buildPython buildPyExamples

RUN cp /opt/spark-jobserver/job-server-extras/target/scala-2.11/spark-job-server.jar /opt/spark-jobserver/bin/spark-job-server.jar && \
    touch bin/settings.sh

COPY . .
