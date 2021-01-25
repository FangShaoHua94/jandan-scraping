import mysql.connector
from pymongo import MongoClient

import os

from dotenv import load_dotenv


class MyDB:

    def __init__(self):
        load_dotenv()
        self.my_db = mysql.connector.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            charset="utf8mb4",
            database=os.getenv('DATABASE'),
        )
        self.my_cursor = self.my_db.cursor()

    def execute_command(self, sql, val):
        self.my_cursor.execute(sql, val)

    def commit(self):
        self.my_db.commit()



# my_db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="fshs9475089z",
#     charset="utf8",
#     database="jandan_database",
# )
#
# my_cursor = my_db.cursor()
#
# my_cursor.execute("INSERT INTO Comment(Comment_id, Comment_user, Comment_oo, Comment_xx, Is_hot_comment, Comment_text, Post_id) " \
#               "VALUES (802110411, 'abc', 20, 50, False, 'abcde', 4784297) ")
#               # "ON DUPLICATE KEY UPDATE Comment_oo = 100, Comment_xx = 200, Is_hot_comment = False")

# my_cursor.execute("Create TABLE Post ("
#                   "Post_id INT PRIMARY KEY NOT NULL, "
#                   "Post_time DATETIME NOT NULL, "
#                   "Post_user TEXT NOT NULL, "
#                   "Post_oo INT NOT NULL, "
#                   "Post_xx INT NOT NULL, "
#                   "Post_comment_count INT NOT NULL, "
#                   "Post_text TEXT NOT NULL)")
#
# my_cursor.execute("Create TABLE Comment ("
#                   "Comment_id INT PRIMARY KEY NOT NULL, "
#                   "Comment_user TEXT NOT NULL, "
#                   "Comment_oo INT NOT NULL, "
#                   "Comment_xx INT NOT NULL, "
#                   "Is_hot_comment BOOL NOT NULL, "
#                   "Comment_text TEXT NOT NULL, "
#                   "Post_id INT NOT NULL, "
#                   "FOREIGN KEY (Post_id) REFERENCES Post(Post_id))")


