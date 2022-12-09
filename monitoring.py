from logger import log
from awsiot import mqtt
import connection
import time
import os
import json
import requests
import config

TOPIC_S3_UPLOAD = 'cameras/idp/{0}/upload'.format(connection.CLIENT_ID)
TOPIC_S3_UPLOAD_ACCEPTED = 'cameras/idp/{0}/upload/accept'.format(connection.CLIENT_ID)

is_monitoring = False

def monitor(topic: str, payload: bytes, dup: bool, qos: mqtt.QoS, retain: bool, **kwargs: dict):
    monitor_cmd = json.loads(payload)
    session_id = monitor_cmd['session-id']
    response_topic = monitor_cmd['response-topic']
    subcommand = monitor_cmd['subcommand']
    interval = monitor_cmd['photo-interval']

    log('received monitoring command on {0}'.format(topic))
    log(payload)

    global is_monitoring
    if subcommand == 'START':
        log('starting monitoring')
        is_monitoring = True
        config.set_configuration(connection.connection, config.TOPIC_SET_CONFIG, {
            'state': {
                'reported': {
                    'monitoring': True,
                    'interval-sec': interval
                }
            }
        })
    elif subcommand == 'STOP':
        log('stopping monitoring')
        is_monitoring = False
        config.set_configuration(connection.connection, config.TOPIC_SET_CONFIG, {
            'state': {
                'reported': {
                    'monitoring': False,
                    'interval-sec': None
                }
            }
        })
    else:
        log('invalid subcommand received: {0}'.format(subcommand))
        return

    monitor_future, _ = connection.connection.publish(
        topic=response_topic,
        payload=json.dumps({
            'device-id': connection.CLIENT_ID,
            'session-id': session_id,
            'status': 'OK'
        }),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    
    log('is_monitoring: {0}'.format(is_monitoring))
    take_photo_and_notify(connection.connection, interval)


def take_photo_and_notify(mqtt_connection: mqtt.Connection, interval_seconds: int):
    # create temporary path
    timestamp = str(time.time())
    img_path = '/tmp/' + timestamp + '.jpg'
    
    # take photo
    os.system('raspistill -vf -o ' + img_path)
    log('photo captured and outputted to ' + img_path)
    # create message payload
    payload = {
        'device_id': connection.CLIENT_ID,
        'local_path': img_path,
        'timestamp': timestamp
    }
    # send notification of new image
    message_send_future, _ = mqtt_connection.publish(
        topic=TOPIC_S3_UPLOAD,
        payload=json.dumps(payload),
        qos=mqtt.QoS.EXACTLY_ONCE
    )
    #message_send_future.result()
    log('new photo notification sent to topic ' + TOPIC_S3_UPLOAD)
    time.sleep(interval_seconds)


def upload_image_with_presigned_url(topic: str, payload: bytes, dup: bool, qos: mqtt.QoS, retain: bool, **kwargs: dict):
    log('received presigned url for image upload on {0}'.format(topic))
    obj = json.loads(payload)
    local_file_path = obj['local_path']
    presigned_url = obj['presigned_url']

    with open(local_file_path, 'rb') as img_file:
        img_text = img_file.read()
    response = requests.put(presigned_url, data=img_text)
    
    if response.status_code < 200 or response.status_code > 299:
        log('upload received bad status {0}'.format(response.status_code))
    log('uploaded image to S3')
    os.remove(local_file_path) # remove file since it is uploaded
