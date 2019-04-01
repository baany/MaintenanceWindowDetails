import json
import string
import requests
import pickle
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def apiCall(Url):
    url = Url
    headers = {'content-type': 'application/json'}
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    r = requests.get(url, verify=False, headers=headers, auth=('XXXX','XXXX'))
    listMaintenance = []
    if (r.status_code == 200):
        resp = json.loads(r.content.decode('utf-8'))
        return (resp)
    else :
        errorMssg = r.status_code
        return (errorMssg)
