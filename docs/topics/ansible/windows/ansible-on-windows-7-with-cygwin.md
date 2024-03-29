---
title: 'Portable Ansible Installation on Windows 7 using Cygwin'
minute_read: 5
categories:
  - devops
  - dsc
tags:
  - ansible
  - windows
  - cygwin
---

### Overview 

You want to install ansible on Windows 7 x64

### Environment Information

- Windows OS:
```
    powershell -NoProfile [System.Environment]::OSVersion.Version
    OS: Windows 7 x64
    Major  Minor  Build  Revision
    -----  -----  -----  --------
    6      1      7601   65536
```
- Cygwin Version (post-installation): 3.0.7(0.338/5/3)
- Ansible Environment (post-installation): 
```
  ansible --version
  ansible 2.9.0.dev0
    config file = None
    configured module search path = [u'/home/${USERNAME}/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
    ansible python module location = /usr/lib/python2.7/site-packages/ansible-2.9.0.dev0-py2.7.egg/ansible
    executable location = /opt/ansible/bin/ansible
    python version = 2.7.16 (default, Mar 20 2019, 12:15:19) [GCC 7.4.0]
```

### Instructions

#### Install cygwin

- Download cygwin64 from [https://www.cygwin.com/setup-x86_64.exe](https://www.cygwin.com/setup-x86_64.exe)
- Create the installation folder (I'm using **C:\tools\cygwin**)
- Move _setup-x86_64.exe_ to **C:\tools\cygwin**
- Click _setup-x86_64.exe_
- Make sure to set the install folder and package folder to **C:\tools\cygwin**
- Go through the setup instructions, and when at the package selection screen,
- Only install wget
- The cygwin64 core package installations will take time, so busy yourself with something else in the meantime :)
- Once the installation is complete, close it out

#### Install python and its dependencies

- From the installation folder (**C:\tools\cygwin**), click Cygwin.bat
- This will initialize your cygwin environment and start the bash interactive terminal
- Adjust shell environment:
  ```
  export PATH="/usr/bin:$PATH"
  PATH+=:~+/bin
  ```
- Install the _apt-cyg_ package manager
  ```
  wget raw.github.com/transcode-open/apt-cyg/master/apt-cyg
  chmod +x apt-cyg
  mv apt-cyg /usr/local/bin
  which -a apt-cyg >/dev/null 2>&1 && echo ok
  ```
- install git, python-devel, gcc-g++, curl, dos2unix, zip, unzip
  ```
  apt-cyg install git python-devel curl dos2unix zip unzip
  ```
- install pip
  ```
  wget https://bootstrap.pypa.io/get-pip.py
  python get-pip.py
  ```
  
#### Install python and its dependencies

Your cygwin environment should be good for installing ansible, so let's get to it.

- Install dependence
  ```
  apt-cyg install openssl openssl-devel libffi-devel vim
  apt-cyg install python-{jinja2,six,yaml,crypto,cryptography}
  ```
- Install ansible from github
  ```
  mkdir /opt
  cd /opt
  git clone --depth 1 git://github.com/ansible/ansible
  cd ansible
  python setup.py install
  ```
- Update your PATH variable
  ```
  echo export PATH="/opt/ansible/bin:\$PATH" >> ~/.bash_profile
  ```
- Verify installation
  ```
  which -a ansible >/dev/null 2>&1 && echo We found the anible binary! || echo We could not find the ansible binary! Please troubleshoot!
  ```
- Troubleshooting<br />
  If problems, use a search engine to look up any errors, start over, rinse/repeat  

#### Test Run

The below worked!

`ansible --connection=local localhost, -m setup -a 'filter=ansible_host*'`

### Appendix

#### Setup cmder

I ran the above tests using [Cmder](https://cmder.net/).

Instructions:
  - Start cmder
  - Click the green + sign at the bottom right
  - Click "Setup Tasks"
  - Click the + sign at the bottom of 'Predefined tasks (command groups)'
    - For 'Task Parameters', enter:
    ```
    /icon "**C:\tools\cygwin**\Cygwin.ico"
    ```
    - Paste this into the empty text area at the bottom right:<br />
      ```
      -cur_console:t:ansible "**C:\tools\cygwin**\bin\bash.exe" --login -i
      ```

#### Notes
  
Final folder size for **C:\tools\cygwin**: **1.24 GB**

That's a big-ass folder for lil' ol' ansible ...

So yeah ...

#### Learning Points

Ansible can (at least in theory) run on Windows 7 x64, but it's not without pain *AND* it's not without problems.

I tested the uri module and was greeted with an error:

```
The following modules failed to execute: setup
  setup: MODULE FAILURE
See stdout/stderr for the exact error
```

More digging I must do.

#### References

- Google Search > ansible on windows 7 - [https://lmgtfy.com/?q=ansible+on+windows+7](https://lmgtfy.com/?q=ansible+on+windows+7)
- Google Search > "apt-cyg" "ansible" "bat" - [https://lmgtfy.com/?q=%22apt-cyg%22+%22ansible%22+%22bat%22](https://lmgtfy.com/?q=%22apt-cyg%22+%22ansible%22+%22bat%22)
- pip - Installing Ansible Python package on Windows - Stack Overflow - [https://stackoverflow.com/questions/51167099/installing-ansible-python-package-on-windows](https://stackoverflow.com/questions/51167099/installing-ansible-python-package-on-windows)
- Running Ansible within Windows (Jeff Geerling) - [https://www.jeffgeerling.com/blog/running-ansible-within-windows](https://www.jeffgeerling.com/blog/running-ansible-within-windows)
- How to install Ansible to Windows - [https://gist.github.com/eyasuyuki/d9c1dc96a9b8356164e5](https://gist.github.com/eyasuyuki/d9c1dc96a9b8356164e5)
