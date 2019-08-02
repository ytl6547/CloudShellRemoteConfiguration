import subprocess
from threading import Thread

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from WebTerm.models import Device, Port
from datetime import datetime, timezone
import requests
import json

session = requests.Session()
Cookies = {}
# login_url = "https://172.27.250.16/api/system/v1/auth/login"
# check_device_url = "https://172.27.250.16/api/rdm/v1/device"
login_url = "https://172.23.165.132/api/system/v1/auth/login"
check_device_url = "https://172.23.165.132/api/rdm/v1/device"
username = ''
password = ''
CORRECT_USERNAME = 'admin'
CORRECT_PASSWORD = 'Maglev123'

devicePassword = "Cisco"
deviceUsername = "Cisco"
deviceIP = ""
timeout_sec = 1200

logged_in = False


def get_open_port():
    ports = Port.objects.filter(available=True)
    if len(ports) > 0:
        return ports[0]

    return False


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
    global Cookies
    global logged_in
    response = session.get(login_url, auth=(username, password), verify=False)
    if response.status_code != 200:
        response = session.get(login_url, auth=(CORRECT_USERNAME, CORRECT_PASSWORD), verify=False)

        Cookies = parse_dict_cookies(response.headers['Set-Cookie'])
        logged_in = False
        return False

    Cookies = parse_dict_cookies(response.headers['Set-Cookie'])
    logged_in = True
    return True


def getDevices():
    if Cookies == {}:
        loginToDNAC()

    r = session.get(check_device_url, cookies=Cookies, verify=False)
    if r.status_code != 200:
        loginToDNAC()
        r = session.get(check_device_url, cookies=Cookies, verify=False)
    if r.status_code != 200:
        return {"success": False, "message": "Failed to get the device list from the DNAC API with status code " + str(r.status_code)}
    return {"success": True, "deviceList": json.loads(r.text)}


def login(request):
    global username, password
    username = request.POST.get("username")
    password = request.POST.get("password")
    return HttpResponse(loginToDNAC())


def hostTerminal(command, device, port):
    print("Connecting to", deviceIP)
    # do it!
    subprocess.Popen(command, shell=True).wait()
    print("Disconnected from", deviceIP)
    device.delete()
    port.available = True
    port.save()


def terminal(request):
    global deviceIP
    if not logged_in:
        return JsonResponse({"success": False, "message": "Please login first!"})

    DeviceId = request.GET.get('DeviceId', "")

    # Fetching data from the DNAC failed
    deviceResult = getDevices()
    if not deviceResult["success"]:
        return JsonResponse(deviceResult)

    # check whether the device is in the list of DNAC and device status is CONNECTED
    deviceInDNAC = False
    for device in deviceResult["deviceList"]:
        if device["deviceId"] == DeviceId:
            if device["connectionState"]["state"] != "CONNECTED":
                return JsonResponse({"success": False, "message": "This device is not ready to use."})
            deviceIP = device["ipAddr"]
            deviceInDNAC = True
            break

    if not deviceInDNAC:
        return JsonResponse({"success": False, "message": "No such device in the DNAC"})

    # Query the database to check availability
    try:
        d = Device.objects.get(id=DeviceId)
        return JsonResponse({"success": True, "port": None, "lastAccessTime": d.lastAccessTime, "timeoutSec": timeout_sec})
    except Device.DoesNotExist:  # not accessed by any one
        d = Device(id=DeviceId)

    # prepare commands and ports
    port = get_open_port()
    if port is False:
        return JsonResponse({"success": False, "message": "No available port. Please wait or add new ports."})

    pre_entered_command = "sshpass -p " + devicePassword + " ssh -o \"StrictHostKeyChecking no\" " + deviceUsername + "@" + deviceIP
    command = "timeout " + str(timeout_sec) + " ttyd -o -p " + port.originalPort + " " + pre_entered_command

    t = Thread(target=hostTerminal, args=(command, d, port,))

    # mark as unavailable
    port.available = False

    # start the timer
    d.lastAccessTime = datetime.now(timezone.utc)

    # do it!
    t.start()
    d.save()
    port.save()
    return JsonResponse({"success": True, "port": port.transferedPort, "lastAccessTime": d.lastAccessTime, "timeoutSec": timeout_sec})


class HomePageView(TemplateView):
    template_name = "index.html"
