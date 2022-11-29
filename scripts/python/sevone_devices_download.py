#!/usr/bin/env python
import sys
import json
import base64
import requests
from json import dumps
import urllib3

from config import *
from common_util import *
from sevone_login import *

urllib3.disable_warnings()

def downloadSevOneDevicesByParam(fileName, myDevicesUrl, token):
    print("Downloading SevOne Devices url     :  " + myDevicesUrl)
    print("Downloading SevOne Devices to file :  " + fileName)

    headers = { 'Authorization':'Bearer ' + token, 'Accept':'application/json' }
    responseJson = requestsGet(myDevicesUrl, headers)
    writeInFile (fileName, dumps(responseJson))
    print('Download Devices success')


def downloadSevOneDevicesByParamList(outputFolder, paramName, paramValueList, token):
    print("Downloading SevOne Devices for :  " + paramName + " : " .join(paramValueList))

    fileName = outputFolder + "/devices.json"

    myText = ""
    for i in paramValueList:
        myText = myText + "&" + paramName  + "=" + i
    myDevicesUrl = SEVONE_TOPO_DEVICES_URL + "?" + myText

    downloadSevOneDevicesByParam (fileName, myDevicesUrl, token)


def downloadSevOneDevices (outputFolder, TOKEN) :
    printHeading3 (True, "SevOne Devices Download Started ", True)

    ### Download topology
    downloadSevOneDevicesByParamList (outputFolder, "deviceGroupIds", SEVONE_GROUP_IDS, TOKEN)

    printHeading3 (False, "SevOne Devices Download Completed ", True)

