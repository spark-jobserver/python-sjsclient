#!/bin/bash

docker exec sjs /bin/bash -c "cd /opt/spark-jobserver; tox -e functional_py34"
