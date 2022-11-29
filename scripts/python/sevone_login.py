#!/usr/bin/env python
import sys
import json
import base64
import requests
from json import dumps
import urllib3

from config import *
from common_util import *

urllib3.disable_warnings()

def getSevOneLoginToken():
    printHeading3 (True, "Fetch SevOne Login Token Started ", True)
    print("Login url :  " + SEVONE_LOGIN_URL)

    ### Login
    responseJson = requestsPost(SEVONE_LOGIN_URL, SEVONE_LOGIN_PAYLOAD)

    TOKEN = responseJson['token']
    print('SevOne Login success')        

    printHeading3 (False, "Fetch SevOne Login Token Completed ", True)

    return TOKEN
