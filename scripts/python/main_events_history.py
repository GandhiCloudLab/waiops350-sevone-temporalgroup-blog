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
from sevone_events_to_waiops import *
from sevone_events_history import *
from sevone_events_history_download import *

def processOperationEventsHistoryAll(workingFolder): 
    printHeading2(True, "SevOne To WAIOps - Events History Process Started ", True)

    ### Folders
    sevoneEventsFolder = workingFolder + FOLDER_EVENTS_SEVONE
    waiopsEventsFolder = workingFolder + FOLDER_EVENTS_WAIOPS

    ### Download SevOne Events History
    downloadSevoneEvents(sevoneEventsFolder)

    ### Convert SevOne to WAIops format
    convertSevOneEventsToWaiopsFormat(sevoneEventsFolder, waiopsEventsFolder)

    ### Copy sevone and waiops files to input folder for further processing (upload to waiops, training)
    copyEventsToInputFolder(sevoneEventsFolder, waiopsEventsFolder)

    printHeading2(True, "SevOne To WAIOps - Events History Process Completed ", True)


def processOperationEventsHistoryDownload(workingFolder): 
    printHeading2(True, "SevOne To WAIOps - Events History Download Process Started ", True)

    ### Folders
    sevoneEventsFolder = workingFolder + FOLDER_EVENTS_SEVONE

    ### Download SevOne Events History
    downloadSevoneEvents(sevoneEventsFolder)

    printHeading2(True, "SevOne To WAIOps - Events History Download Process Completed ", True)

