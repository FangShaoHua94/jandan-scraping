import time
import unittest

import settings
from page_manager import PageManager
from selenium_api import *
from jandan_database import MyDB


class TestA1(unittest.TestCase):

    def setUp(self):
        self.driver = setup_driver('chrome', settings.chrome_driver_path)
        self.my_db = MyDB()
        pass

    def test_xxx(self):
        page_manager = PageManager(self.my_db).parse_all_pages(self.driver, 60)
        print("-------------------------------------test end--------------------------------------------")
        time.sleep(10)

        pass

    def tearDown(self):
        # self.driver.close()
        pass


if __name__ == "__main__":
    unittest.main()
