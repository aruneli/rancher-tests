import sys
import pickle
import os
import subprocess

serviceobject = {}

def main():
    base = sys.argv[0]
    target = sys.argv[1]
    upgrade_test(base, target)


def upgrade_test(base, target):

    print ("\n ********** CREATING SERVICES NOW IN BASE SETUP ********** \n")
    # TO-DO: Get the logs from below run
    os.system("py.test /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core/rancher_compose.py -v -m create -s")
    # Print global dict to make sure object created in base is stored
    global serviceobject
    print ("\n object state before server upgrade: \n")
    serviceobj = _get_service_object(serviceobject)
    print serviceobj
    upgrade_rancher_server(target)
    # Wait until rancher server is upgraded
    # After rancher server is successfully upgraded,
    # "make -C <../validation/cattlevalidationtest/core_target>"
    # "git -C <../validation/cattlevalidationtest/core_target>"
    # git fetch {remote}
    # git checkout FETCH_HEAD -- {files}
    # Now a folder names core_target is created with libraries from target version
    # Print global dict to make sure object created in base is retained after server upgrade
    print ("\n object state after server upgrade: \n\n")
    serviceobj = _get_service_object(serviceobject)
    print serviceobj
    # TO-DO: GET THE LIST OF SERVICES SUCCESSFULLY CREATED
    print ("\n ********** VALIDATING UPGRADED SETUP NOW WITH TARGET API ********** \n")
    os.system("py.test /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core_target/rancher_compose.py -v -m validate_created -s")


def _get_service_object(serviceobject):
    pkl_file = open('myfile.pkl', 'rb')
    serviceobj = pickle.load(pkl_file)
    pkl_file.close()
    return serviceobj


def upgrade_rancher_server(target):
    print "\n ********* UPGRADING RANCHER SERVER TO TARGET ************* \n"

if __name__ == '__main__':
  main()









