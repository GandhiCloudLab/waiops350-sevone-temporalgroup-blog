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
from sevone_topo_download import *
from sevone_topo_to_file_observer import *
from waiops_file_observer import *
from sevone_devices_download import *

def processOperationTopoAll(workingFolder): 
    printHeading2(True, "SevOne To WAIOps - Topology Process Started ", True)

    ### Folders
    outputFolderTopo = workingFolder + FOLDER_TOPO_SEVONE
    fileObserverFile = workingFolder + FOLDER_TOPO_WAIOPS  + "/" + WAIOPS_TOPO_JOB_FILE_NAME

    ### Get Login Token
    TOKEN = getSevOneLoginToken()

    ### Download topo from sevone
    downloadSevOneTopo (outputFolderTopo, TOKEN)

    ### Folders
    outputFolderTopoDevice = workingFolder + FOLDER_TOPO_SEVONE_DEVICES
    
    ### Download topo from sevone
    downloadSevOneDevices (outputFolderTopoDevice, TOKEN)

    ### Generate WAIOps FileObserver job file
    generateFileObserverJobFile(outputFolderTopo, outputFolderTopoDevice, fileObserverFile)

    ### Upload file to WAIOps FileObserver Job
    uploadFileToFileObserver(fileObserverFile)

    printHeading2(True, "SevOne To WAIOps - Topology Process Completed ", True)


def processOperationTopoDownload(workingFolder): 
    printHeading2(True, "SevOne To WAIOps - Topology Download Process Started ", True)

    ### Get Login Token
    TOKEN = getSevOneLoginToken()

    ### Folders
    outputFolderTopo = workingFolder + FOLDER_TOPO_SEVONE

    ### Download topo from sevone
    downloadSevOneTopo (outputFolderTopo, TOKEN)

    printHeading2(True, "SevOne To WAIOps - Topology Download Process Completed ", True)