# fabric-nmap
Python script Nmap and Fabric to scan network
The objective is to send a shell command to the hosts found (nmap)

>ex : python fabric-nmap.py -H 192.168.2.1/24 -u benoit -C "tail /etc/fstab | grep /volume1/backup"

## Stack
 + Linux 
 + Python 2.7
 + Nmap 
 + [Fabric] (http://www.fabfile.org)
 + [Nmap] (http://xael.org/pages/python-nmap-en.html)

>Warning : this version don't work with Python 3.x. 

## Install

    sudo pip install fabric
    sudo pip install python-nmap
  
## Script

    python fabric-nmap.py -H 192.168.2.1/24 -u benoit -C "tail /etc/fstab | grep /volume1/backup" 

    Usage: fabric-nmap.py [options]
    Options:
    -h, --help            show this help message and exit
    -H GETARG_HOST, --host=GETARG_HOST
                        Entrez une IP ou un range ex 192.168.1.0/24
    -u GETARG_LOGIN, --user=GETARG_LOGIN
                        Entrez votre login
    -C GETARG_COMMAND, --command=GETARG_COMMAND
                        Entrez une commande shell


## Release

#### v0.1.0
- [Added] Init code script