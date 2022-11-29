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
from sevone_login import *

urllib3.disable_warnings()

def downloadSevoneEventsAndStoreInFolder(outputFolder, token):
    no_of_days = int(SEVONE_EVENT_HISTORY_DAYS)
    past_date = datetime.now() - timedelta(days = no_of_days)
    start_date = datetime(past_date.year, past_date.month, past_date.day, 0, 0, 0)
    # start_date = start_date.astimezone(pytz.UTC)
    printHeading4(False, "Download Event History - No of Days  : " + str(no_of_days), False)
    printHeading4(False, "Download Event History - Start Date  : "+ start_date.strftime('%Y-%m-%d-%H-%M-%S'), True)

    milliSecondsPerDay = (24 * 86400000) - 1

    ### Iterate for each day
    for i in range(0, no_of_days, 1):
        my_date1 = start_date + timedelta(days = i)
        my_date_epoc1 = my_date1.strftime('%s')
        # print('date:', str(my_date1) + '   -->  date epoc:' + str(my_date_epoc1))

        my_date2 = start_date + timedelta(days = i) + timedelta(milliseconds= milliSecondsPerDay)
        my_date_epoc2 = my_date2.strftime('%s')
        # print('date  2:', str(my_date2) + '   -->  date epoc:' + str(my_date_epoc2))

        fileSuffix = my_date1.strftime('%Y-%m-%d-%H-%M-%S') + "---" + my_date2.strftime('%Y-%m-%d-%H-%M-%S')

        downloadSevoneEventsAndStoreInFolderDayily(outputFolder, token, fileSuffix, my_date_epoc1, my_date_epoc2)


def downloadSevoneEventsAndStoreInFolderDayily(outputFolder, token, fileSuffix, statTime, endTime):
    fileName = outputFolder + "/sevone-events-" + fileSuffix + ".json"

    # myEventsUrl = SEVONE_EVENTS_URL + "?query.alertStatus=OPEN&query.alertType=UNKNOWN"
    # queryString = "?query.alertStatus=BOTH"

    queryString = "?"
    queryString = queryString + "query.timeRange.specificInterval.startTime=" + statTime
    queryString = queryString + "&query.timeRange.specificInterval.endTime=" + endTime
    if (SEVONE_ALERT_TYPE == "SYSTEM") : 
        queryString = queryString + "&query.alertType=SYSTEM"
    elif (SEVONE_ALERT_TYPE == "TRAP"):
        queryString = queryString + "&query.alertType=TRAP"
    myEventsUrl = SEVONE_EVENTS_URL + queryString

    print("SevOne Url query str :  " + queryString)
    print("Event stored in File :  " + fileName)
    print(".....")

    headers = { 'Authorization':'Bearer ' + token, 'Accept':'application/json' }
    responseJson = requestsGet(myEventsUrl, headers)
    writeInFile (fileName, dumps(responseJson))
    print('Download Events History - Success')


def downloadSevoneEvents (outputFolder) :
    printHeading3(False, "Download SevOne Events History ", True)

    ### Get Login Token
    TOKEN = getSevOneLoginToken()

    ### Download
    downloadSevoneEventsAndStoreInFolder (outputFolder,  TOKEN)