#!/usr/bin/env python
import os
import sys
import json
import base64
import requests

import urllib3
from datetime import datetime

from common_util import *

################################# External Parameters #################################

#### SevOne - Access Parameters
SEVONE_URL = os.environ.get('SEVONE_URL', '')
SEVONE_USER = os.environ.get('SEVONE_USER', '')
SEVONE_PWD = os.environ.get('SEVONE_PWD', '')

#### WAIOps Topology - Access Parameters
WAIOPS_TOPO_URL = os.environ.get('WAIOPS_TOPO_URL', '')
WAIOPS_TOPO_USER = os.environ.get('WAIOPS_TOPO_USER', '')
WAIOPS_TOPO_PWD = os.environ.get('WAIOPS_TOPO_PWD', '')
WAIOPS_TOPO_TENENT_ID = os.environ.get('WAIOPS_TOPO_TENENT_ID', '')

#### SevOne - Topology Filter Parameters
SEVONE_DEVICE_IDS = getArrayFromEnv('SEVONE_DEVICE_IDS')
SEVONE_TOPO_HOPS = getStringFromEnv('SEVONE_TOPO_HOPS', '1')
SEVONE_GROUP_IDS = getArrayFromEnv('SEVONE_GROUP_IDS')

#### SevOne - Topology Filter Secondary Parameters 
SEVONE_DEVICE_NAMES = getArrayFromEnv('SEVONE_DEVICE_NAMES')
SEVONE_SOURCE_IDS = getArrayFromEnv('SEVONE_SOURCE_IDS')

#### Event History - Parameters
SEVONE_EVENT_HISTORY_DAYS = os.environ.get('SEVONE_EVENT_HISTORY_DAYS', 2)
MAX_NORMALIZED_EVENTS_PER_FILE = os.environ.get('MAX_NORMALIZED_EVENTS_PER_FILE', 500)

#### WAIOps Topology File Observer Job Parameters
WAIOPS_TOPO_JOB_ID = os.environ.get('WAIOPS_TOPO_JOB_ID', 'filejob1')
WAIOPS_TOPO_JOB_FILE_NAME = os.environ.get('WAIOPS_TOPO_JOB_FILE_NAME', 'filejob1.txt')
WAIOPS_TOPO_JOB_PROVIDER = os.environ.get('WAIOPS_TOPO_JOB_PROVIDER', 'filejob1')
WAIOPS_TOPO_JOB_DATA_CENTER = os.environ.get('WAIOPS_TOPO_JOB_DATA_CENTER', 'filejob1-dc')

#### Debug Log (true/false)
LOG_DEBUG = os.environ.get('LOG_DEBUG', "false")

#### Folders
INPUT_FOLDER_ROOT = os.environ.get('INPUT_FOLDER', '../../data/input/')
OUTPUT_FOLDER_ROOT = os.environ.get('OUTPUT_FOLDER', '../../data/output/')

#### Operations Type (TopoDownload,TopoAll,EventsHistoryDownload, EventsHistoryAll)
OPERATION_TYPE = os.environ.get('OPERATION_TYPE', 'TopoDownload')

################################# Internal Parameters #################################

#### SevOne URLS
SEVONE_LOGIN_URL = SEVONE_URL + "/api/v3/users/signin"
SEVONE_TOPO_URL = SEVONE_URL + "/api/v3/data/topology/graph"
SEVONE_EVENTS_URL = SEVONE_URL + "/api/v3/data/alerts"
SEVONE_TOPO_DEVICES_URL = SEVONE_URL + "/api/v3/metadata/devices"

#### SevOne Params
SEVONE_LOGIN_PAYLOAD = {  "username" : SEVONE_USER, "password": SEVONE_PWD }
SEVONE_TOPO_SOURCETYPE = ["Logical","Physical","Session"]

#### WAIOps File Observer
WAIOPS_TOPO_EDGE_TYPE = "uses"
WAIOPS_TOPO_TAGS = "sevone"
WAIOPS_TOPO_TEMPLATE_NODE="V:{\"_operation\":\"InsertReplace\", \"uniqueId\":\"###ID###\", \"entityTypes\":[\"###TYPE###\"],\"matchTokens\":[\"###ID###\", \"###NAME###\"],\"name\":\"###NAME###\", \"tags\":[\"###TAGS###\"], \"_references\":[###REF###]}"
WAIOPS_TOPO_TEMPLATE_REF="{\"_edgeType\" : \"###EDGE_TYPE###\", \"_toUniqueId\" : \"###ID###\"}"

#### WAIOps File Observer - Upload Type (POST,PUT,BOTH)
WAIOPS_TOPO_UPLOAD_TYPE = "BOTH"

#### Folders
FOLDER_EVENTS_WAIOPS = "/events-history/waiops"
FOLDER_EVENTS_SEVONE = "/events-history/sevone"
FOLDER_TOPO_WAIOPS = "/topology/waiops"
FOLDER_TOPO_SEVONE = "/topology/sevone"
FOLDER_TOPO_SEVONE_DEVICES = "/topology/sevone-devices"

#### SevOne Alert Type to download - (SYSTEM,TRAP,ALL)
SEVONE_ALERT_TYPE = "SYSTEM"
