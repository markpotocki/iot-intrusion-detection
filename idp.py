from awscrt import mqtt
from subscriptionmanager import SubscriptionManager
from shutdowning import shutdown
from rebooting import reboot
from logger import log
from monitoring import monitor, TOPIC_S3_UPLOAD_ACCEPTED, upload_image_with_presigned_url
import connection
import time
import config

# Command Topics
TOPIC_CMD_SHUTDOWN = 'cmd/idp/{0}/shutdown'.format(connection.CLIENT_ID)
TOPIC_CMD_REBOOT = 'cmd/idp/{0}/reboot'.format(connection.CLIENT_ID)
TOPIC_CMD_MONITOR = 'cmd/idp/{0}/monitor'.format(connection.CLIENT_ID)


def main():
    start_time = time.time()
    conn = connection.create_mqtt_connection()

    # subscriptions
    subscription_manager = SubscriptionManager(conn)
    subscription_manager.load_subscriptions({
        config.TOPIC_GET_CONFIG_ACCEPTED: config.get_config_accepted,
        TOPIC_S3_UPLOAD_ACCEPTED: upload_image_with_presigned_url,
        TOPIC_CMD_SHUTDOWN: shutdown,
        TOPIC_CMD_REBOOT: reboot,
        TOPIC_CMD_MONITOR: monitor,
        config.TOPIC_SET_CONFIG_ACCEPTED: config.accept_configuration
    })

    # Publish the current state of the device
    global configuration
    configuration = {
        'state':{
            'reported': {
                'status': 'starting',
                'start-time': start_time,
                'support-contact': config.CONFIG_DEFAULT_SUPPORT_CONTACT,
                'system-id': config.CONFIG_DEFAULT_SYSTEMID,
                'device-id': connection.CLIENT_ID 
            }
        }
    }
    config.set_configuration(connection=connection.connection, topic=config.TOPIC_SET_CONFIG, config=configuration)

    config.load_configuration(conn, config.TOPIC_GET_CONFIG)

    # event loop
    config.set_configuration(connection=connection.connection, topic=config.TOPIC_SET_CONFIG, config={
        'state': {
            'reported': {
                'status': 'running'
            }
        }
    })
    log('awaiting commands...')
    hold = input('Press enter to quit')




if __name__ == '__main__':
    main()

