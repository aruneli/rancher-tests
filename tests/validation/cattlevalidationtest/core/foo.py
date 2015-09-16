# import pytest
# import inspect
# import pickle
# from tests.validation.cattlevalidationtest.core.common_fixtures import *  # NOQA
# import re
#
# class TestClass:
#     bar = ""
#
#     @pytest.mark.create
#     @pytest.mark.run(order=1)
#     def test_method1(self):
#         TestClass.bar = 2
#         print "git dir is:", git_root_dir
#         print "root dir is:", root_dir
#         print "bar is-", self.bar
#         uuids = [1,2,3]
#         print str(self.__class__)
#         print "classname is:", str(self.__class__).split(".")[-1:]
#         save(uuids,self)
#     #
#     # @pytest.mark.validate
#     # @pytest.mark.run(order=2)
#     # def test_method2(self):
#     #     print "bar is ", self.bar
#     #     uuids = load()
#     #     print uuids
#
#
# def save(uuids,obj):
#     filename = str(obj.__class__).split(".")[-1:]
#     print "filename is:",filename
#     with open(os.path.join(root_dir, filename), 'wb') as handle:
#             pickle.dump(uuids, handle)
#
#
# def load(self):
#     filename = str(self.__class__).split(".")[-1:]
#     print "filename is:",filename
#     with open(os.path.join(root_dir, filename), 'rb') as handle:
#             uuids = pickle.load(handle)
#             os.remove(os.path.join(git_root_dir, filename))
#             return uuids

import json
x = {'planet' : {'has': {'plants': 'yes', 'animals': 'yes', 'cryptonite': 'no'}, 'name': 'Earth'}}

print json.dumps(x, indent=2)