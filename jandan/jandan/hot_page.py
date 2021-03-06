from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from selenium_api import *
from utils import *


class HotPage:
    __post_locator = (By.XPATH, '//ol[@class="commentlist"]/li[contains(@id, "comment")]')
    __open_comment_locator = (By.XPATH, '//div[@class="jandan-vote"]/a[@class="tucao-btn"]')

    __bad_content_locator = (By.XPATH, '//a[@class="view_bad"]')

    def __init__(self, driver, parse=True):
        self.url = driver.current_url
        if parse:
            self.open_bad_content(driver)
            self.post_list = self.parse_post_list(driver)

    def parse_post_list(self, driver):
        print("Parsing post list...")
        post_list = []
        post_elements = wait_for_elements_present(driver, self.__post_locator, 'Obtaining posts...')
        for post_element in post_elements:
            post = self.HotPost(post_element, driver)
            post_list.append(post)
            print(post)
        # self.write_to_json(post_list)
        return post_list

    def open_bad_content(self, driver):
        try:
            bad_content_elements = wait_for_elements_present(driver, self.__bad_content_locator, timeout=3)
            for bad_content_element in bad_content_elements:
                scroll_to_element(driver, bad_content_element)
                bad_content_element.click()
        except TimeoutException:
            print("No bad content in this page.")

    def __eq__(self, other):
        if isinstance(other, HotPage):
            return self.url == other.url
        return False

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_json(self):
        return self.__dict__

    class HotPost:
        __user_locator = (By.XPATH, './b')
        __time_locator = (By.XPATH, './span[@class="time"]')
        __text_locator = (By.XPATH, './div[@class="commenttext"]/p')
        __oo_locator = (By.XPATH,
                        './div[@class="jandan-vote"]//a[@class="comment-like like"]/following-sibling::span')
        __xx_locator = (By.XPATH,
                        './div[@class="jandan-vote"]//a[@class="comment-unlike unlike"]/following-sibling::span')
        __comment_count_locator = (By.XPATH, './/a[@class="tucao-btn"]')
        __open_comment_locator = (By.XPATH, './div[@class="jandan-vote"]/a[@class="tucao-btn"]')

        __hot_comment_locator = (By.XPATH, './/div[@class="tucao-hot"]/div[@class="tucao-row"]')
        __comment_locator = (By.XPATH, './/div[@class="tucao-list"]/div[@class="tucao-row"]')

        __image_locator = (By.XPATH, './div[@class="commenttext"]/p/a[@class="view_img_link"]')

        def __init__(self, post_element, driver):
            self.post_user, self.post_time, self.post_id, self.post_oo, self.post_xx, self.post_text, self.post_img_link_list, self.comment_count, self.hot_comment_list, self.comment_list = self.parse_post(
                post_element, driver)

        def parse_post(self, post_element, driver):
            print("Parsing post...")
            post_user = wait_for_element_present(post_element, self.__user_locator).text
            post_time = wait_for_element_present(post_element, self.__time_locator).text.strip()[2:]
            post_id = post_element.get_attribute('id')[8:]
            post_oo = wait_for_element_present(post_element, self.__oo_locator).text
            post_xx = wait_for_element_present(post_element, self.__xx_locator).text

            post_text = ''
            post_text_elements = wait_for_elements_present(post_element, self.__text_locator)
            for post_text_element in post_text_elements:
                post_text += '\n' + post_text_element.text

            post_img_link_list = []
            try:
                post_img_link_elements = wait_for_elements_present(post_element, self.__image_locator, timeout=3)
                for post_img_link_element in post_img_link_elements:
                    link = post_img_link_element.get_attribute('href')
                    post_img_link_list.append(link)
            except:
                pass

            comment_list = []
            hot_comment_list = []

            comment_count = self.parse_comment_count(post_element)
            if comment_count != '0':
                self.open_comment_section(post_element, driver)
                print("Parsing comments...")
                comment_elements = wait_for_elements_present(post_element, self.__comment_locator)
                for comment_element in comment_elements:
                    comment = self.HotComment(comment_element, post_id)
                    comment_list.append(comment)
                # list(set(comment_list))

                try:
                    print("Parsing hot comments...")
                    hot_comment_elements = wait_for_elements_present(post_element, self.__hot_comment_locator,
                                                                     timeout=1)
                    for hot_comment_element in hot_comment_elements:
                        hot_comment = self.HotComment(hot_comment_element, post_id, is_hot_comment=True)
                        hot_comment_list.append(hot_comment)

                    # list(set(hot_comment_list))
                except TimeoutException:
                    pass

            return post_user, post_time, post_id, post_oo, post_xx, post_text, post_img_link_list, comment_count, hot_comment_list, comment_list

        def parse_comment_count(self, post_element):
            comment_count_string = wait_for_element_present(post_element, self.__comment_count_locator).text
            return retain_number(comment_count_string)

        def open_comment_section(self, post_element, driver):
            print("Opening comment section...")
            element = wait_for_element_present(post_element, self.__open_comment_locator)
            scroll_to_element(driver, element)
            element.click()
            # scroll_to_and_click_button(post_element, self.__open_comment_locator)

        def __eq__(self, other):
            if isinstance(other, HotPage.HotPost):
                return self.post_id == other.post_id
            return False

        def __str__(self):
            return str(self.__dict__)

        def __repr__(self):
            return str(self.__dict__)

        def to_json(self):
            return self.__dict__

        class HotComment:

            __user_locator = (By.XPATH, './/div[@class="tucao-author"]/span')
            __id_locator = (By.XPATH, './/span[@class="tucao-id"]')
            __text_locator = (By.XPATH, './/div[@class="tucao-content"]')
            __oo_locator = (By.XPATH, './/span[@class="tucao-oo"]')
            __xx_locator = (By.XPATH, './/span[@class="tucao-xx"]')

            def __init__(self, comment_element, post_id, is_hot_comment=False, ):
                self.comment_user, self.comment_id, self.comment_oo, self.comment_xx, self.comment_text = self.parse_comment(
                    comment_element)
                self.is_hot_comment = is_hot_comment
                self.post_id = post_id

            def parse_comment(self, comment_element):
                comment_user = wait_for_element_present(comment_element, self.__user_locator).text
                comment_id = wait_for_element_present(comment_element, self.__id_locator).text[1:]
                comment_text = ''
                comment_text_elements = wait_for_elements_present(comment_element, self.__text_locator)
                for comment_text_element in comment_text_elements:
                    comment_text += '\n' + comment_text_element.text

                comment_oo = wait_for_element_present(comment_element, self.__oo_locator).text
                comment_xx = wait_for_element_present(comment_element, self.__xx_locator).text
                return comment_user, comment_id, comment_oo, comment_xx, comment_text

            def __eq__(self, other):
                if isinstance(other, HotPage.HotPost.HotComment):
                    return self.comment_id == other.comment_id
                return False

            def __str__(self):
                return str(self.__dict__)

            def __repr__(self):
                return str(self.__dict__)

            def to_json(self):
                return self.__dict__
