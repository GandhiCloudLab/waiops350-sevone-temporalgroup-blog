#!/usr/bin/env python
import os
import sys
import json
import base64
import requests

import urllib3
from datetime import datetime

from config import *
from common_util import *
from main_events_history import *
from main_topology import *

# urllib3.disable_warnings()

def createWorkingFolders(workingFolder):
    os.makedirs(workingFolder + FOLDER_EVENTS_WAIOPS)
    os.makedirs(workingFolder + FOLDER_EVENTS_SEVONE)
    os.makedirs(workingFolder + FOLDER_TOPO_WAIOPS)
    os.makedirs(workingFolder + FOLDER_TOPO_SEVONE)
    os.makedirs(workingFolder + FOLDER_TOPO_SEVONE_DEVICES)


def printKeyParameters(): 
    printHeading3(True, "Key Parameters ", True)
    print(" Operation Type           : ", OPERATION_TYPE)
    print(" Topology Device Ids      : ", SEVONE_DEVICE_IDS)
    print(" Topology Hops            : ", SEVONE_TOPO_HOPS)
    print(" Topology Group Ids       : ", SEVONE_GROUP_IDS)
    # print(" Topology Source Ids      : ", SEVONE_SOURCE_IDS)
    # print(" Topology Device Names    : ", SEVONE_DEVICE_NAMES)
    print(" File Observer JobId      : ", WAIOPS_TOPO_JOB_ID)
    print(" File Observer FileName   : ", WAIOPS_TOPO_JOB_FILE_NAME)
    print(" File Observer Provider   : ", WAIOPS_TOPO_JOB_PROVIDER)
    printHeading3(False, None, True)

def myMain(): 
    printHeading1(True, "SevOne To WAIOps Process Started ", True)

    ### Create Working folders
    workingFolder = OUTPUT_FOLDER_ROOT + generateMainWorkingFolderName()
    createWorkingFolders(workingFolder)
    
    ### Print parameters from config
    printKeyParameters()

    ### Do Operation
    if (OPERATION_TYPE == "TopoDownload") : 
        processOperationTopoDownload (workingFolder)
    elif (OPERATION_TYPE == "TopoAll"):
        processOperationTopoAll (workingFolder)
    elif (OPERATION_TYPE == "EventsHistoryDownload"):
        processOperationEventsHistoryDownload (workingFolder)
    elif (OPERATION_TYPE == "EventsHistoryAll"):
        # printTimes()
        processOperationEventsHistoryAll(workingFolder)
    else :
        print ("Invalid Operation Type : " + OPERATION_TYPE)

    printHeading1(True, "SevOne To WAIOps Process Completed ", True)

myMain()