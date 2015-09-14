from tests.validation.cattlevalidationtest.core.common_fixtures import *  # NOQA
import os
import argparse
import paramiko
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
import time
import requests
import shutil

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', help='base version')
    parser.add_argument('-t', help='target version')
    parser.add_argument('-s', help='server node')
    args = parser.parse_args()
    print args.b, args.t, args.s
    upgrade_test(args.b, args.t, args.s)


def upgrade_test(base, target, servernode):
    print ("\n ********** CREATING SERVICES NOW IN BASE SETUP  ********** \n")
    tmp_dir = os.path.join(root_dir, 'tmp')
    os.mkdir(tmp_dir)
    core_dir = os.path.join(root_dir,'tests','validation','cattlevalidationtest','core')
    core_target_checkedout_dir = os.path.join(tmp_dir,'rancher-tests','tests','validation','cattlevalidationtests','core')
    core_target_dir = os.path.join(root_dir,'tests','validation','cattlevalidationtest','core_target')
    os.mkdir(core_target_dir)
    #os.system("git clone -b master --single-branch https://github.com/aruneli/rancher-tests.git <tmp>")
    #try:
        #shutil.copy(core_target_checkedout_dir,core_target_dir)
    # Directories are the same
    # except shutil.Error as e:
    #     print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    # except OSError as e:
    #     print('Directory not copied. Error: %s' % e)

    #below is for quick dummy test
    try:
        shutil.copy(core_dir, core_target_dir)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)
    create_cmd = "py.test "+core_dir+" -v -m create -s"
    os.system(create_cmd)
    time.sleep(5)
    upgrade_rancher_server(base, target, servernode)
    print ("\n ********** VALIDATING UPGRADED SETUP NOW WITH TARGET ********** \n")
    validate_cmd = "py.test "+core_target_dir+" -v -m validate -s"
    os.system(validate_cmd)
    logger.info("\n *** VALIDATION COMPLETE *** \n")
    os.rmdir(tmp_dir)
    os.rmdir(core_target_dir)


def upgrade_rancher_server(base, target, servernode):
    logger.info("\n ********* UPGRADING RANCHER SERVER TO TARGET *********** \n")
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
    stdin, stdout, stderr = ssh.exec_command("sudo docker ps | awk ' NR>1 {print $2}' | cut -d \: -f 2| cut -d \\v -f 2")
    tag_of_rancher_version_after_upgrade= stdout.readlines()[0].strip("\n")
    print "tag_of_rancher_version_after_upgrade is:", tag_of_rancher_version_after_upgrade
    time.sleep(10)
    stdin, stdout, stderr = ssh.exec_command("sudo docker ps | awk ' NR>1 {print $8}' ")
    state_of_rancher_server_container_after_upgrade = stdout.readlines()[0].strip("\n")
    print "state_of_rancher_server_container_after_upgrade is:", state_of_rancher_server_container_after_upgrade
    if tag_of_rancher_version_after_upgrade == target and state_of_rancher_server_container_after_upgrade == "Up":
        server = 'http://'+servernode+":8080"
        if requests.get(server).status_code == 200:
            logger.info("\n ********* UPGRADE RANCHER SERVER TO TARGET COMPLETE AND SUCCESSFUL ************* \n")
    time.sleep(90)


if __name__ == '__main__':
    main()
