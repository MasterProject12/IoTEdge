import sys
import greengrasssdk
import platform
import os
import logging

# Create a Greengrass Core SDK client.
client = greengrasssdk.client('iot-data')

volumePath = '/tf/msg_json_dir'

def function_handler(event, context):
    client.publish(topic='local/resources', payload='Sent from tf message json to AWS IoT Greengrass Core.')
    try:
        volumeInfo = os.stat(volumePath)
        client.publish(topic='local/resources', payload=str(volumeInfo))
        with open(volumePath + '/tf', 'a') as output:
            output.write('tf json file successfully wrote to a disk.\n')
        with open(volumePath + '/tf', 'r') as myfile:
            data = myfile.read()
        client.publish(topic='local/resources', payload=data)
    except Exception as e:
        logging.error("Unexpected error  :{}".format(e))
    return