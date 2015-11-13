# Script NFAB
Python script Nmap and Fabric to scan network.
The objective is to send a shell command to the hosts.

>ex : python fabric-nmap.py -H 192.168.2.1/24 -u benoit -C "tail /etc/fstab | grep /volume1"

## Stack
 + Linux x86_64
 + Python 2.7.6
 + [Nmap] (http://nmap.org)
    >Nmap version 6.40 ( http://nmap.org )
    >Platform: x86_64-pc-linux-gnu
    >Compiled with: liblua-5.2.3 openssl-1.0.1f libpcre-8.31 libpcap-1.5.3 nmap-libdnet-1.12 ipv6
    >Compiled without:
    >Available nsock engines: epoll poll select
 + [Python-nmap 0.4.3] (http://xael.org/pages/python-nmap-en.html)
 + [Fabric] (http://www.fabfile.org)
    >Fabric 1.10.2
    >Paramiko 1.15.2


>Warning : this version don't work with Python 3.x. 


## Schema

![schema](https://cloud.githubusercontent.com/assets/7000210/11146997/3b8b19aa-8a13-11e5-8544-a4607698a034.png)


## Install

    sudo pip install fabric
    sudo pip install python-nmap
  
## Script

    python nfab.py -H 192.168.1.0/24 -u benoit -C "tail /etc/fstab | grep /volume1/backup" 

    Usage: nfab.py [options]
    Options:
        -h, --help            
            show this help message and exit
        -H HOST, --host=HOST  
            Enter IP or the range IP ex: 192.168.1.0/24
        -u LOGIN, --user=LOGIN
            Enter your login
        -S --sudo
            Active sudo command 
        -C COMMAND, --command=COMMAND
            Enter the shell command
        -i FILE, --in=FILE 
            Enter input CSV file
        -q, --verbose
            Active debug
        -v, --version
            See app version
        -P, --ping
            Active ping mode
        -o, --out=FILENAME
             Enter output CSV file
        -L FILENAME, --log=FILENAME
             Enter output filename log
             
## Usecase

[Visit wiki UseCase] (https://github.com/bfoujols/fabric-nmap/wiki/UseCase)

## Release

#### v0.7.0
- [Added] List IP fail in the report action
- [Updated] Readme
- [Fixed] Log to concat str()
- [Fixed] Condition ArgV

#### v0.6.0
- [Added] Return error host
- [Added] Logging
- [Added] Report Action

#### v0.5.0
- [Added] Active command Ping 

#### v0.4.0
- [Added] Active command Sudo

#### v0.3.0
- [Added] Docstring
- [Added] Version mode

#### v0.2.0
- [Added] Input file CSV for list host
- [Added] Verbose mode

#### v0.1.0
- [Added] Init code script