import greengrasssdk
import time
import json
import sys
import cv2
import time

#aGPS adafruit chips unable standalone device
from gps3 import agps3
from pathlib import Path
from IPython.display import clear_output, Image, display

import ipywidgets
import cv2

#GPS-Set-up
gps_socket = agps3.GPSDSocket()
data_stream = agps3.DataStream()
gps_socket.connect()
gps_socket.watch()
video = cv2.VideoCapture(0)
display_handle=display(None, display_id=True)

image_widget = ipywidgets.Image(format='jpeg')
iot_client = greengrasssdk.client('iot-data')
send_topic = 'sns/message'

def create_request_with_all_fields():
    return  {
         "request": {
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
                },
    }

def create_gps_coordinates():
    print('Connecting GPS Socket')
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            alt = data_stream.alt
            lat = data_stream.lat
            lon = data_stream.lon
        if (lat != "n/a"):
            break
    print('Altitue = ', alt)
    print('Lantitude = ', lat)
    print('Longitude = ', lon)
    print('-------------------') 

def publish_basic_message():
    messageToPublish = create_request_with_all_fields()
    print("Message To Publish: ", messageToPublish)
    iot_client.publish(topic=send_topic,
        payload=json.dumps(messageToPublish))

publish_basic_message()

def function_handler(event, context):
    return