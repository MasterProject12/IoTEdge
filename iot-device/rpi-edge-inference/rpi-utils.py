import boto3
from boto3.dynamodb.conditions import Key, Attr
import logging
import subprocess
import os
import glob
import json
from mutagen.mp3 import MP3
import math
from time import sleep
import os.path

import sys
from time import strftime
from PIL import Image, ImageDraw, ImageFont

from os import listdir
from os.path import isfile, join

try:
    #from picamera import PiCamera
    from gpiozero import LED, Button
    #from gpiozero import LED
    test_environment = False
except (ImportError, RuntimeError):
    #import cv2
    test_environment = True

import cups
import requests

import sqlite3
from datetime import datetime

from config import Configuration

# --------- Module- Level Globals ---------------
config = Configuration()

print(config.__SQS_BACKEND_QUEUE__)
# --------- End of Module-Level Globals ----------

def show_images(media_dir=config.__CEREBRO_MEDIA_DIR__, debug_mode=False):

    show_images_logger = logging.getLogger('tf_utils.show_images')

    show_images_logger.info("Entered the switch_images method ...")
    
    if debug_mode:
        show_images_logger.info("In Debug mode, so no showing of images!")
        return True

    show_images_logger.info("And now, starting up the image again ...")
    slideshow_log = "%s/picframe.start.log" % config.__CEREBRO_LOGS_DIR__
    status = subprocess.call(
        '%s && %s "%s" > %s 2>&1 &' % 
        (media_dir, slideshow_log), 
        shell=True)

    show_images_logger.info("Switching of images is now complete!")    

    return True

def download_json(profile_name="", media_dir='', ignore_stock_profiles=False):
    download_media_logger = logging.getLogger('cerebro_processor.download_media')

    download_media_logger.info("Entered Download_media ...")
    # Create an S3 client
    s3 = boto3.resource('s3')

    download_media_logger.info("Downloading Media now ...")

    payload={}
    payload['profile']=profile_name
    payload['audio']='yes'
    payload['image_max_count'] = str(config.__IMAGE_MAX_COUNT__)
    if ignore_stock_profiles:
        payload['ignore_stock_profiles'] = "1"

    headers = {
        'Content-Type': "application/json",
        'x-api-key': config.__APIGW_X_API_KEY__
        }

    url = config.__APIGW_API__

    download_media_logger.info("URL: %s, payload: %s" % (url, json.dumps(payload)) )
    response = requests.request(
        "POST", 
        url, 
        data=json.dumps(payload), 
        headers=headers)

    s3_bucket = config.__S3_BUCKET__
    s3_key = ""

    download_media_logger.debug("Response: %s" % (json.dumps(response.json())) )

    media_count = len(response.json())
    download_media_logger.info("Total Number of Media files: %d" % media_count )

    for item in response.json():
        download_media_logger.info("Processing Media: %s ..." % item["image_key"])
        # now download the s3 files one by one
        s3_key = item["image_key"]
        media_caption = item["image_caption"]
        if media_dir:
            local_file = "%s/%s" % (media_dir, os.path.basename(s3_key))
        else:
            local_file = "%s/%s" % (config.__CEREBRO_MEDIA_DIR__, os.path.basename(s3_key))

        download_media_logger.info("Try downloading file: %s" % s3_key)
        try:
            s3.Bucket(s3_bucket).download_file(s3_key, local_file)
        except botocore.exceptions.ClientError as e:
            print("Error seen!")
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
        download_media_logger.info("Image Downloaded to %s." % local_file)

    download_media_logger.info("Media downloaded.")
    return media_count

def write_json():
    # create a dictionary  
    data_holder = tf_data["data"]
    counter = 0        
    while counter < 3:
        data_holder.append(write())
        counter += 1    
    #write the file        
    file_path='/tf/msg_json_dir/car_data.json'
    with open(file_path, 'w') as outfile:
        print("writing json file to: ",file_path)
        json.dump(tf_data, outfile)
    outfile.close()     
    print("done")

def __init__(self, filename):
        self.console = sys.stdout
        self.file = open(filename, 'w')

def write(self, message):
        path = '/tf/msg_json_dir'
        self.console.write(message)
        self.file.write(message)
 
def flush(self):
        self.console.flush()
        self.file.flush()


