# CloudShellRemoteConfiguration

Cloud Shell Remote Configuration is a web application to remotely configure Cisco devices.

## Features

- Built on top of [ttyd][1] for terminal sharing
- Access to remote Cisco devices with button clicks

# Installation and Usage

## Install on Linux

- Build from source (debian/ubuntu):

    ```bash
    # SSH to cloud vm

    # Become root
    sudo -s

    # Install apt-get
    apt-get update && apt-get -y upgrade

    # Install cmake
    apt install cmake

    # Install Python3
    apt-get install python3
    python3 -V

    # Install pip3
    apt-get install -y python3-pip
    pip3 -V

    # Install sshpass
    apt-get install sshpass

    # Create Cloud Shell directory
    mkdir CloudShell
    cd CloudShell/

    # Install libwebsockets v3.1.0
    git clone https://github.com/warmcat/libwebsockets.git
    cd libwebsockets/
    git checkout 89eedcaa94e1c8a97ea3af10642fd224bcea068f
    apt-get install libssl-dev
    mkdir build
    cd build
    cmake ..
    make
    make install
    ldconfig
    cd ../..

    # Install ttyd
    apt-get install cmake g++ pkg-config git vim-common libwebsockets-dev libjson-c-dev libssl-dev
    git clone https://github.com/tsl0922/ttyd.git
    cd ttyd && mkdir build && cd build
    cmake ..
    make && make install
    cd ../..

    # Install virtualenv
    pip3 install virtualenv
    virtualenv --version
    virtualenv env
    . env/bin/activate

    # Install Django
    pip3 install Django
    django-admin --version

    # Clone Cloud Shell
    git clone https://github.com/ytl6547/CloudShellRemoteConfiguration.git
    ```
    
## Example Usage
    
    sudo -s
    cd CloudShell/
    . env/bin/activate
    cd CloudShellRemoteConfiguration/
    python3 manage.py runserver 0.0.0.0:80
    
Then open http://`<publicIP>` with a browser.

## Browser Support

Modern browsers, See [Browser Support][2].

# Credits

- [ttyd][1]: ttyd provides the terminal sharing functionality

  [1]: https://github.com/tsl0922/ttyd
  [2]: https://github.com/xtermjs/xterm.js#browser-support  
