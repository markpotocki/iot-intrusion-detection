from awsiot import mqtt
from logger import log
import connection
import os
import time
import json

def shutdown(topic: str, payload: bytes, dup: bool, qos: mqtt.QoS, retain: bool, **kwargs: dict):
    shutdown_request = json.loads(payload)
    session_id = shutdown_request['session-id']
    res_topic = shutdown_request['response-topic']
    shutdown_at = shutdown_request['shutdown-at']

    log('shutdown scheduled for {0} mins in future'.format(shutdown_at))

    pub_future, _ = connection.connection.publish(
        topic=res_topic,
        payload=json.dumps({
            "session-id": session_id,
            "device-id": connection.CLIENT_ID,
            "shutdown-status": "OK"
        }),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

    log('system is shutting down...')
    os.system('sudo shutdown +{0}'.format(shutdown_at))
