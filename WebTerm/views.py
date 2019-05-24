import subprocess
import socket
from django.views.generic import TemplateView

from django.http import HttpResponse
from threading import Timer

clientPassword = "admin"
clientUsername = "admin"
clientIP = "40.0.0.10"
hostPublic = "pnp-scd-dev03.cisco.com"
# hostLocal = "172.23.165.87"
# portToHostTerminal = "8080"
timeout_sec = "20"


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def terminal(request):
    portToHostTerminal = str(get_open_port())

    DeviceId = 0

    if request.method == "GET":
        DeviceId = request.GET.get('DeviceId')

        pre_entered_command = "sshpass -p " + clientPassword + " ssh " + clientUsername + "@" + clientIP

        command = "timeout " + timeout_sec + " ttyd -o -p " + portToHostTerminal + " " + pre_entered_command
        subprocess.Popen(command, shell=True)

    return HttpResponse(hostPublic + ":" + portToHostTerminal)


class HomePageView(TemplateView):
    template_name = "index.html"



























