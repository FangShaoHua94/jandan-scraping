import json
import os
import urllib.request

from datetime import datetime

from hot_page import HotPage
from selenium_api import *
from settings import jandan_top_url


def default(o):
    if hasattr(o, 'to_json'):
        return o.to_json()
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')


class HotPageManager:

    def __init__(self, my_db):
        self.my_db = my_db

    def parse_all_pages(self, driver):
        path = self.create_sub_folder()
        navigate_to(driver, jandan_top_url)
        page = HotPage(driver)
        self.write_page(page, path)
        self.store_db(page)

    def create_sub_folder(self):
        # create sub-folder
        current_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        path = 'C:\\Users\\shaohua\\Desktop\\jandan-data\\hot\\' + str(current_datetime)
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s" % path)
            return path

    def write_page(self, page, path):
        file_name = path + '\\page_'  + '.txt'
        with open(file_name, 'w', encoding='utf8') as outfile:
            json.dump(page, outfile, default=default, indent=4, ensure_ascii=False)

        for post in page.post_list:
            for index, post_img_link in enumerate(post.post_img_link_list):
                file_name = path + '\\post_%s_img_%s' % (post.post_id, str(index))
                extension = '.' + self.get_extension(post_img_link)
                with open(file_name + extension, 'wb') as outfile:
                    outfile.write(urllib.request.urlopen(post_img_link).read())

    def get_extension(self, img_link):
        return img_link.rpartition('.')[2]

    def store_db(self, page):
        for post in page.post_list:
            self.write_post_to_db(post)
            for comment in post.comment_list:
                self.write_comment_to_db(comment)
            for hot_comment in post.hot_comment_list:
                self.write_comment_to_db(hot_comment)
            for index, post_img_link in enumerate(post.post_img_link_list):
                self.write_image_to_db(post.post_id, post_img_link, index)

    def write_post_to_db(self, post):
        sql = "INSERT INTO HotPost(post_id, post_time, post_user, post_oo, post_xx, post_comment_count, post_text) " \
              "VALUES (%(post_id)s, %(post_time)s, %(post_user)s, %(post_oo)s, %(post_xx)s, %(post_comment_count)s, %(post_text)s) " \
              "ON DUPLICATE KEY " \
              "UPDATE post_oo = %(post_oo)s, post_xx = %(post_xx)s, post_comment_count = %(post_comment_count)s, post_text = %(post_text)s"
        val = {'post_id': post.post_id,
               'post_time': post.post_time,
               'post_user': post.post_user,
               'post_oo': post.post_oo,
               'post_xx': post.post_xx,
               'post_comment_count': post.comment_count,
               'post_text': post.post_text,}
        self.my_db.execute_command(sql, val)
        self.my_db.commit()

    def write_comment_to_db(self, comment):
        sql = "INSERT INTO HotComment(comment_id, comment_user, comment_oo, comment_xx, Is_hot_comment, comment_text, post_id) " \
              "VALUES (%(comment_id)s, %(comment_user)s, %(comment_oo)s, %(comment_xx)s, %(is_hot_comment)s, %(comment_text)s,  %(post_id)s)" \
              "ON DUPLICATE KEY " \
              "UPDATE comment_oo = %(comment_oo)s, comment_xx = %(comment_xx)s, is_hot_comment = %(is_hot_comment)s, comment_text = %(comment_text)s"
        val = {'comment_id': comment.comment_id,
               'comment_user': comment.comment_user,
               'comment_oo': comment.comment_oo,
               'comment_xx': comment.comment_xx,
               'is_hot_comment': comment.is_hot_comment,
               'comment_text': comment.comment_text,
               'post_id': comment.post_id}
        self.my_db.execute_command(sql, val)
        self.my_db.commit()
    
    def write_image_to_db(self, post_id, image_link, index): 
        id = int(post_id) * 100 + index
        sql = "INSERT IGNORE INTO HotImage(id, post_id, link) VALUES (%(id)s, %(post_id)s, %(link)s)"
        val = {
            'id': id,
            'post_id': post_id,
            'link': image_link
        }
        self.my_db.execute_command(sql, val)
        self.my_db.commit()
         
