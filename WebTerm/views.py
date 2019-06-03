import subprocess
import socket
from django.views.generic import TemplateView

from django.http import HttpResponse, StreamingHttpResponse
import asyncio
from channels.consumer import AsyncConsumer
import time
import websockets
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
    print(r.text)
    device_list = json.loads(r.text)
    print(device_list)

    filtered_device_list = []
    for device in device_list:
        if device['connectionState']['state'] == "PENDING":
            filtered_device_list.append(device)
    device_list = filtered_device_list
    return json.dumps(device_list)


def terminal(request):
    portToHostTerminal = str(get_open_port())

    DeviceId = ""

    if request.method == "GET":
        DeviceId = request.GET.get('DeviceId')

        pre_entered_command = "sshpass -p " + clientPassword + " ssh " + clientUsername + "@" + clientIP

        command = "timeout " + timeout_sec + " ttyd -o -p " + portToHostTerminal + " " + pre_entered_command
        subprocess.Popen(command, shell=True)

    return HttpResponse(portToHostTerminal)


class HomePageView(TemplateView):
    template_name = "index.html"
