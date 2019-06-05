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

login_url = "https://172.27.250.16/api/system/v1/auth/login"
check_device_url = "https://172.27.250.16/api/rdm/v1/device"
username = 'admin'
password = 'Maglev123'

clientPassword = "admin"
clientUsername = "admin"
clientIP = "40.0.0.10"
timeout_sec = "20"


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


def login():
    global Cookies
    response = session.get(login_url, auth=(username, password), verify=False)

    Cookies = parse_dict_cookies(response.headers['Set-Cookie'])


def getDevices():
    print("get devices")
    global device_list
    if Cookies == {}:
        login()

    r = session.get(check_device_url, cookies=Cookies, verify=False)
    if r.status_code != 200:
        login()
        r = session.get(check_device_url, cookies=Cookies, verify=False)
    # print(r.text)
    device_list = json.loads(r.text)
    # print(device_list)

    filtered_device_list = []
    for device in device_list:
        if device['connectionState']['state'] == "PENDING":
            filtered_device_list.append(device)
    device_list = filtered_device_list
    return json.dumps(device_list)


class ReturnValue():
    def __init__(self, pending=True, last_access_time=None, port=None):
        self.port = port
        self.lastAccessTime = last_access_time
        self.pending = pending


def terminal(request):
    DeviceId = request.GET.get('DeviceId', "")

    # Query the database
    try:
        d = Device.objects.get(id=DeviceId)
        print(d.id)
        print(d.lastAccessTime)
        if (datetime.now(timezone.utc) - d.lastAccessTime).total_seconds() < 1200:  # using by others
            # return not pending and the access time of others
            print((datetime.now(timezone.utc) - d.lastAccessTime).total_seconds())
            return HttpResponse(json.dumps(ReturnValue(False, d.lastAccessTime).__dict__, cls=DjangoJSONEncoder),
                                content_type="application/json")
    except Device.DoesNotExist:  # not accessed by any one
        d = Device(id=DeviceId)
    except:
        d = Device(id=DeviceId)
    else:
        d = Device(id=DeviceId)

    # check whether device status is PENDING
    # getDevices()
    # for device in device_list:
    #     if device["deviceId"] == DeviceId:
    #         if device["connectionState"]["state"] == "PENDING":
    #             return HttpResponse(json.dumps(ReturnValue().__dict__, cls=DjangoJSONEncoder),
    #                                 content_type="application/json")
    #         break

    # get the password

    # prepare commands and ports
    port_to_host_terminal = str(get_open_port())
    pre_entered_command = "sshpass -p " + clientPassword + " ssh " + clientUsername + "@" + clientIP
    command = "timeout " + timeout_sec + " ttyd -o -p " + port_to_host_terminal + " " + pre_entered_command

    # start the timer
    d.lastAccessTime = datetime.now(timezone.utc)

    # do it!
    # subprocess.Popen(command, shell=True)
    subprocess.Popen("ttyd -o -p " + port_to_host_terminal, shell=True)
    d.save()
    # print(json.dumps(ReturnValue(False, d.lastAccessTime, port_to_host_terminal), default=lambda o: o.__str__()))

    return HttpResponse(
        json.dumps(ReturnValue(False, d.lastAccessTime, port_to_host_terminal).__dict__, cls=DjangoJSONEncoder),
        content_type="application/json")


class HomePageView(TemplateView):
    template_name = "index.html"
