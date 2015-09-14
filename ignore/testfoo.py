import os
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def main():
    # print ("\n **********   CREATING SERVICES NOW IN BASE SETUP  ********** \n")
    # os.system("py.test /Users/aruneli/rancher/rancher-tests/ignore/test_foo.py -v -m create -s")
    # #upgrade_rancher_server(base, target, servernode)
    # os.system("mkdir /Users/aruneli/rancher/rancher-tests/ignore_target")
    # os.system("mkdir /Users/aruneli/rancher/rancher-tests/tmp")
    # os.chdir("/Users/aruneli/rancher/rancher-tests/tmp")
    # os.system("cp -r /Users/aruneli/rancher/rancher-tests/ignore/* /Users/aruneli/rancher/rancher-tests/ignore_target/")
    # print ("\n ********** VALIDATING UPGRADED SETUP NOW WITH TARGET ********** \n")
    # os.system("py.test /Users/aruneli/rancher/rancher-tests/ignore_target/test_foo.py -v -m validate -s")
    # logger.info("\n *** VALIDATION COMPLETE *** \n")
    # os.chdir("../")
    # os.system("rm -rf /Users/aruneli/rancher/rancher-tests/tmp")
    # os.system("rm -rf /Users/aruneli/rancher/rancher-tests/ignore_target")
    os.system("rm -rf /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core_target")



if __name__ == '__main__':
    main()
