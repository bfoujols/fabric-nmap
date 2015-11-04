"""
fabric-nmap.py - version and date, see below

Source code : https://github.com/bfoujols/fabric-nmap.git

"""

__author__ = 'Benoit Foujols (benoit@foujols.com)'
__version__ = '0.6.0'
__last_modification__ = '2015.11.04'

import optparse
import nmap
import getpass
import sys
import csv
import time
import logging
from fabric.api import *
from fabric.network import disconnect_all

# import paramiko, os
# paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

logger = logging.getLogger()


class reportAction:
    """
    Class report Action
    """
    count_total = 0
    count_fail = 0
    count_success = 0


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
            Log01 = "ERROR-NMAP-01: ", sys.exc_info()[0]
            logger.critical(Log01)
            print(Log01)
            sys.exit(0)
        except:
            Log02 = "ERROR-NMAP-02: ", sys.exc_info()[0]
            logger.critical(Log02)
            print(Log02)
            sys.exit(0)

        hosts = self.nmap.listscan(self.hosts)
        totalhost = len(hosts)
        reportAction.count_total = totalhost
        logger.debug("COUNT_HOST: " + str(totalhost))

        return hosts

    def getPingUp(self):
        """
        Get Network in ping network for Nmap
        :return: list

        Ex : ['192.168.0.1', '192.168.0.2', '192.168.0.3']
        """

        try:
            self.nmap = nmap.PortScanner()
        except nmap.PortScannerError:
            Log03 = "ERROR-NMAP-03: ", sys.exc_info()[0]
            logger.critical(Log03)
            print(Log03)
            sys.exit(0)
        except:
            Log04 = "ERROR-NMAP-04: ", sys.exc_info()[0]
            logger.critical(Log04)
            print(Log04)
            sys.exit(0)

        self.nmap.scan(self.hosts, arguments='-sP')
        hosts = self.nmap.all_hosts()
        # hosts = [(x, self.nmap[x]['status']['state']) for x in self.nmap.all_hosts()]
        totalhost = len(hosts)
        reportAction.count_total = totalhost
        logger.debug("COUNT_HOST: " + str(totalhost))

        return hosts


class execHost:
    """
    Class execHost
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
                env.skip_bad_hosts = True
                env.warn_only = True
                env.user = login
                env.password = password

                host_exec = "[" + env.host_string + "]"

                try:
                    if sudo_commande:
                        output = sudo(command)
                    else:
                        output = run(command)

                    if (output.stderr != ""):
                        logger.warning(host_exec + " fail")
                        reportAction.count_fail += 1
                    else:
                        reportAction.count_success += 1
                        logger.info(host_exec + " success")
                        logger.info(host_exec + " result: " + output)

                except Exception, e:
                    reportAction.count_fail += 1
                    logger.warning(host_exec + " fail exception: " + e.message)

            @task
            def runFabric():
                execute(fabricHosts)
                execute(fabricEnv)

            try:
                runFabric()
            finally:
                disconnect_all()
        else:
            log003 = "ERROR-003: Missing an argument"
            logger.critical(log003)
            print log003


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

                totalhost = len(listhosts)
                reportAction.count_total = totalhost
                logger.debug("COUNT_HOST: " + str(totalhost))

                return listhosts
            finally:
                file.close()
        else:
            print "ERROR-006: No file CSV"
            sys.exit(0)


def getArg():
    """
    Get the argument
    TODO deprecated 2.7 -> argparse

    :return: (options, args)

    options.getarg_ping Option -P
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
    parser.add_option("-P", "--ping", dest="getarg_ping", help="Enter your filename", metavar="FILENAME")
    parser.add_option("-L", "--log", dest="getarg_log", help="Enter your filename", metavar="FILENAME")

    (options, args) = parser.parse_args()

    if options.getarg_version:
        print "Script Fabric Network (use Nmap)"
        print "VERSION ", __version__
        print "LAST_MODIFICATION ", __last_modification__
        sys.exit(0)
    elif not (options.getarg_command or options.getarg_ping):
        print "ERROR-CMD-01 : You must first the command - Option -C <COMMAND> OR Option -P <FILENAME>"
        sys.exit(0)
    elif options.getarg_command and not options.getarg_login:
        print "ERROR-CMD-02 : You must first your login SSH - Option -u <LOGIN>"
        sys.exit(0)

    if options.getarg_login:
        login = options.getarg_login
        password = getpass.getpass('Enter your password : ')
    else:
        login = False
        password = False

    return options.getarg_log, options.getarg_ping, options.getarg_sudo, options.getarg_verbose, options.getarg_csv, options.getarg_host, options.getarg_command, login, password


def main():
    # get arg in the commande
    logging_commande, ping_commande, sudo_commande, verbose, filecsv, listhost, command, login, password = getArg()

    if not logging_commande:
        logging_commande = "fabric-nmap"

    formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
    handler = logging.FileHandler(logging_commande + ".log", mode="a", encoding="utf-8")
    handler.setFormatter(formatter)
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info("START FABRIC-NMAP")
    logger.info("Version " + __version__)
    handerInfo = 'HOSTS: ', listhost, ' LOGIN: ', login
    logger.info(handerInfo)
    logger.info("COMMAND:" + command)
    logger.info('INPUT_FILE: ' + filecsv)

    startrun = time.time()

    if sudo_commande:
        if listhost:
            report = reportNetwork(listhost)
            if ping_commande:
                allhost = report.getPingUp()
            else:
                allhost = report.getNetwork()
        elif filecsv:
            inputfile = inputCsv(filecsv)
            allhost = inputfile.getHostToCsv()

        execHost(allhost, login, password, command, sudo_commande)

    elif ping_commande:
        report = reportNetwork(listhost)
        allhost = report.getPingUp()

        resultFyle = open(ping_commande + ".csv", 'wb')
        wr = csv.writer(resultFyle, dialect='excel')

        for hostPing in allhost:
            wr.writerow([hostPing, ])

    logger.info("END FABRIC-NMAP")
    logger.info("REPORT ****************************************************************")
    logger.info("TIMERUNNER: " + str((time.time() - startrun) / 60) + " min")
    logger.info("TOTAL: " + str(reportAction.count_total))
    logger.info("FAIL: " + str(reportAction.count_fail) + "/" + str(reportAction.count_total))
    logger.info("SUCCESS: " + str(reportAction.count_success) + "/" + str(reportAction.count_total))
    if reportAction.count_total != (reportAction.count_fail + reportAction.count_success):
        logger.critical("TOTAL_DIFF_ACTION: " + str((reportAction.count_fail + reportAction.count_success)))
    logger.debug(' HOSTS: '.join(allhost))
    logger.info("***********************************************************************")


if __name__ == "__main__":
    main()
