# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from datetime import datetime
from models.blog_post import BlogPost


memory_data = [
                BlogPost(1,'Red flowers', 'text about red flowers','User1',datetime.now()),
                BlogPost(2,'Yellow flowers', 'text about yellow flowers','User2',datetime.now()),
                BlogPost(3,'Blue flowers', 'text about blue flowers','User3',datetime.now())
                ]
