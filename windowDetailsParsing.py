#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import ast
import string
import requests
import pickle
import cx_Oracle
import dpath.util
import time
from datetime import datetime
from datetime import date
from makeAPICall import apiCall
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def getMaintenanceList():
    url = 'XXXX'
    resp = apiCall(url)
    listMaintenance = []
    #return (resp['windows'][2]['id'])
    for i in range(len(resp['windows'])):
        listMaintenance.append(resp['windows'][i]['id'])
        #print (resp['windows'][i])
    return (sorted(listMaintenance))

def auditFlatFileConsole(workDone):
    currentDatetime = date.today()
    fileOpen = open("ConsoleDataPush.txt", 'a+')
    fileOpen.write(str(workDone)+"\r\n")
    fileOpen.close()
    return()

def updateFlag(value):
    with open('flagMaintenanceID', 'wb') as f:
        flag = pickle.dump(value, f)
    return ()

def getFlag():
    if os.path.isfile('flagMaintenanceID'):
        with open('flagMaintenanceID', 'rb') as f:
            try:
                return (pickle.load(f))
            except Exception:
                pass
    with open('flagMaintenanceID', 'wb') as f:
        pickle.dump(0, f)
        return (pickle.load(f))

def extractValues(jsonObj, key):
    """Pull all values of specified key from nested JSON."""
    resultList = []
    def extract(jsonObj, resultList, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(jsonObj, dict):
            for k, v in jsonObj.items():
                if isinstance(v, dict):
                    extract(v, resultList, key)
                elif k == key:
                    resultList.append(v)
        elif isinstance(jsonObj, list):
            for item in jsonObj:
                extract(item, resultList, key)
        return (resultList)

    result = extract(jsonObj, resultList, key)
    return (result)

def duplicates(columnList,key):
    return ([i for i, x in enumerate(columnList) if x == key])

def windowParser():
    #flagVal = getFlag()
    flagVal = 970
    urlMaintenanceBase = "XXXX"
    urlMaintenanceTail = "XXXX"
    url = urlMaintenanceBase+str(flagVal)+urlMaintenanceTail
    resp = apiCall(url)
    print (resp)
    #print ('##############################################################')
    #print (resp['windows'][0]['filter'])
    maintenanceWindowDetails = {}
    #print (resp['windows'])
    nameWindow = resp['windows'][0]['name']
    descriptionWindow = resp['windows'][0]['description']
    updatedBy = resp['windows'][0]['updated_by']
    valueList = extractValues(json.loads(resp['windows'][0]['filter']), 'value')
    columnList = extractValues(json.loads(resp['windows'][0]['filter']), 'column')
    windowDurationSeconds = resp['windows'][0]['duration']
    windowDuration = time.strftime("%H:%M:%S", time.gmtime(windowDurationSeconds))
    windowID = resp['windows'][0]['id']
            ##Time conversion - START##
    lastUpdatedTime = resp['windows'][0]['last_updated']
    startTime = resp['windows'][0]['start_date_time']
    startTimeFormatted = datetime.utcfromtimestamp(int(startTime)).strftime('%Y-%m-%d %H:%M:%S')
    lastUpdatedTimeFormatted = datetime.utcfromtimestamp(int(lastUpdatedTime)).strftime('%Y-%m-%d %H:%M:%S')
            ##Time conversion - END##
    #print ('##############################################################')
##    print ('##############################################################')
##    print (valueList)
##    print (columnList)
##    print ('##############################################################')
    hostIndexList = []
    teamIndexList = []
    textPatternIndexList = []
    teamNameList = []
    textPatternList = []
    hostList = []
    managerList = []
    agentList = []
    hostIndexList = duplicates(columnList, 'source')
    teamIndexList = duplicates(columnList, 'custom_info.Team')
    textPatternIndexList = duplicates(columnList, 'description')
    managerIndexList = duplicates(columnList, 'manager')
    agentIndexList = duplicates(columnList, 'agent')
    #print (teamIndexList)
    #print (textPatternIndexList)
    #print (hostIndexList)
    #print (managerIndexList)
    #print (agentIndexList)
    if (teamIndexList):
        for item in teamIndexList:
            teamNameList.append(valueList[item])
    if (textPatternIndexList):
        for item in textPatternIndexList:
            textPatternList.append(valueList[item])
    if (hostIndexList):
        for item in hostIndexList:
            hostList.append(valueList[item])
    if (managerIndexList):
        for item in managerIndexList:
            managerList.append(valueList[item])
    if (agentIndexList):
        for item in agentIndexList:
            agentList.append(valueList[item])
    print ("Name : ", nameWindow)
    print ("Description : ", descriptionWindow)
    print ("Updated by : ", updatedBy)
    print ("Host List :", hostList)
    print ("Team : ", teamNameList)
    print ("TextPattern : ", textPatternList)
    print ("Manager : ", managerList)
    print ("Agent : ", agentList)
    print ("Start Time : ", startTimeFormatted)
    print ("Duration : ", windowDuration)
    print ("Window ID : ", windowID)
    print ("Last Updated Time", lastUpdatedTimeFormatted)
    print ('##############################################################')
    maintenanceWindowDetails.update({"Name":nameWindow, "Description":descriptionWindow, "HostList":hostList, "Team":teamNameList, "Description":textPatternList, "Manager":managerList, "Agent": agentList, "StartTime":startTimeFormatted, "Duration":windowDuration, "Window ID":windowID, "LastUpdatedTime":lastUpdatedTimeFormatted, "UpdatedBy":updatedBy})
    print (maintenanceWindowDetails)
    print ('##############################################################')
    return ()

#updateFlag(968)
windowParser()
