#!/usr/bin/env python3

import json
import os
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
    #print (len(resp['windows']))
    #return (resp['windows'][2]['id'])
    for i in range(len(resp['windows'])):
        listMaintenance.append(resp['windows'][i]['id'])
        #print (resp['windows'][i])
    #return(listMaintenance)
    return (sorted(listMaintenance))

def auditFlatFileConsole(workDone):
    currentDatetime = date.today()
    #fileOpen = open("SelfServiceLogs_"+str(currentDatetime)+'.txt', 'a+')
    fileOpen = open("Console_Moogsoft.txt", 'a+')
    fileOpen.write("#####################################################\r\n")
    fileOpen.write(str(workDone)+"\r\n")
    fileOpen.close()

def updateFlag(value):
    with open('flagMaintenanceID', 'wb') as f:
        flag = pickle.dump(value, f)
    return ()

##def getFlag():
##    with open('flagMaintenanceID', 'rb') as f:
##        flag = pickle.load(f)
##    return (flag)

def getFlag():
    if os.path.isfile('flagMaintenanceID'):
        with open('flagMaintenanceID', 'rb') as f:
            try:
                return (pickle.load(f))
            except Exception:
                pass 
    with open('flagMaintenanceID', 'wb') as f:
        pickle.dump(0, f)
    return (0)

def auditMaintenanceConsole():
    maintenanceList = getMaintenanceList()
    print (maintenanceList)
    lengthListMaintenance = len(maintenanceList)
    flag = getFlag()
    print (flag)
    #print (lengthListMaintenance)
    #print (maintenanceList[lengthListMaintenance-1])
    urlMaintenanceBase = "XXXX"
    urlMaintenanceTail = "XXXX"
    for item in maintenanceList:
        if (item > flag):
            flag = item
            url = urlMaintenanceBase+str(item)+urlMaintenanceTail
            resp = apiCall(url)
            auditFlatFileConsole(resp)
        else :
            pass
    updateFlag(flag)
    return ()

#auditMaintenanceConsole()

def extractValues(jsonObj, key):
    """Pull all values of specified key from nested JSON."""
    resultList = []
    def extract(jsonObj, resultList, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(jsonObj, dict):
            for k, v in jsonObj.items():
                if isinstance(v, (dict, list)):
                    extract(v, resultList, key)
                elif k == key:
                    resultList.append(v)
        elif isinstance(jsonObj, list):
            for item in jsonObj:
                extract(item, resultList, key)
        return (resultList)

    result = extract(jsonObj, resultList, key)
    return (result)

def windowParser():
    flagVal = getFlag()
    urlMaintenanceBase = "XXXX"
    urlMaintenanceTail = "XXXX"
    url = urlMaintenanceBase+str(flagVal)+urlMaintenanceTail
    resp = apiCall(url)
    print (resp)
    print ('##############################################################')
    #print (resp['windows'][0]['filter'])
    hostList = []
    nameWindow = resp['windows'][0]['name']
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
    print ("Name : ", nameWindow)
    #print (valueList)
    #print (columnList)
    for num in range(0,len(valueList)-1):
        hostList.append(valueList[num])
    teamName = valueList[len(valueList)-1]
    print ("Host List :", hostList)
    print ("Team : ", teamName)
    print ("Start Time : ", startTimeFormatted)
    print ("Duration : ", windowDuration)
    print ("Window ID : ", windowID)
    print ("Last Updated Time", lastUpdatedTimeFormatted)
    return ()

#auditMaintenanceConsole()
windowParser()
