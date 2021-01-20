import time
import unittest

import settings
from treehole_page_manager import TreeholePageManager
from hot_page_manager import HotPageManager
from selenium_api import *
from jandan_database import MyDB


class TestA1(unittest.TestCase):

    def setUp(self):
        self.driver = setup_driver('chrome', settings.chrome_driver_path)
        self.my_db = MyDB()
        pass

    def test_treehole_page(self):
        TreeholePageManager(self.my_db).parse_all_pages(self.driver, 67)
        print("-------------------------------------test end--------------------------------------------")
        time.sleep(10)

    def test_hot_page(self):
        HotPageManager(self.my_db).parse_all_pages(self.driver)
        print("-------------------------------------test end--------------------------------------------")
        time.sleep(10)

    def tearDown(self):
        # self.driver.close()
        pass


if __name__ == "__main__":
    unittest.main()
