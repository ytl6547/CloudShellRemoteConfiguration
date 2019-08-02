# CloudShellRemoteConfiguration

Cloud Shell Remote Configuration is a web application to remotely configure Cisco devices.

## Features

- Built on top of [ttyd][1] for terminal sharing
- Access to remote Cisco devices with button clicks

# Installation and Usage

## Install in a Docker Container in DNAC
### SSH to maglev cluster
    ssh maglev@172.23.165.132 -p 2222
    Password: Maglev123
### Expose 1 port for the web server and several for terminal sharing ([ttyd][1])
    # Get the name of the api server, e.g., api-server-7659bcdb9b-k5vtt
    kubectl get pods -n rdm

    # Expose 6 (any number more than 2 according to your need) ports not used before
    #（There is a bug in DNAC, If the deployments is edited and the Docker container is restarted, 
    # the ports exposed for the original Docker container cannot be used again)
    magctl service expose api-server-7659bcdb9b-k5vtt --appstack rdm 20000
    magctl service expose api-server-7659bcdb9b-k5vtt --appstack rdm 20001
    magctl service expose api-server-7659bcdb9b-k5vtt --appstack rdm 20002
    magctl service expose api-server-7659bcdb9b-k5vtt --appstack rdm 20003
    magctl service expose api-server-7659bcdb9b-k5vtt --appstack rdm 20004
    magctl service expose api-server-7659bcdb9b-k5vtt --appstack rdm 20005
    # Save the mapping between the original and transferred port numbers to be used in the future
    # 20000 -> 8029 (For web server)
    # 20001 -> 12887 (For terminal sharing)
    # 20002 -> 19029 (For terminal sharing)
    # 20003 -> 15811 (For terminal sharing)
    # 20004 -> 20221 (For terminal sharing)
    # 20005 -> 21628 (For terminal sharing)
### Get into the Docker container
    docker ps|grep api
    # Get the hash for "maglev-registry.maglev-system.svc.cluster.local:5000/rdm/ap-server", 
    # which is usually the first one, e.g., 6f203e976d38
    
    # Get into the container with the hash
    docker exec -it 6f203e976d38 bash

### Install the running environment
#### 
    apt-get -y update && apt-get -y upgrade
#### 
    apt-get -y install iputils-ping openssh-server python3 python3-pip python3-dev cmake g++ pkg-config git vim-common libjson-c-dev libssl-dev sshpass telnet redis-server
#### 
    mkdir CloudShell
    cd CloudShell
    
    export HTTP_PROXY="http://proxy.esl.cisco.com:80"
    export HTTPS_PROXY="https://proxy.esl.cisco.com:80"
    
    git clone https://github.com/warmcat/libwebsockets.git
    cd libwebsockets/
    git checkout 89eedcaa94e1c8a97ea3af10642fd224bcea068f
    mkdir build
    cd build
    cmake ..
    make
    make install
    ldconfig
    cd ../..
    
    git clone https://github.com/tsl0922/ttyd.git
    cd ttyd && mkdir build && cd build
    cmake ..
    make && make install
    cd ../..
    
    pip3 install virtualenv
    virtualenv env
    . env/bin/activate
    
    pip3 install Django
    pip3 install -U channels
    pip3 install paramiko
    pip3 install requests
    
    git clone https://github.com/ytl6547/CloudShellRemoteConfiguration.git
    
    /etc/init.d/redis-server start
    pip3 install channels_redis[cryptography]
    
    unset HTTPS_PROXY
    unset HTTP_PROXY
    cd CloudShellRemoteConfiguration/
### Change constants
Default constants:

    LOGIN_API_URL = "https://172.23.165.132/api/system/v1/auth/login"
    CHECK_DEVICE_LIST_API_URL = "https://172.23.165.132/api/rdm/v1/device"
    CORRECT_USERNAME_FOR_DNAC_LOGIN = 'admin'
    CORRECT_PASSWORD_FOR_DNAC_LOGIN = 'Maglev123'
    DEVICE_USERNAME = "Cisco"
    DEVICE_PASSWORD = "Cisco"
    ACCESS_TIMEOUT_SECONDS = 1200

