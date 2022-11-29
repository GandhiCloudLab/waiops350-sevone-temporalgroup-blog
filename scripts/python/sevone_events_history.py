#!/usr/bin/env python
import os
import sys
import json
import base64
import requests
import glob

import urllib3
from datetime import datetime

from config import *
from common_util import *

urllib3.disable_warnings()

def copyEventsToInputFolder(sevoneEventsFolder, waiopsEventsFolder):
    printHeading3 (True, "Copying Events History files to Input Folder ", True)

    print ("Sevone Events Source Folder : " + sevoneEventsFolder)
    print ("Waiops Events Source Folder : " + waiopsEventsFolder)

    ### Folders
    inputFolderSevOne = INPUT_FOLDER_ROOT + FOLDER_EVENTS_SEVONE
    inputFolderWaiops = INPUT_FOLDER_ROOT + FOLDER_EVENTS_WAIOPS

    print ("Sevone Events Destination Folder : " + inputFolderSevOne)
    print ("Waiops Events Destination Folder : " + inputFolderWaiops)

    ### Delete existing folders
    deleteFolder (inputFolderSevOne)
    deleteFolder (inputFolderWaiops)

    ### Copy the result
    copyFolder(sevoneEventsFolder, inputFolderSevOne)
    copyFolder(waiopsEventsFolder, inputFolderWaiops)
