# coding=utf-8
import unittest

__author__ = 'Lorenzo'

from test.test_base_class import *
from test.test_querying import *
from test.test_storedata import *
from test.test_querying_spatial import *
from test.test_formatdata import *
from test.test_datafiles import *
#from test.test_server import
#from test.test_webserver_query import


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestDataFiles))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestDataFormat))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestXco2TableClass))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(DBtestStoring))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestQuerying))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(DBareasSpatial))
    return s


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite())
