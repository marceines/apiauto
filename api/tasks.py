import logging
import unittest

import requests

from api.todo_base import TodoBase
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Tasks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url_tasks = "https://api.todoist.com/rest/v2/tasks"
        cls.session = requests.Session()
        cls.todo = TodoBase()

    def test_create_task(self):

        response = self.create_task()


    def test_create_task_with_project_id(self):
        project_id_all = self.todo.get_all_projects()
        project_id = project_id_all["body"][0]["id"]
        response = self.create_task(project_id=project_id)

    def test_create_task_with_section_id(self):
        section_id_all = self.todo.get_all_sections()
        section_id = section_id_all["body"][0]["id"]
        response = self.create_task(section_id=section_id)

    def test_get_all_tasks(self):

        tasks_id_all = self.todo.get_all_tasks()

        LOGGER.info("Number of tasks returned: %s", len(tasks_id_all["body"]))

    def test_get_task_by_id(self):
        task_id_all = self.todo.get_all_tasks()
        task_id = task_id_all["body"][0]["id"]

        LOGGER.info("Task Id: %s", task_id)
        url_task = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS, url=url_task)
    def test_close_task(self):

        task_id_all = self.todo.get_all_tasks()
        task_id = task_id_all["body"][0]["id"]
        LOGGER.info("Task Id: %s", task_id)
        url_task_close = f"{self.url_tasks}/{task_id}/close"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task_close)

    def test_reopen_task(self):
        # valid task open
        task_created = self.create_task()
        task_id = task_created["body"]["id"]

        # close
        url_task_close = f"{self.url_tasks}/{task_id}/close"
        response_close = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                                   url=url_task_close)



        LOGGER.info("Task Id: %s", task_id)
        url_task_reopen = f"{self.url_tasks}/{task_id}/reopen"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task_reopen)

    def test_update_task(self):

        data = {
            "content": "Task Edited"
        }

        task_created = self.create_task()
        task_id = task_created["body"]["id"]
        LOGGER.info("Task Id: %s", task_id)
        url_task_update = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task_update, data=data)



    def test_delete_task(self):

        task_created = self.create_task()
        task_id = task_created["body"]["id"]
        LOGGER.info("Task Id: %s", task_id)
        url_task_update = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS,
                                             url=url_task_update)


    def create_task(self, project_id=None, section_id=None):
        data = {
            "content": "Task inside section",
            "due_string": "tomorrow at 12:00",
            "due_lang": "en",
            "priority": 4
        }
        if project_id:
            data["project_id"] = project_id
        if section_id:
            data["section_id"] = section_id

        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_tasks, data=data)

        return response