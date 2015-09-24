# fabric-nmap
Python script Nmap and Fabric to scan network
The objective is to send a shell command to the hosts found (nmap)

>ex : python fabric-nmap.py -H 192.168.2.1/24 -u benoit -C "tail /etc/fstab | grep /volume1/backup"

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

## Install

    sudo pip install fabric
    sudo pip install python-nmap
  
## Script

    python fabric-nmap.py -H 192.168.2.1/24 -u benoit -C "tail /etc/fstab | grep /volume1/backup" 

    Usage: fabric-nmap.py [options]
    Options:
        -h, --help            
            show this help message and exit
        -H HOST, --host=HOST  
            Enter IP or the range IP ex: 192.168.1.0/24
        -u LOGIN, --user=LOGIN
            Enter your login
        -C COMMAND, --command=COMMAND
            Enter the shell command
        -c FILE, --inputcsv=FILE 
            Enter input CSV file
        -v, --verbose
            Active mode debug

## Release

#### v0.2.0
- [Added] Input file CSV for list host
- [Added] Verbose mode

#### v0.1.0
- [Added] Init code script