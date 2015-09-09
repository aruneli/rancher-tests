import sys
import pickle
import os
import subprocess as sub
import argparse
import paramiko
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
import time
import tests.validation.cattlevalidationtest.serviceobjects



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', help='base version')
    parser.add_argument('-t', help='target version')
    parser.add_argument('-s', help='server node')
    args = parser.parse_args()
    print args.b, args.t, args.s
    upgrade_test(args.b, args.t, args.s)


def upgrade_test(base, target, servernode):
    print ("\n ********** CREATING SERVICES NOW IN BASE SETUP ********** \n")
    # TO-DO: Get the logs from below run
    os.system("py.test /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core/rancher_compose.py -v -m create -s")
    # Print global dict to make sure object created in base is stored
    #global serviceobject
    #(service, env) = serviceobject['TestRancherComposeLB']
    #print ("\n service and env before server upgrade: \n", service, env)
    global serviceobject
    serviceobject = tests.validation.cattlevalidationtest.serviceobjects.serviceobject
    print serviceobject
    upgrade_rancher_server(base, target, servernode)
    # Wait until rancher server is upgraded. If server upgrade failed, exit here with message
    # After rancher server is successfully upgraded,
    os.system("mkdir ../validation/cattlevalidationtest/core_target")
    os.system("mkdir ../../tmp")
    os.chdir("../../tmp")
    os.system("git clone -b "+target+" https://github.com/aruneli/rancher-tests.git")
    os.system("cp -r ../tests/validation/cattlevalidationtest/core/* ../tests/validation/cattlevalidationtest/core_target")
    # Print global dict to make sure object created in base is retained after server upgrade
    #print ("\n service and env after server upgrade: \n", service, env)
    #serviceobj = _get_service_object(serviceobject)
    # TO-DO: GET THE LIST OF SERVICES SUCCESSFULLY CREATED
    serviceobject = tests.validation.cattlevalidationtest.serviceobjects.serviceobject
    print serviceobject
    print ("\n ********** VALIDATING UPGRADED SETUP NOW WITH TARGET API ********** \n")
    os.system("py.test /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core_target/rancher_compose.py -v -m validate_created -s")


# def _get_service_object(serviceobject):
#     pkl_file = open('myfile.pkl', 'rb')
#     serviceobj = pickle.load(pkl_file)
#     pkl_file.close()
#     return serviceobj


def upgrade_rancher_server(base, target, servernode):
    logger.info("\n ********* UPGRADING RANCHER SERVER TO TARGET ************* \n")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privatekeyfile = os.path.expanduser('~/.ssh/google_compute_engine')
    mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
    ssh.connect(servernode, username='ubuntu', pkey=mykey)
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
    logger.info("\n ********* UPGRADE RANCHER SERVER TO TARGET COMPLETE ************* \n")


if __name__ == '__main__':
    main()









