from ReadGoogleSheet import *
from TwitterFunctions import *
import json
import time
import boto3
from datetime import datetime
import os

Users = getSheetData()
output = []
for user in Users:
    try:
        if user["Twitter ID"] != "":
            pass
            data = getTweetsByUser(user["Twitter ID"])
            output.append(data)
            writeCaptureStatus(user["FullName"], "Success")
        else:
            if user["Twitter Handle"] != "":
                userData = getUserByUsername(user["Twitter Handle"])
                ID = userData['data']['id']
                writeIDToSheet(user["Twitter Handle"], ID)
                data = getTweetsByUser(ID)
                output.append(data)
                writeCaptureStatus(user["FullName"], "Success")
            else:
                writeCaptureStatus(user["FullName"], "No Twitter Handle")
    except Exception as e:
        writeCaptureStatus(user["FullName"], f'Error: {e}')
    time.sleep(90)

with open('output.json', 'w') as f:
    json.dump(output, f)


timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
file_name = f'raw_data/twitterpull/{timestamp}.json'
bucket = 'socialsignalsdata'

s3_client = boto3.client(
    's3'
)

try:
    response = s3_client.upload_file('output.json', bucket, file_name)
except ClientError as e:
    print(e)

if os.path.exists('output.json'):
    os.remove('output.json')
