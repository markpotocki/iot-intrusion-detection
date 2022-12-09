from awscrt import mqtt
from awsiot import mqtt_connection_builder
from logger import log

# Constants
CLIENT_ID = '029f'
ENDPOINT = 'a2oywy2tufou84-ats.iot.us-east-2.amazonaws.com'
PORT = 443
CERT_PATH = '../credentials/bcd7ea66fb136ad3a3789bc441db33e153a41b080c8631e26b7ca81b60048054-certificate.pem.crt'
PRI_KEY = '../credentials/bcd7ea66fb136ad3a3789bc441db33e153a41b080c8631e26b7ca81b60048054-private.pem.key'
CA_PATH = '../credentials/AmazonRootCA1.pem'

connection = None

def create_mqtt_connection() -> mqtt.Connection:
    # Establish connection
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        port=PORT,
        cert_filepath=CERT_PATH,
        pri_key_filepath=PRI_KEY,
        ca_filepath=CA_PATH,
        on_connection_interrupt=on_connection_interrupt,
        on_connection_resumed=on_connection_resumed,
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=30,
    )
    connect_future = mqtt_connection.connect()

    # Connect to endpoint
    connect_future.result()
    log('Connected')  

    global connection
    connection = mqtt_connection
    return mqtt_connection


def on_connection_interrupt():
    log('Connection has been lost')


def on_connection_resumed():
    log('Connection has been established')