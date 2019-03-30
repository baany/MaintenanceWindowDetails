import json
import os
import ast
import string
import requests
import pickle
from datetime import datetime
from datetime import date
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def apiCall():
    url = 'XXXX'
    headers = {'content-type': 'application/json'}
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    r = requests.get(url, verify=False, headers=headers, auth=('XXXX','XXXX'))
    listMaintenance = []
    if (r.status_code == 200):
        resp = json.loads(r.content.decode('utf-8'))
        #print (len(resp['windows']))
        #return (resp['windows'][2]['id'])
        for i in range(len(resp['windows'])):
            listMaintenance.append(resp['windows'][i]['id'])
            #print (resp['windows'][i])
        #return(listMaintenance)
        return (sorted(listMaintenance))
    else :
        errorMssg = r.status_code
        return (errorMssg)
    

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
    maintenanceList = apiCall()
    print (maintenanceList)
    lengthListMaintenance = len(maintenanceList)
    flag = getFlag()
    print (flag)
    #print (lengthListMaintenance)
    #print (maintenanceList[lengthListMaintenance-1])
    urlCheckMaintenanceBase = "XXXX"
    urlCheckMaintenanceTail = "XXXX"
    #return ()
    for item in maintenanceList:
        if (item > flag):
            flag = item
            url = urlCheckMaintenanceBase+str(item)+urlCheckMaintenanceTail
            headers = {'content-type': 'application/json'}
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            r = requests.get(url, verify=False, headers=headers, auth=('XXXX','XXXX'))
            if (r.status_code == 200):
                resp = json.loads(r.content.decode('utf-8'))
                auditFlatFileConsole(resp)
            else :
                errorMssg = r.status_code
                print (errorMssg)
        else :
            pass
    updateFlag(flag)
    return ()

auditMaintenanceConsole()
