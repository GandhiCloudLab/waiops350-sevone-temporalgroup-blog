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


def downloadSevOneTopoByParam(fileName, myTopoUrl, token):
    print("Downloading SevOne Topology url     :  " + myTopoUrl)
    print("Downloading SevOne Topology to file :  " + fileName)

    headers = { 'Authorization':'Bearer ' + token, 'Accept':'application/json' }
    responseJson = requestsGet(myTopoUrl, headers)
    writeInFile (fileName, dumps(responseJson))
    print('Download topology success')

def downloadSevOneTopoByParamValue(outputFolder, paramName, paramValue, token):
    print("Downloading SevOne Topology for :  " + paramName + " : " + paramValue)

    fileName = outputFolder + "/" + paramName + "-" + paramValue +  ".json"
    myTopoUrl = SEVONE_TOPO_URL + "?hops=" + SEVONE_TOPO_HOPS + "&" + paramName  + "=" + paramValue

    downloadSevOneTopoByParam (fileName, myTopoUrl, token)


def downloadSevOneTopoByParamList(outputFolder, paramName, paramValueList, token):
    print("Downloading SevOne Topology for :  " + paramName + " : " .join(paramValueList))

    fileName = outputFolder + "/" + paramName +  ".json"

    myText = ""
    for i in paramValueList:
        myText = myText + "&" + paramName  + "=" + i
    # myTopoUrl = SEVONE_TOPO_URL + "?hops=" + SEVONE_TOPO_HOPS + myText
    myTopoUrl = SEVONE_TOPO_URL + "?hops=" + SEVONE_TOPO_HOPS + myText

    downloadSevOneTopoByParam (fileName, myTopoUrl, token)


def downloadSevOneTopo (outputFolder, TOKEN)  :
    printHeading3 (True, "SevOne Topology Download Started ", True)

    ### Download topology
    for i in SEVONE_DEVICE_IDS:
        downloadSevOneTopoByParamValue (outputFolder, "deviceId", i, TOKEN)
    for i in SEVONE_DEVICE_NAMES:
        downloadSevOneTopoByParamValue (outputFolder, "deviceName", i, TOKEN)
    downloadSevOneTopoByParamList (outputFolder, "deviceGroupIds", SEVONE_GROUP_IDS, TOKEN)
    downloadSevOneTopoByParamList (outputFolder, "sourceIds", SEVONE_SOURCE_IDS, TOKEN)

    printHeading3 (False, "SevOne Topology Download Completed ", True)

