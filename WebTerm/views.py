import logging
import subprocess
import socket
from django.views.generic import TemplateView

from django.http import HttpResponse

logger = logging.getLogger("mylogger")
# logger.debug("works")
password = "admin"
username = "admin"
client = "40.0.0.10"
host = "52.27.82.38"
port = "8080"


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


# @xframe_options_exempt

def terminal(request):
    # if port == "":
    port = str(get_open_port())
    # port = "8000"

    id = 0

    if request.method == "GET":
        id = request.GET.get('id')

        pre_entered_command = "ttyd -i 20.0.0.18 -p " + port + " sshpass -p " + password + " ssh " + username + "@" + client
        # ttyd sshpass -
        #  " ssh " + username + "@" + host + " && " + password
        subprocess.Popen(pre_entered_command, shell=True)
    return HttpResponse(host + ":" +port)


class HomePageView(TemplateView):
    template_name = "index.html"



























