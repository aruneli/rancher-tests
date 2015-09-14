import pytest
import inspect
import pickle
from tests.validation.cattlevalidationtest.core.common_fixtures import *  # NOQA
import re

class TestClass:
    bar = ""

    @pytest.mark.create
    @pytest.mark.run(order=1)
    def test_method1(self):
        TestClass.bar = 2
        print "bar is-", self.bar
        uuids = [1,2,3]
        #print "classname is:", str(self.__class__).split(".")[1]
        save(uuids,self)
    #
    # @pytest.mark.validate
    # @pytest.mark.run(order=2)
    # def test_method2(self):
    #     print "bar is ", self.bar
    #     uuids = load()
    #     print uuids


def save(uuids,self):
    # stack = inspect.stack()
    # frame = stack[1][0]
    # caller = frame.f_locals.get('self', None)
    # caller = str(caller)
    # print caller
    # classname = re.search(r'\.\w+\s', caller).group()[1:]
    classname = str(self.__class__).split(".")[1]
    print "classname is:", classname
    print "dat file: ", os.path.join(DAT_DIR, classname)
    with open(os.path.join(DAT_DIR, classname), 'wb') as handle:
            pickle.dump(uuids, handle)


def load():
    stack = inspect.stack()
    frame = stack[1][0]
    caller = frame.f_locals.get('self', None)
    caller = str(caller)
    print caller
    classname = re.search(r'\.\w+\s', caller).group()[1:]
    print classname
    print "dat file: ", os.path.join(DAT_DIR, classname)
    with open(os.path.join(DAT_DIR, classname), 'rb') as handle:
            uuids = pickle.load(handle)
            return uuids