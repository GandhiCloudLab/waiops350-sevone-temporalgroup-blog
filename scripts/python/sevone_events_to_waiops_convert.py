#!/usr/bin/env python
import os
import sys
import json
import base64
import requests
import glob
import time

import urllib3
from datetime import datetime
from config import *
import uuid

from common_util import *

urllib3.disable_warnings()



def convertCloudEventMeta(occurrenceTime):
    printDebug ("convertCloudEventMeta .... started")

    ## json string
    my_json_string = {
                    'ce_id': str(uuid.uuid4()), 
                    'ce_time':  occurrenceTime,
                    'ce_source': "SevOne",
                    'content-type': "application/json",
                    'ce_specversion': "1.0"
                    }
    printDebug ("convertCloudEventMeta ....completed")
    return my_json_string

def convertSeverity(sevoneAlert):
    printDebug ("convertSeverity .... started")

    sevoneSeverity = retrieveFromJson1(sevoneAlert, 'severity', "NOTICE")

    result = 5
    if (sevoneSeverity == "NOTICE") : 
        result = 3
    elif (sevoneSeverity == "WARNING"):
        result = 4
    elif (sevoneSeverity == "EMERGENCY"):
        result = 5
    elif (sevoneSeverity == "ERROR"):
        result = 6

    printDebug ("convertSeverity .... completed")
    return result

def convertType(sevoneAlert):
    printDebug ("convertType .... started")
    # print("........" + json.dumps(sevoneAlert))

    classification = retrieveFromJson2(sevoneAlert, 'threshold', 'name', '')
    condition = retrieveFromJson3(sevoneAlert, 'threshold', 'policy', 'name', '')
    type = "SevOne - " + retrieveFromJson1(sevoneAlert, 'alertType', '')
    if (classification == '') :
        classification = type
    if (condition == '') :
        condition = type
    
    result = retrieveFromJson1(sevoneAlert, 'closed', 'false')
    eventType = "problem"
    if (bool(result)) : 
        eventType = "resolution"

    ## json string
    my_json_string = {
                    'classification': classification, 
                    'condition': condition, 
                    'eventType': eventType
                    }

    printDebug ("convertType ....completed : " )
    return my_json_string


def convertDeDuplicationKey(sevoneAlert):
    printDebug ("convertDeDuplicationKey .... started")
    # print("........" + json.dumps(sevoneAlert))

    name = retrieveFromJson2(sevoneAlert, 'device', 'name', '')
    classification = retrieveFromJson2(sevoneAlert, 'threshold', 'name', '')
    condition = retrieveFromJson3(sevoneAlert, 'threshold', 'policy', 'name', '')

    result = name + "-" + classification + "-" + condition + "-"
    printDebug ("convertDeDuplicationKey ....completed : " )
    return result


def convertSender(sevoneAlert):
    printDebug ("convertSender .... started")

    name = retrieveFromJson2(sevoneAlert, 'device', 'name', '')
    service = retrieveFromJson3(sevoneAlert, 'device', 'object', 'name', name)
    type = "SevOne/" + retrieveFromJson1(sevoneAlert, 'alertType', '')

    ## json string
    my_json_string = {
                    'service': service, 
                    'name': name,
                    'type': type
                    }
    printDebug ("convertSender ....completed")
    return my_json_string


def convertResource(sevoneAlert):
    printDebug ("convertResource .... started")

    name = retrieveFromJson2(sevoneAlert, 'device', 'name', '')
    hostname = name
    service = retrieveFromJson3(sevoneAlert, 'device', 'object', 'name', name)

    type1 = retrieveFromJson2(sevoneAlert, 'infoDevice', 'displayName', '')
    type = retrieveFromJson3(sevoneAlert, 'infoObject', 'objectType', 'name', type1)

    ipaddress = retrieveFromJson2(sevoneAlert, 'device', 'ip', '')
    location  = "sevoneloc"

    ## json string
    my_json_string = {
                    'name': name,
                    # 'service': service, 
                    'hostname': hostname,
                    'type': type,
                    'ipaddress': ipaddress,
                    'location': location
                    }

    printDebug ("convertResource .... completed")
    return my_json_string


def convertDetails(sevoneAlert):
    printDebug ("convertDetails .... started")

    id = retrieveFromJson2(sevoneAlert, 'device', 'id', '')
    name = retrieveFromJson2(sevoneAlert, 'device', 'name', '')
    alertType = retrieveFromJson1(sevoneAlert, 'alertType', '')
    messageText = retrieveFromJson1(sevoneAlert, 'messageText', '')

    ## json string
    my_json_string = {
                    'deviceId': id, 
                    'alertType': alertType, 
                    'name': name,
                    'summary': messageText
                    }
    printDebug ("convertDetails .... completed")

    return my_json_string

def convertLinks(sevoneAlert):
    printDebug ("convertLinks .... started")

    ## json string
    my_json_string = {
                    'url': 'http://abc.com', 
                    'linkType': 'webpage',
                    'description':  'mydesc'
                    }
    
    printDebug ("convertLinks .... completed")

    return my_json_string

