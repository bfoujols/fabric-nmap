# Fabric-nmap
# Version 0.1.0
# Benoit Foujols <benoit@foujols.com>
#

import optparse
import nmap
import getpass
import sys
from fabric.api import *
from fabric.network import disconnect_all

# Class qui recupere les IP avec Nmap
class reportNetwork:

        def __init__(self, hosts='localhost'):
            self.hosts = hosts

        def getNetwork(self):
            try:
                self.nmap = nmap.PortScanner()
            except nmap.PortScannerError:
                print('Nmap Erreur', sys.exc_info()[0])
                sys.exit(0)
            except:
                print("Error:", sys.exc_info()[0])
                sys.exit(0)

            hosts = self.nmap.listscan(self.hosts)

            return hosts

# Class qui execute Fabric
class reportHost:

        def __init__(self, hosts='', login='', password='', command=''):

            if hosts and login and password and command:
                def fabricHosts():
                    env.hosts = hosts

                def fabricEnv():
                    env.skip_bad_hosts=True
                    env.warn_only = True
                    env.user = login
                    env.password = password
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
                print "ERROR : Manque un argument"

# Recuperation des arguments
def getArg():
    script_info = """Script qui va cherche des infos sur les serveurs de ton reseau\n"""
    script_usage = "usage: %prog [options]"

    parser = optparse.OptionParser(usage=script_usage, description=script_info)
    parser.add_option("-H", "--host", dest="getarg_host",
                      help="Entrez une IP ou un range ex 192.168.1.0/24")
    parser.add_option("-u", "--user", dest="getarg_login", help="Entrez votre login")
    parser.add_option("-C", "--command", dest="getarg_command", help="Entrez une commande shell")

    (options, args) = parser.parse_args()

    if not options.getarg_host:
        print "ERROR : Il faut obligatoirement un host ou un un range ex 192.168.1.0/24 - Option -H <HOST>"
        sys.exit(0)
    elif not options.getarg_command:
        print "ERROR : Il faut obligatoirement une commande - Option -C <COMMAND>"
        sys.exit(0)
    elif options.getarg_login:
        login = options.getarg_login
        password = getpass.getpass('Entrez votre mot de passe : ')
    else:
        print "ERROR : Il faut obligatoirement un login - Option -u <LOGIN>"
        sys.exit(0)

    return options.getarg_host, options.getarg_command, login, password


def main():
    # get the user inputs
    host, command, login, password = getArg()

    print 'HOST    :', host
    print 'USER :', login
    print 'COMMAND', command

    report = reportNetwork(host)
    hosts = report.getNetwork()

    reportHost(hosts, login, password, command)

if __name__ == "__main__":
    main()
