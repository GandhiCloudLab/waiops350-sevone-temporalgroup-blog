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
from sevone_events_to_waiops_convert import *

urllib3.disable_warnings()

# Normalized Envets mapping : https://github.ibm.com/katamari/incident-management-data-models/blob/main/models/event/event.schema.yaml

def convertSevOneEventsToNormalizedFormat(sevoneEventsFolder, waiopsEventsFolder):
    printHeading3 (False, "Converting SevOne format to WAIOps Normalized format Started ", True)

    max_events_per_file = int (MAX_NORMALIZED_EVENTS_PER_FILE)
    filesCount = 0
    eventsCount = 0
    firstRecord = True
    # normalizedEventsFileName = waiopsEventsFolder + "/normalized-events.json"

    ### Scan the folder for .json files
    for filename in glob.iglob(os.path.join(sevoneEventsFolder, '**/*.json'), recursive=True):

        ### Open the file
        print("Processing the sevone events file : " + filename)
        f = open(filename)
        data = json.load(f)
        # print("SevOne Events file content : \n " + json.dumps(data))

        if 'alerts' in data and data['alerts'] != None :
            for i in data['alerts']:

                eventsCount = eventsCount + 1

                if (eventsCount % max_events_per_file == 1) :
                    filesCount = filesCount + 1

                normalizedEventsFileName = waiopsEventsFolder + "/normalized-events-" + str(filesCount).zfill(5) + ".json"

                printDebug("...........................")
                printDebug("Event No. : " + str(eventsCount))
                # print("........" + json.dumps(i))
                # print("...........................")

                deviceId = retrieveFromJson2(i, 'device', 'id', '')
                alertType = retrieveFromJson1(i, 'alertType', '')
                messageText = retrieveFromJson1(i, 'messageText', '')
                occurrenceTime = retrieveFromJson1(i, 'startTime', '')
                occurrenceTime = covertEpochToISOFormat(occurrenceTime)

                printDebug("device id : " +  deviceId)
                printDebug("alertType : " + alertType)
                printDebug("messageText : " +  messageText)

                id = uuid.uuid4()
                # deduplicationKey = convertDeDuplicationKey(i)
                summary = messageText
                severity = convertSeverity(i)
                severity = 5
                type = convertType(i)
                sender = convertSender(i)
                resource = convertResource(i)
                details = convertDetails(i)
                links = convertLinks(i)
                cloudevent_meta = convertCloudEventMeta(occurrenceTime)

                expiryseconds = 0  ### 0 minutes

                my_json_string_normalized_alert = {
                        # 'id': str(id), 
                        # 'deduplicationKey': deduplicationKey,
                        'sender': sender,
                        'resource': resource,
                        'type': type,

                        'severity': severity,
                        'summary': summary,
                        'occurrenceTime': occurrenceTime,
                        'expirySeconds': expiryseconds
                }
                    
                my_json_string = json.dumps({
                    'cloudevent_meta' : cloudevent_meta ,
                    'normalized_alert': my_json_string_normalized_alert
                    })

                if (firstRecord) :
                    firstRecord = False
                else :
                    my_json_string = "  \n" + my_json_string

                ## Append the normalized event into the file
                writeInFile(normalizedEventsFileName, my_json_string)

        else :
            print(f"Error : SevOne Events doesn't have data with key : alerts")

        f.close()

    printHeading3 (False, "Converting SevOne format to WAIOps Normalized format Completed ", True)


def convertSevOneEventsToWaiopsFormat(sevoneEventsFolder, waiopsEventsFolder):
    printHeading3 (True, "Converting SevOne format to WAIOps format ", False)

    ### Convert SevOne events into Normalized Events
    convertSevOneEventsToNormalizedFormat(sevoneEventsFolder, waiopsEventsFolder)

