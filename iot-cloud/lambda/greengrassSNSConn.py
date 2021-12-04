# This Lambda function requires the AWS Greengrass SDK to run on Greengrass devices. This can be found on the AWS IoT Console.
# IMPORTING OUR LIBRARIES

import json
import greengrasssdk
import cv2

iot_client = greengrasssdk.client('iot-data')
send_topic = 'sns/message'
video = cv2.VideoCapture(0)
display_handle=display(None, display_id=True)
from pathlib import Path
from IPython.display import clear_output, Image, display

import ipywidgets
import cv2


def create_request():
    return {
        "request": 
           try: 
                clear_output(wait=True)
                _, frame = video.read()
                lines, columns, _ =  frame.shape
                frame = cv2.resize(frame, (int(columns/4), int(lines/4))) 
                image_widget.value =cv2.imencode('.jpeg', frame)[1].tobytes()
                display(image_widget)
           except KeyboardInterrupt:
                video.release()
                break
                }

def publish_basic_message():
    message = create_request()
    print(f"Message to publish: {message}")
    iot_client.publish(topic=send_topic, payload=json.dumps(message))

publish_basic_message()

# In this example, the required AWS Lambda handler is never called.
def function_handler(event, context):
    pass