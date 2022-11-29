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

link_sevone = []
node_sevone = {}

devices_list = {''}

link_fileobserver = {}
node_fileobserver = {}
result_fileobserver = {}

def processNodeTemplate(id, name):
    myText = WAIOPS_TOPO_TEMPLATE_NODE.replace("###ID###", id)
    myText = myText.replace("###NAME###", name)
    myText = myText.replace("###TYPE###", "node")
    myText = myText.replace("###TAGS###", WAIOPS_TOPO_TAGS)
    return myText

def processLinkTemplate(id):
    myText = WAIOPS_TOPO_TEMPLATE_REF.replace("###ID###", id)
    myText = myText.replace("###EDGE_TYPE###", WAIOPS_TOPO_EDGE_TYPE)
    return myText    

def findNameByDeviceId(myId) : 
    my_json_string = node_sevone[myId]
    myNode = json.loads(my_json_string)
    name = myNode["name"]
    return name

def processLinks():
    print("Creates WAIOps FileObserver Nodes and References from the SevOne Links ")

    for i in link_sevone:
        myLink = json.loads(i)
        fromId = myLink['aDeviceId']
        toId = myLink['zDeviceId']
        
        ## From ID
        myId = fromId
        if not myId in node_fileobserver :
            name = findNameByDeviceId(str(myId))

            myText = processNodeTemplate (str(myId), name)
            keyValue = {myId : myText}
            node_fileobserver.update(keyValue)

        ## To ID
        myId = toId
        if not myId in node_fileobserver :
            name = findNameByDeviceId(str(myId))

            myText = processNodeTemplate (str(myId), name)
            keyValue = {myId : myText}
            node_fileobserver.update(keyValue)

        ## Link
        myText = processLinkTemplate (str(myId))
        if fromId in link_fileobserver :
            myText = link_fileobserver[fromId] + " , " + myText

        keyValue = {fromId : myText}
        link_fileobserver.update(keyValue)


def processNodes():
    print("Creates WAIOps FileObserver Nodes and References from the SevOne Nodes ")
    for i in node_sevone.values() :
        myNode = json.loads(i)
        myId =  myNode['id']
        myIdInt = int(myId)
        if not myIdInt in node_fileobserver :
            name = myNode['name']

            myText = processNodeTemplate (myId, name)
            keyValue = {myIdInt : myText}
            node_fileobserver.update(keyValue)


def processReferences():
    print("Updates the References section of the WAIOps FileObserver Nodes with above created References")
    for deviceId in node_fileobserver:
        myText = node_fileobserver[deviceId]
        refText = ""
        if deviceId in link_fileobserver :
            refText = link_fileobserver[deviceId]
        
        myText = myText.replace("###REF###", refText)

        keyValue = {deviceId : myText}
        result_fileobserver.update(keyValue)


def writeInFileObserverFile(fileObserverFile):
    print("Writes the WAIOps FileObserver Job file content into the file : " + fileObserverFile)

    for myText in result_fileobserver.values():
        writeInFile(fileObserverFile,  "\n")
        writeInFile(fileObserverFile, myText)

    ### Note: 
    ### Need to write atleast \n in the file though there is no record. 
    ### Otherwise file will not be created. With the empty file we can delete the previously created resources in WAIOps.
    writeInFile(fileObserverFile,  "\n")



def copyDevicesFromFilesToArray(topoFilesFolder):
    print("Copy Devices from Topology files to Array ")

    ### Scan the folder for .json files
    for filename in glob.iglob(os.path.join(topoFilesFolder, '**/*.json'), recursive=True):

        ### Open the file
        print("Processing the devices file : " + filename)
        f = open(filename)
        data = json.load(f)

        ### Load Links
        print("Copying links ")
        try:
            for i in data['devices']:
                devices_list.add(i['id'])
        except KeyError:
            print(f"Devices doesn't have data : devices")

        f.close()


def copyLinksAndNodesFromFilesToArray(topoFilesFolder):
    print("Copy Links and Nodes details from Topology files to Array ")


    print("devices list  : " , devices_list)

    ### Scan the folder for .json files
    for filename in glob.iglob(os.path.join(topoFilesFolder, '**/*.json'), recursive=True):

        ### Open the file
        print("Processing the topology file : " + filename)
        f = open(filename)
        data = json.load(f)

        ### Load Links
        print("Copying links ")
        try:
            for i in data['links']:
                if (i['sourceType'] in SEVONE_TOPO_SOURCETYPE) : 
                    if (devices_list.__contains__( str(i['aDeviceId']))) :
                        my_json_string = json.dumps({ 'aDeviceId': i['aDeviceId'], 'zDeviceId': i['zDeviceId'] })
                        link_sevone.append(my_json_string)
                    else:
                        print ("Device doesn't belongs to the device group : " , i['aDeviceId'])
        except KeyError:
            print(f"Topology doesn't have data : links")

        ### Load Nodes
        print("Copying nodes ")
        try:
            for i in data['nodes']:
                my_json_string = json.dumps({ 'id': i['id'], 'name': i['name'] })
                keyValue = {i['id'] : my_json_string}
                node_sevone.update(keyValue)
        except KeyError:
            print(f"Topology doesn't have data : nodes")

        f.close()

def generateFileObserverJobFile(topoFilesFolder, outputFolderTopoDevice, fileObserverFile):
    printHeading3 (True, "Generate File Observer Jobs file from SevOne Topology Started ", True)

    ### Copy devices data from json files to array
    copyDevicesFromFilesToArray(outputFolderTopoDevice)

    ### Copy links and nodes data from json files to array
    copyLinksAndNodesFromFilesToArray(topoFilesFolder)

    ### Process
    processLinks ()
    processNodes ()
    processReferences ()
    writeInFileObserverFile(fileObserverFile)
    printHeading3 (True, "Generate File Observer Jobs file from SevOne Topology Completed ", True)

