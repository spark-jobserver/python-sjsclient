import json

import requests

from sjsclient import client


def get_demeter_config():
    json_config = """
    {"spark_jobserver": { "host": "10.29.23.172", "port": 8090 } }
    """
    return json.loads(json_config)


def get_sjs_client():
    demeter_config = get_demeter_config()
    sjs_config = demeter_config.get('spark_jobserver', {})
    spark_jobserver_url = "http://%s:%d" % (sjs_config.get('host'),
                                            sjs_config.get('port'))
    auth = None
    user = sjs_config.get('user')
    password = sjs_config.get('password')

    if user or password:
        auth = requests.auth.HTTPBasicAuth(user, password)
    return client.Client(spark_jobserver_url, auth)
