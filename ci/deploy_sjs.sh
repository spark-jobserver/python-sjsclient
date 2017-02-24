#!/bin/bash

docker build -t sjsclient_ft -f ci/Dockerfile.test .
docker run --name sjs_db -d sjsclient_ft /bin/bash -c "/opt/h2/bin/h2-server.sh;"
docker ps -a
docker run --link sjs_db:db --name sjs -d sjsclient_ft /bin/bash -c "cd /opt/spark-jobserver; ./start.sh;"
docker ps -a
