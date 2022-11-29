#!/usr/bin/env python
import os
import sys
import json
import base64
import requests
import shutil
import pytz


import urllib3
from datetime import datetime, timedelta

def getBooleanFromEnv(paraName, defaultValue):
    result = defaultValue
    testValue = os.environ.get(paraName)
    if (testValue) :
        if (str(testValue).lower() == "true") : 
            result = True
    return result

def getStringFromEnv(paraName, defaultValue):
    result = defaultValue
    testValue = os.environ.get(paraName)
    if (testValue) :
         result =str(testValue)
    return result

def getArrayFromEnv(paramName):
    result = []
    testValue = os.environ.get(paramName)
    if (testValue) :
        result = testValue.split(",") 
    return result

def getArrayFromEnvWithDefault(paramName, defaultValue):
    result = []
    testValue = os.environ.get(paramName)
    if (testValue) :
        result = testValue.split(",")
    else :
        result = defaultValue.split(",")
    return result    

def generateMainWorkingFolderName():
    date_suffix = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    workingFolder = "sevone-wa-" + date_suffix
    return workingFolder    

def getCurretTimeStamp():
    DATE_SUFFIX = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    return DATE_SUFFIX    

def writeInFile(fileName, fileData):
    with open(fileName, 'a') as output_file:
        output_file.write(fileData)

#### Others
LOG_DEBUG_FLAG = getBooleanFromEnv('LOG_DEBUG', False)

def printDebug(msg) : 
    if (LOG_DEBUG_FLAG) :
        print (msg)


def retrieveFromJson1 (jsonObject, key1, defaultValue):
    result = defaultValue

    if key1 in jsonObject :
         result = jsonObject[key1]
    
    return result

def retrieveFromJson2 (jsonObject, key1, key2, defaultValue):
    result = defaultValue

    if key1 in jsonObject and jsonObject[key1] != None :
        if key2 in jsonObject[key1] :
             result = jsonObject[key1][key2]
    
    return result

def retrieveFromJson3 (jsonObject, key1, key2, key3, defaultValue):
    result = defaultValue

    if key1 in jsonObject and jsonObject[key1] != None :
        if key2 in jsonObject[key1] and jsonObject[key1][key2] != None:
            if key3 in jsonObject[key1][key2] :
                result = jsonObject[key1][key2][key3]
    
    return result

def covertEpochToISOFormat(epochTime):
    datetime1 = datetime.fromtimestamp(int(epochTime))
    dateTimeString = datetime1.isoformat()[:-3]+'Z'
    # print ("epochTime : " + epochTime +  " ----  dateTimeString : " + dateTimeString)
    return dateTimeString  

def deleteFolder (folderPath):
    shutil.rmtree(folderPath, ignore_errors=True, onerror=None)

def deleteAndCreateFolder (folderPath):
    deleteFolder(folderPath)
    os.makedirs(folderPath)

def copyFolder (sourceFolder, destinationFolder):
    shutil.copytree(sourceFolder, destinationFolder)

def copyFile (sourceFolder, destinationFolder):
    shutil.copyfile(sourceFolder, destinationFolder)    

def printHeading1 (flagTop, msg, flagBottom) :
    if (flagTop) :
        print("****************************************************************************************************")
    if (msg != None) :
        print (msg)
    if (flagBottom) :
        print("****************************************************************************************************")

def printHeading2 (flagTop, msg, flagBottom) :
    if (flagTop) :
        print("======================================================================")
    if (msg != None) :
        print (msg)
    if (flagBottom) :
        print("======================================================================")

def printHeading3 (flagTop, msg, flagBottom) :
    if (flagTop) :
        print("--------------------------------------------------")
    if (msg != None) :
        print (msg)
    if (flagBottom) :
        print("--------------------------------------------------")

def printHeading4 (flagTop, msg, flagBottom) :
    if (flagTop) :
        print(".........................")
    if (msg != None) :
        print (msg)
    if (flagBottom) :
        print(".........................")

def printSeparator4 () :
    print(".....")


def exitWithError (myUrl) :
    print("######################")
    print('Error Occured while calling the URL : ', myUrl)
    print('Program exits ')
    print("######################")
    sys.exit()


def requestsGet (myUrl, headersInfo) :
    printDebug("Requests GET URL : " + myUrl)

    response= requests.get(myUrl, verify=False, headers=headersInfo)

    print("Response status_code : ", response.status_code)
    printDebug("Download response  : " + response.text)

    if (response.status_code >= 200 and response.status_code < 300) :
        responseJson = response.json()
        return responseJson
    else:
        exitWithError(myUrl)

def requestsPost (myUrl, jsonObject) :
    printDebug("Requests POST URL : " + myUrl)

    headersInfo = { "Content-Type" : "application/json", "Accept" : "application/json"  }

    try: 
        response = requests.post(myUrl, headers=headersInfo, json=jsonObject, verify=False)
        print("Response status_code : ", response.status_code)
        printDebug("Download response  : " + response.text)

        if (response.status_code >= 200 and response.status_code < 300) :
            responseJson = response.json()
            return responseJson
        else:
            exitWithError(myUrl)
    except:
        exitWithError(myUrl)

def requestsPostFile (myUrl, headersInfo, filesIn) :
    printDebug("Requests POST File URL : " + myUrl)

    try: 
        response = requests.post(myUrl, headers=headersInfo, files=filesIn, verify=False)

        print("Response status_code : ", response.status_code)
        print("Response : " + response.text)
    except:
        exitWithError(myUrl)

def requestsPutFile (myUrl, headersInfo, filesIn) :
    printDebug("Requests PUT File URL : " + myUrl)

    try: 
        response = requests.put(myUrl, headers=headersInfo, files=filesIn, verify=False)

        print("Response status_code : ", response.status_code)
        print("Response : " + response.text)
    except:
        exitWithError(myUrl)        

def requestsPostFile (myUrl, headersInfo, filesIn) :
    printDebug("Requests POST URL : " + myUrl)

    try: 
        response = requests.post(myUrl, headers=headersInfo, files=filesIn, verify=False)

        print("Response status_code : ", response.status_code)
        print("Response : " + response.text)
    except:
        exitWithError(myUrl)        


