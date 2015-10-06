"""
fabric-nmap.py - version and date, see below

Source code : https://github.com/bfoujols/fabric-nmap.git

"""

__author__ = 'Benoit Foujols (benoit@foujols.com)'
__version__ = '0.4.0'
__last_modification__ = '2015.10.06'


import optparse
import nmap
import getpass
import sys
import csv
from fabric.api import *
from fabric.network import disconnect_all

#import paramiko, os
#paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

class reportNetwork:
    """
    Class reportNetwork
    Recover IP for NMAP
    """
    def __init__(self, hosts='localhost'):
        """
        Init reportNetwork
        :param hosts: string IP ex 192.168.0.1 or 192.168.2.0/24
        """
        self.hosts = hosts


    def getNetwork(self):
        """
        Get Network in list
        :return: list

        Ex : ['192.168.0.1', '192.168.0.2', '192.168.0.3']
        """
        try:
            self.nmap = nmap.PortScanner()
        except nmap.PortScannerError:
            print("ERROR-005 NMAP :", sys.exc_info()[0])
            sys.exit(0)
        except:
            print("ERROR-004 :", sys.exc_info()[0])
            sys.exit(0)

        hosts = self.nmap.listscan(self.hosts)

        return hosts



class reportHost:
    """
    Class reportHost
    Executed Fabric Script
    """
    def __init__(self, hosts='', login='', password='', command='', sudo_commande=''):
        """
        Init reportHost
        :param hosts: List [IP]
        :param login: String login SSH
        :param password: String password SSH
        :param command: String commande shell
        :param sudo: Booleen active mode sudo
        """

        if hosts and login and password and command:
            def fabricHosts():
                env.hosts = hosts

            def fabricEnv():
                env.skip_bad_hosts=True
                env.warn_only = True
                env.user = login
                env.password = password
                if sudo_commande:
                    sudo(command)
                else:
                    run(command)

            @task
            def runFabric():
                execute(fabricHosts)
                execute(fabricEnv)

            try:
                runFabric()
            finally:
                disconnect_all()
        else:
            print "ERROR-003 : Missing an argument"



class inputCsv:
    """
    Class inputCsv
    Input file Host CSV
    """
    def __init__(self, filecsv=''):
        """
        Init inputCsv
        :param filecsv: String name file CSV

        Ex : See -> test.csv
        10.10.12.43
        10.10.10.20
        10.10.0.11
        """
        self.filecsv = filecsv

    def getHostToCsv(self):
        """
        Get Network in list
        :return: list

        Ex : ['10.10.12.43', '10.10.10.20', '10.10.0.11']
        """
        if self.filecsv:
            file = open(self.filecsv, 'rt')
            try:
                reader = csv.reader(file)
                listhosts = []
                for row in reader:
                    listhosts.append(row[0])
                return listhosts
            finally:
                file.close()
        else:
            print "ERROR-006 : No file CSV"
            sys.exit(0)



def getArg():
    """
    Get the argument
    TODO deprecated 2.7 -> argparse

    :return: (options, args)

    options.getarg_version Option -v
    options.getarg_verbose Option -q
    options.getarg_csv Option -c
    options.getarg_host Option -H
    options.getarg_command Option -C
    options.getarg_sudo Option -S
    login Option -u
    password getpass
    """
    script_info = """Script Fabric Network (use Nmap)\n"""
    script_usage = "usage: %prog [options]"

    parser = optparse.OptionParser(usage=script_usage, description=script_info)
    parser.add_option("-H", "--host", dest="getarg_host",
                      help="Enter IP or the range IP ex: 192.168.1.0/24", metavar="HOST")
    parser.add_option("-u", "--user", dest="getarg_login", help="Enter your login", metavar="LOGIN")
    parser.add_option("-C", "--command", dest="getarg_command", help="Enter the shell command", metavar="COMMAND")
    parser.add_option("-S", "--sudo", dest="getarg_sudo", help="Active mode command sudo", action="store_true")
    parser.add_option("-c", "--inputcsv", dest="getarg_csv", help="Enter input CSV file", metavar="FILE")
    parser.add_option("-q", "--verbose", dest="getarg_verbose", help="Active mode debug", action="store_true")
    parser.add_option("-v", "--version", dest="getarg_version", help="See app version", action="store_true")

    (options, args) = parser.parse_args()

    if options.getarg_version:
        print "Script Fabric Network (use Nmap)"
        print "VERSION ", __version__
        print "LAST_MODIFICATION ", __last_modification__
        sys.exit(0)
    elif not options.getarg_command:
        print "ERROR-001 : You must first the command - Option -C <COMMAND>"
        sys.exit(0)
    elif options.getarg_login:
        login = options.getarg_login
        password = getpass.getpass('Enter your password : ')
    else:
        print "ERROR-002 : You must first your login SSH - Option -u <LOGIN>"
        sys.exit(0)

    return options.getarg_sudo, options.getarg_verbose, options.getarg_csv, options.getarg_host, options.getarg_command, login, password



def main():
    sudo_commande, verbose, filecsv, host, command, login, password = getArg()

    if verbose:
        print "**** ARG **************************"
        print "Host:",host
        print "CSV:",filecsv
        print "COMMAND:",command
        print "LOGIN:",login
        print "**** ARG end **********************"

    if host:
        report = reportNetwork(host)
        hosts = report.getNetwork()
    elif filecsv:
        inputfile = inputCsv(filecsv)
        hosts = inputfile.getHostToCsv()
    else:
        print "Please, select the option -c or -H"

    if verbose:
        print "**** LIST Host **************************"
        print hosts
        print "**** LIST Host end **********************"

    reportHost(hosts, login, password, command, sudo_commande)



if __name__ == "__main__":
    main()