If you want to change any of them:
    
    apt-get install nano
    nano WebTerm/views.py

### Start the web server
    # Use the original port number for web server here, which is 20000 in this case
    python3 manage.py runserver 0.0.0.0:20000 &
### Tell the database your terminal sharing port mappings
1. Open in browser with `http://<DNAC IP>:<transferred port number for web server>/admin/WebTerm/port/`, e.g., http://172.23.165.132:8029/admin/WebTerm/port/
2. username: admin, password: Maglev123
3. Delete all unrelated mappings
4. Click add port on the right
5. Add your original -> transferred terminal sharing mappings one by one, keep "available" being checked, and don't forget to save
### Go to the website
Go to `http://<DNAC IP>:<transferred port number for web server>`, e.g., http://172.23.165.132:8029/

And feel free to use your shared terminal :)
## Future Usage 
### Web server stopped running
1. [SSH to maglev cluster][3]
2. [Get into the Docker container][4]
3. Start the server 
    ```
    cd CloudShell/
    . env/bin/activate
    cd CloudShellRemoteConfiguration/
    ```
4. [Start the web server][8]
5. [Go to the website][5]
### Pull updates
1. [SSH to maglev cluster][3]
2. [Get into the Docker container][4]
3. Remove folder and run again
    ```
    cd CloudShell/
    . env/bin/activate
    rm -r CloudShellRemoteConfiguration/
    export HTTPS_PROXY="https://proxy.esl.cisco.com:80"
    git clone https://github.com/ytl6547/CloudShellRemoteConfiguration.git
    unset HTTPS_PROXY
    cd CloudShellRemoteConfiguration/
    ```
4. [Change constants][6]
5. [Start the web server][8]
6. [Tell the database your terminal sharing port mappings][7]
7. [Go to the website][5]

# Functionalities
1. Login
    1. User input username and password of the DNAC
    2. Click Submit
    3. If succeeded, “Connect!” becomes clickable, if not, alert “Wrong username or password!”
2. Show devices and status in the DNAC
    1. When a user opens the website, the backend creates a thread. In every 5 minutes, the thread pushes the new DNAC devices data to the frontend. The frontend shows the device name and device status to the user.
3. Search a device
    1. In the real time, the user can search a device by a string inside of the device name. All the devices with the string in their names will be shown in the list
4. Select and connect to a device
    1. A user can select a device by clicking it in the device list 
    2. By clicking “Connect!”, the device id will be sent to the backend with AJAX (if you already connected to a device, you need to disconnect first)
    3. In the following cases, Connection will fail with an alert:
        1. Not logged in
        2. Fetching data from the DNAC failed
        3. The device is not in the list of DNAC 
        4. The device status is not CONNECTED
        5. The device is using by someone else
            1. Will show countdown for time needed for waiting
        6. No available port to host the terminal sharing tool
    4. If connection succeeded, will show the device console in the iframe (Sometimes iframe shows “host refused to connect”. In this situation, “Reload frame” is good)
    5. Do any operation you want in the shared console within the time limitation
5. Countdown
    1. After connected to a device, the countdown will be shown on the top
6. Disconnect
    1. By clicking “Disconnect!” or the time limitation reached, the user will lose connection with the device, and anybody can connect to the device
# Browser Support

Modern browsers, See [Browser Support][2].

# Credits

- [ttyd][1]: ttyd provides the terminal sharing functionality

  [1]: https://github.com/tsl0922/ttyd
  [2]: https://github.com/xtermjs/xterm.js#browser-support  
  [3]: https://github.com/ytl6547/CloudShellRemoteConfiguration#ssh-to-maglev-cluster
  [4]: https://github.com/ytl6547/CloudShellRemoteConfiguration#get-into-the-docker-container
  [5]: https://github.com/ytl6547/CloudShellRemoteConfiguration#go-to-the-website
  [6]: https://github.com/ytl6547/CloudShellRemoteConfiguration#change-constants
  [7]: https://github.com/ytl6547/CloudShellRemoteConfiguration#tell-the-database-your-terminal-sharing-port-mappings
  [8]: https://github.com/ytl6547/CloudShellRemoteConfiguration#start-the-web-server