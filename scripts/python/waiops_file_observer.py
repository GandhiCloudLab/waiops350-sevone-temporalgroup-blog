#!/usr/bin/env python
import sys
import json
import base64
import requests
from json import dumps
import urllib3

from config import *
from common_util import *

def uploadFileToFileObserver(fileObserverFile):
    printHeading3(False, "Upload file to WAIOps FileObserver Started ", True)
    print("Uploading the file :  " + fileObserverFile)

    basicAuth_string = WAIOPS_TOPO_USER + ':' + WAIOPS_TOPO_PWD
    basicAuth_bytes = basicAuth_string.encode("ascii") 
    basicAuth_bytes_encoded = base64.b64encode(basicAuth_bytes) 
    basicAuth_bytes_decoded = basicAuth_bytes_encoded.decode("ascii") 

    headers = {
        'Authorization': 'Basic ' + basicAuth_bytes_decoded,
        # 'Accept':'application/json',
        # 'Content-Type' : 'multipart/form-data',
        'X-TenantID' : WAIOPS_TOPO_TENENT_ID
        }

    files = {'job_file': open(fileObserverFile, 'rb')}

    ### Upload to WAIOps FileObserver by POST - New file
    if (WAIOPS_TOPO_UPLOAD_TYPE == "POST" or WAIOPS_TOPO_UPLOAD_TYPE == "BOTH") :
        print("Uploading to WAIOps FileObserver via POST ..")
        requestsPostFile(WAIOPS_TOPO_URL, headers, files)

    ### Upload to WAIOps FileObserver by PUT - Updated file
    if (WAIOPS_TOPO_UPLOAD_TYPE == "PUT" or WAIOPS_TOPO_UPLOAD_TYPE == "BOTH") :
        print("Uploading to WAIOps FileObserver via PUT ..")
        requestsPutFile(WAIOPS_TOPO_URL, headers, files)

    printHeading3(False, "Upload file to WAIOps FileObserver Completed ", True)