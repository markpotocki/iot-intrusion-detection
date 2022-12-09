from datetime import datetime
#import connection
import json
from awsiot import mqtt

TOPIC_TELEMETRY_LOG = 'dt/idp/{0}/log'
TOPIC_TELEMETRY_LOG_ACCEPTED = 'dt/idp/{0}/log/accepted'

def log(message: str, level='INFO') -> None:
    timestamp = datetime.now()
    #connection.connection.publish(
    #    topic=TOPIC_TELEMETRY_LOG,
    #    payload=json.dumps({
    #        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S%Z'),
    #        'level': level,
    #        'message': message
    #    }),
    #    qos=mqtt.QoS.EXACTLY_ONCE
    #)
    
    print('{0}  {1}'.format(
        timestamp.strftime('%Y-%m-%d %H:%M:%S%Z'),
        message))

