import argparse
import logging
import subprocess as process
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
from tests.validation.cattlevalidationtest.core.common_fixtures import *  # NOQA
from docker import Client
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='target version')
    parser.add_argument('-s', help='server node')
    args = parser.parse_args()
    logger.info(args)
    #upgrade(args.t, args.s)
    #current_rancher_server_version(args.s)
    upgrade(args.t, args.s)

def upgrade(target, server):
    cli = Client(base_url="http://130.211.189.242:5555")
    cli.containers()


def current_rancher_server_version(server):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privatekeyfile = os.path.expanduser('~/.ssh/google_compute_engine')
    mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
    ssh.connect(server, username='aruneli', pkey=mykey)
    stdin, stdout, stderr = ssh.exec_command("sudo docker ps -a | awk ' NR>1 {print $2}' | cut -d \: -f 2 | cut -d \\v -f 2")
    tag_of_rancher_server = stdout.readlines()[0].strip("\n")
    logger.info(tag_of_rancher_server)

def upgrade(target, servernode):
    # logger.info("\n ********* UPGRADING RANCHER SERVER TO TARGET ************* \n")
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # privatekeyfile = os.path.expanduser('~/.ssh/google_compute_engine')
    # mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
    # ssh.connect(servernode, username='aruneli', pkey=mykey)
    # stdin, stdout, stderr = ssh.exec_command("sudo docker ps")
    # response = stdout.readlines()
    # logger.info(response)
    # stdin, stdout, stderr = ssh.exec_command("sudo docker stop $(sudo docker ps -q | awk '{print $1}')")
    # server_container_id = stdout.readlines()[0].strip("\n")
    # logger.info(server_container_id)
    # stdin, stdout, stderr = ssh.exec_command("sudo docker ps -a | awk ' NR>1 {print $2}' | cut -d \: -f 2 | cut -d \\v -f 2")
    # tag_of_previous_rancher_server = stdout.readlines()[0].strip("\n")
    # logger.info(tag_of_previous_rancher_server)
    # cmd = "sudo docker create --volumes-from "+server_container_id+ " --name rancher-data rancher/server:v"+tag_of_previous_rancher_server
    # stdin, stdout, stderr = ssh.exec_command(cmd)
    # response = stdout.readlines()
    # logger.info(response)
    # cmd = "sudo docker pull rancher/server:v"+target
    # stdin, stdout, stderr = ssh.exec_command(cmd)
    # response = stdout.readlines()
    # logger.info(response)
    # cmd = "sudo docker run -d --volumes-from rancher-data --restart=always -p 8080:8080 rancher/server:v"+target
    # stdin, stdout, stderr = ssh.exec_command(cmd)
    # response = stdout.readlines()
    # logger.info(response)
    # stdin, stdout, stderr = ssh.exec_command("sudo docker ps | awk ' NR>1 {print $2}' | cut -d \: -f 2| cut -d \\v -f 2")
    # tag_of_rancher_version_after_upgrade= stdout.readlines()[0].strip("\n")
    # print "tag_of_rancher_version_after_upgrade is:", tag_of_rancher_version_after_upgrade
    # time.sleep(10)
    # stdin, stdout, stderr = ssh.exec_command("sudo docker ps | awk ' NR>1 {print $8}' ")
    # state_of_rancher_server_container_after_upgrade = stdout.readlines()[0].strip("\n")
    # print "state_of_rancher_server_container_after_upgrade is:", state_of_rancher_server_container_after_upgrade
    tag_of_rancher_version_after_upgrade = "0.37.0"
    state_of_rancher_server_container_after_upgrade = "Up"
    if tag_of_rancher_version_after_upgrade == target and state_of_rancher_server_container_after_upgrade == "Up":
        server = 'http://'+servernode+":8080"
        if requests.get(server).status_code == 200:
            print "\n ********* UPGRADE RANCHER SERVER TO TARGET COMPLETE ************* \n"
    time.sleep(90)

if __name__ == '__main__':
    main()
