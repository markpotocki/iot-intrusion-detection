from awscrt import mqtt
from logger import log

class SubscriptionManager:

    subscriptions = []

    def __init__(self, connection: mqtt.Connection):
        self._connection = connection

    
    def remove_subscription(self, topic: str):
        pass


    def load_subscriptions(self, subs: dict[str, any]):
        for topic, callback in subs.items():
            log('subscribing to topic {0}'.format(topic))
            get_config_accepted_future, packet_id = self._connection.subscribe(
                topic,
                mqtt.QoS.AT_LEAST_ONCE,
                callback)
            get_config_accepted_sub = get_config_accepted_future.result()
            log('subscribed with {0}'.format(get_config_accepted_sub['qos']))
