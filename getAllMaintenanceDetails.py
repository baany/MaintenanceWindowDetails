import json
import os
import ast
import string
import requests
import pickle
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
    urlCheckMaintenanceBase = "XXXX"
    urlCheckMaintenanceTail = "XXXX"
    for item in maintenanceList:
        if (item > flag):
            flag = item
            url = urlCheckMaintenanceBase+str(item)+urlCheckMaintenanceTail
            resp = apiCall(url)
            auditFlatFileConsole(resp)
        else :
            pass
    updateFlag(flag)
    return ()
auditMaintenanceConsole()
