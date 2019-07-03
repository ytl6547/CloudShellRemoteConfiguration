import subprocess
import socket

from django.http import HttpResponse
from django.views.generic import TemplateView
from WebTerm.models import Device
from datetime import datetime, timezone
from django.core.serializers.json import DjangoJSONEncoder

# from djongo import database
# import asyncio
# from channels.consumer import AsyncConsumer
# import time
# import websockets
import requests
import json

session = requests.Session()
Cookies = {}
device_list = []

# login_url = "https://172.27.250.16/api/system/v1/auth/login"
# check_device_url = "https://172.27.250.16/api/rdm/v1/device"
login_url = "https://172.23.165.148/api/system/v1/auth/login"
check_device_url = "https://172.23.165.148/api/rdm/v1/device"
username = ''
password = ''
CORRECT_USERNAME = 'admin'
CORRECT_PASSWORD = 'Maglev123'

clientPassword = "Cisco"
clientUsername = "Cisco"
clientIP = "40.0.0.10"
timeout_sec = "1200"

logged_in = False


# proxies = {
#   'http': 'http://172.27.250.16:443',
#   'https': 'http://172.27.250.16:443'
# }


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def parse_dict_cookies(value):
    result = {}
    for item in value.split(';'):
        item = item.strip()
        if not item:
            continue
        if '=' not in item:
            result[item] = None
            continue
        name, value = item.split('=', 1)
        result[name] = value
    return result


def loginToDNAC():
    print("login to DNAC")
    global Cookies
    global logged_in
    response = session.get(login_url, auth=(username, password), verify=False)
    print(response.status_code)
    if response.status_code != 200:
        print("login failed")
        response = session.get(login_url, auth=(CORRECT_USERNAME, CORRECT_PASSWORD), verify=False)

        Cookies = parse_dict_cookies(response.headers['Set-Cookie'])
        print(Cookies)
        logged_in = False
        print(logged_in)
        return False

    Cookies = parse_dict_cookies(response.headers['Set-Cookie'])
    print(Cookies)
    logged_in = True
    print(logged_in)
    return True


def getDevices():
    print("get devices")
    global device_list
    if Cookies == {}:
        loginToDNAC()

    r = session.get(check_device_url, cookies=Cookies, verify=False)
    if r.status_code != 200:
        loginToDNAC()
        r = session.get(check_device_url, cookies=Cookies, verify=False)
    print(r.status_code)
    device_list = json.loads(r.text)
    print(device_list)

    filtered_device_list = []
    for device in device_list:
        if device['connectionState']['state'] == "CONNECTED":
            filtered_device_list.append(device)
    device_list = filtered_device_list
    return json.dumps(device_list)


def login(request):
    global username, password
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username, password)
    return HttpResponse(loginToDNAC())


class ReturnValue():
    def __init__(self, pending=True, last_access_time=None, port=None, authenticated=True):
        self.port = port
        self.lastAccessTime = last_access_time
        self.pending = pending
        self.authenticated = authenticated


def terminal(request):
    global clientIP
    if not logged_in:
        r = ReturnValue()
        r.authenticated = False
        return HttpResponse(json.dumps(r.__dict__, cls=DjangoJSONEncoder), content_type="application/json")

    DeviceId = request.GET.get('DeviceId', "")

    # check whether device status is PENDING
    getDevices()
    for device in device_list:
        if device["deviceId"] == DeviceId:
            if device["connectionState"]["state"] == "PENDING":
                return HttpResponse(json.dumps(ReturnValue().__dict__, cls=DjangoJSONEncoder),
                                    content_type="application/json")
            clientIP = device["ipAddr"]
            break

    # Query the database
    try:
        d = Device.objects.get(id=DeviceId)
        print(d.id)
        print(d.lastAccessTime)
        if (datetime.now(timezone.utc) - d.lastAccessTime).total_seconds() < 1200:  # using by others
            # return not pending and the access time of others
            # print((datetime.now(timezone.utc) - d.lastAccessTime).total_seconds())
            print("now:", datetime.now(timezone.utc))
            print("last: ", d.lastAccessTime)
            return HttpResponse(json.dumps(ReturnValue(False, d.lastAccessTime).__dict__, cls=DjangoJSONEncoder),
                                content_type="application/json")
    # except Device.DoesNotExist:  # not accessed by any one
    #     d = Device(id=DeviceId)
    except:
        d = Device(id=DeviceId)
    # else:
    #     d = Device(id=DeviceId)

    # get the password

    # prepare commands and ports
    port_to_host_terminal = str(get_open_port())
    pre_entered_command = "sshpass -p " + clientPassword + " ssh " + clientUsername + "@" + clientIP
    command = "timeout " + timeout_sec + " ttyd -o -p " + port_to_host_terminal + " " + pre_entered_command

    # start the timer
    d.lastAccessTime = datetime.now(timezone.utc)

    # do it!
    subprocess.Popen(command, shell=True)
    # port_to_host_terminal = "8080"
    # subprocess.Popen("ttyd -o -p " + port_to_host_terminal + " " + "bash", shell=True)
    d.save()
    # print(json.dumps(ReturnValue(False, d.lastAccessTime, port_to_host_terminal), default=lambda o: o.__str__()))

    return HttpResponse(
        json.dumps(ReturnValue(False, d.lastAccessTime, port_to_host_terminal).__dict__, cls=DjangoJSONEncoder),
        content_type="application/json")


def removeDevice(request):
    DeviceId = request.GET.get('DeviceId', "")
    try:
        Device.objects.get(id=DeviceId).delete()
    except:
        return HttpResponse(False)

    return HttpResponse(True)


class HomePageView(TemplateView):
    template_name = "index.html"
