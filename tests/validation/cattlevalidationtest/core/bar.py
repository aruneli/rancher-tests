import os
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from tests.validation.cattlevalidationtest.core.common_fixtures import *  # NOQA
import pickle

class Testing:
    def main(self):
        print "root dir is:", root_dir
        print os.path.exists(root_dir)
        #uuids = [1,2,3]
        #save(uuids,self)
        tmp_dir = os.path.join(root_dir, 'tmp')
        print tmp_dir
        os.mkdir(tmp_dir)
        core_dir = os.path.join(root_dir,'tests','validation','cattlevalidationtest','core')
        core_target_checkedout_dir = os.path.join(tmp_dir,'rancher-tests','tests','validation','cattlevalidationtests','core')
        core_target_dir = os.path.join(root_dir,'tests','validation','cattlevalidationtest','core_target')
        os.mkdir(core_target_dir)
        time.sleep(10)
        os.system("rm -rf "+tmp_dir)
        os.system("rm -rf "+core_target_dir)

    # os.system("mkdir ../../tmp")
    # os.chdir("../../tmp")
    # os.system(("cp -r /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core/* /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core_target/"))
    # os.system("py.test /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core/test_rancher_compose.py -v -m create -s")
    # time.sleep(10)
    # #upgrade_rancher_server(base, target, servernode)
    # #os.system("git clone -b master --single-branch https://github.com/aruneli/rancher-tests.git")
    # #os.system("cp /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core/* /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core_target/")
    # print ("\n ********** VALIDATING UPGRADED SETUP NOW WITH TARGET ********** \n")
    # os.system("py.test /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core_target/test_rancher_compose.py -v -m validate -s")
    # logger.info("\n *** VALIDATION COMPLETE *** \n")
    # os.chdir("../")
    # os.system("rm -rf tmp")
    # os.system("rm -rf /Users/aruneli/rancher/rancher-tests/tests/validation/cattlevalidationtest/core_target")

def save(uuids,obj):
    filename = str(obj.__class__).split(".")[-1:][0]
    print "filename is:",str(filename)
    print "full path:", os.path.join(root_dir,filename)
    with open(os.path.join(root_dir, filename), 'wb') as handle:
            pickle.dump(uuids, handle)


def load(self):
    filename = str(self.__class__).split(".")[-1:]
    print "filename is:",str(filename)
    print "full path:", os.path.join(root_dir, filename)
    with open(os.path.join(root_dir, filename), 'rb') as handle:
            uuids = pickle.load(handle)
            os.remove(os.path.join(root_dir, filename))
            return uuids


if __name__ == '__main__':
    testing = Testing()
    testing.main()
