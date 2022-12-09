from logger import log
from awsiot import mqtt
import json

# Topics
TOPIC_GET_CONFIG = '$aws/things/RP_IDP_Camera/shadow/name/RP_IDP_Camera-Shadow/get'
TOPIC_GET_CONFIG_ACCEPTED = '$aws/things/RP_IDP_Camera/shadow/name/RP_IDP_Camera-Shadow/get/accepted'
TOPIC_SET_CONFIG = '$aws/things/RP_IDP_Camera/shadow/name/RP_IDP_Camera-Shadow/update'
TOPIC_SET_CONFIG_ACCEPTED = '$aws/things/RP_IDP_Camera/shadow/name/RP_IDP_Camera-Shadow/update/accepted'

# Config
CONFIG_DEFAULT_ROOM = 'living-room'
CONFIG_DEFAULT_SUPPORT_CONTACT = {
    'name': 'Mark Potocki',
    'email': 'mepotock@asu.edu'
}
CONFIG_DEFAULT_SYSTEMID = 'FIN'
configuration = {}


def load_configuration(connection: mqtt.Connection, topic: str) -> None:
    log('loading configuration from {0}'.format(topic))
    get_config_future, _ = connection.publish(
        topic=topic,
        payload=json.dumps({}),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    get_config_future.result()
    log('configuration request sent successfully')


def set_configuration(connection: mqtt.Connection, topic: str, config: dict) -> None:
    log('setings configuration at {0}'.format(topic))
    set_config_future, _ = connection.publish(
        topic=topic,
        payload=json.dumps(config),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    #set_config_future.result()
    log('configuration set sent successfully')


def accept_configuration(topic: str, payload: bytes, dup: bool, qos: mqtt.QoS, retain: bool, **kwargs: dict):
    log('configuration change accepted [{0}]'.format(topic))


def get_config_accepted(topic: str, payload: bytes, dup: bool, qos: mqtt.QoS, retain: bool, **kwargs: dict):
    log('received configuration from shadow on {0}'.format(topic))
    obj = json.loads(payload)
    global configuration
    configuration = obj
    log('configuration loaded with value:\n' + json.dumps(obj))
