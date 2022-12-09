from awsiot import mqtt
import connection
from logger import log
import json
import os
import time

def reboot(topic: str, payload: bytes, dup: bool, qos: mqtt.QoS, retain: bool, **kwargs: dict):
    reboot_cmd = json.loads(payload)
    session_id = reboot_cmd['session-id']
    res_topic = reboot_cmd['response-topic']
    reboot_at = reboot_cmd['reboot-at']

    epoch_now_mins = time.time() / 60
    shutdown_diff = reboot_at - epoch_now_mins
    log('shutdown scheduled for {0} mins in future'.format(shutdown_diff))

    reboot_future, _ = connection.connection.publish(
        topic=res_topic,
        payload=json.dumps({
            'session-id': session_id,
            'device-id': connection.CLIENT_ID,
            'status': 'OK'
        }),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

    log('rebooting device...')
    reboot_future.result()
    os.system('shutdown -r +{0}'.format(reboot_at))
