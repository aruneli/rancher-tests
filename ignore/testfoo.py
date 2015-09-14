import os
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import time

def main():
    QA_ROOT_DIR = "/Users/aruneli/rancher/rancher-tests"
    os.system("mkdir /validation/cattlevalidationtest/core_target")
    os.system("mkdir ../../tmp")
    os.chdir("../../tmp")
    os.system(("cp -r /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core/* /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core_target/"))
    os.system("py.test /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core/test_rancher_compose.py -v -m create -s")
    time.sleep(10)
    #upgrade_rancher_server(base, target, servernode)
    #os.system("git clone -b master --single-branch https://github.com/aruneli/rancher-tests.git")
    #os.system("cp /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core/* /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core_target/")
    print ("\n ********** VALIDATING UPGRADED SETUP NOW WITH TARGET ********** \n")
    os.system("py.test /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core_target/test_rancher_compose.py -v -m validate -s")
    logger.info("\n *** VALIDATION COMPLETE *** \n")
    os.chdir("../")
    os.system("rm -rf tmp")
    os.system("rm -rf /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core_target")



if __name__ == '__main__':
    main()
