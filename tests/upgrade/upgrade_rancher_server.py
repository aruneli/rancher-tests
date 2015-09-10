import os
import argparse
import paramiko
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='target version')
    parser.add_argument('-s', help='server node')
    args = parser.parse_args()
    print args.t, args.s
    upgrade_rancher_server(args.t, args.s)


def upgrade_rancher_server(target, servernode):
    logger.info("\n ********* UPGRADING RANCHER SERVER "+servernode+" TO "+target+" ************* \n")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privatekeyfile = os.path.expanduser('~/.ssh/google_compute_engine')
    mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
    ssh.connect(servernode, username='aruneli', pkey=mykey)
    stdin, stdout, stderr = ssh.exec_command("sudo docker ps")
    response = stdout.readlines()
    logger.info(response)
    stdin, stdout, stderr = ssh.exec_command("sudo docker stop $(sudo docker ps -q | awk '{print $1}')")
    server_container_id = stdout.readlines()[0].strip("\n")
    logger.info(server_container_id)
    stdin, stdout, stderr = ssh.exec_command("sudo docker ps -a | awk ' NR>1 {print $2}' | cut -d \: -f 2 | cut -d \\v -f 2")
    tag_of_previous_rancher_server = stdout.readlines()[0].strip("\n")
    logger.info(tag_of_previous_rancher_server)
    cmd = "sudo docker create --volumes-from "+server_container_id+ " --name rancher-data rancher/server:v"+tag_of_previous_rancher_server
    stdin, stdout, stderr = ssh.exec_command(cmd)
    response = stdout.readlines()
    logger.info(response)
    cmd = "sudo docker pull rancher/server:v"+target
    stdin, stdout, stderr = ssh.exec_command(cmd)
    response = stdout.readlines()
    logger.info(response)
    cmd = "sudo docker run -d --volumes-from rancher-data --restart=always -p 8080:8080 rancher/server:v"+target
    stdin, stdout, stderr = ssh.exec_command(cmd)
    response = stdout.readlines()
    logger.info(response)
    # TO DO - make sure server is listening at port 8080
    time.sleep(60)
    logger.info("\n ********* UPGRADE OF RANCHER SERVER "+servernode+" TO "+target+" is complete ************* \n")
