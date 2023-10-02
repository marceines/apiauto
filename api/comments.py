import logging
import unittest
from logging import Logger
from typing import Dict, Any

import requests

from api.todo_base import TodoBase
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER: Logger = get_logger(__name__, logging.DEBUG)


class Comments(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url_comments = "https://api.todoist.com/rest/v2/comments"
        cls.session = requests.Session()
        cls.todo = TodoBase()


    def test_get_all_comments_with_task_id(self):
        response = self.get_comments_task()
        LOGGER.info("Number of comments returned: %s", len(response["body"]))

    def test_get_all_comments_by_project_id(self):
        all_projects = self.todo.get_all_projects()
        project_id = all_projects["body"][0]["id"]
        url_comments_project = f"{self.url_comments}?project_id={project_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS, url=url_comments_project)
        LOGGER.info("Number of comments returned: %s", len(response["body"]))

    def test_create_comment_on_task(self):
        task_id_all = self.todo.get_all_tasks()
        task_id = task_id_all["body"][0]["id"]
        data = {
            "task_id": task_id,
            "content": "New comment from API 2"
        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_comments, data=data)
        LOGGER.info("Comment id ", response["body"])

    def test_create_comment_on_project(self):
        all_projects = self.todo.get_all_projects()
        project_id = all_projects["body"][0]["id"]
        data = {
            "project_id": project_id,
            "content": "New comment MB"
        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_comments, data=data)
        LOGGER.info("Comment Id: %s", response["body"])

    def test_get_comment_on_task(self):
        comments = self.get_comments_task()
        comment_id = comments["body"][0]
        url_comment = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_comment)

    def test_update_comment_on_task(self):
        data = {
            "content": "Comment edited"
        }
        comments = self.get_comments_task()
        comment_id = comments["body"][0]
        LOGGER.info("Comment id to edit: ", comment_id)
        url_comment = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_comment, data=data)

    def test_delete_comment_on_task(self):
        comments = self.get_comments_task()
        comment_id = comments["body"][0]
        LOGGER.info("Comment id to delete: ", comment_id)
        url_comment = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS,
                                             url=url_comment)

    def get_comments_task(self):
        task_id_all = self.todo.get_all_tasks()
        task_id = task_id_all["body"][0]["id"]
        url_comments_by_task = f"{self.url_comments}?task_id={task_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                                               url=url_comments_by_task)

        return response