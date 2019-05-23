import subprocess
import socket
from django.views.generic import TemplateView

from django.http import HttpResponse
from threading import Timer

password = "admin"
username = "admin"
clientIP = "40.0.0.10"
host = "52.27.82.38"
port = "8080"
timeout_sec = "20"
kill = lambda process: process.kill()


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def terminal(request):
    port = str(get_open_port())

    DeviceId = 0

    if request.method == "GET":
        DeviceId = request.GET.get('DeviceId')

        pre_entered_command = "sshpass -p " + password + " ssh " + username + "@" + clientIP

        command = "timeout " + timeout_sec + " ttyd -i 20.0.0.18 -o -p " + port + " " + pre_entered_command
        proc = subprocess.Popen(command, shell=True)
        # try:
        #     proc.communicate(timeout=5)
        # except subprocess.TimeoutExpired:
        #     proc.kill()
        #     proc.communicate()
        timer = Timer(3, proc.kill)
        # timer.start()
        try:
            timer.start()
            proc.communicate()
        finally:
            timer.cancel()
        # proc.kill()
    return HttpResponse(host + ":" +port)


class HomePageView(TemplateView):
    template_name = "index.html"



























