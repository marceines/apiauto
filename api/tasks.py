import logging
import unittest

import requests

from api.validate_response import ValidateResponse
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
        cls.tasks_list = []

    def test_create_task(self):

        response = self.create_task()
        LOGGER.debug("Task id generated: %s", response["body"]["id"])
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="task")



    def test_create_task_with_project_id(self):
        project_id_all = self.todo.get_all_projects()
        project_id = project_id_all["body"][0]["id"]
        response = self.create_task(project_id=project_id)
        LOGGER.info("tasks created: %s", len(response["body"]))
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="task")

    def test_create_task_with_section_id(self):
        section_id_all = self.todo.get_all_sections()
        section_id = section_id_all["body"][0]["id"]
        response = self.create_task(section_id=section_id)
        LOGGER.info("tasks created: %s", len(response["body"]))
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="task")

    def test_get_all_tasks(self):

        tasks_id_all = self.todo.get_all_tasks()
        LOGGER.info("Getting all tasks")
        ValidateResponse().validate_response(actual_response=tasks_id_all, method="get", expected_status_code=200,
                                             feature="tasks")

    def test_get_task_by_id(self):
        task_id_all = self.todo.get_all_tasks()
        task_id = task_id_all["body"][0]["id"]

        LOGGER.info("Task Id: %s", task_id)
        url_task = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS, url=url_task)
        LOGGER.info("Get task id: %s", len(response["body"]))
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="task")
    def test_close_task(self):

        task_id_all = self.todo.get_all_tasks()
        task_id = task_id_all["body"][0]["id"]
        LOGGER.info("Task Id: %s", task_id)
        url_task_close = f"{self.url_tasks}/{task_id}/close"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task_close)
        LOGGER.info("task closed id: %s", task_id)



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
        ValidateResponse().validate_response(actual_response=response, method="delete", expected_status_code=204,
                                             feature="task")
        self.tasks_list.append(task_id)

    def test_update_task(self):

        data = {
            "content": "Task Edited"
        }

        task_created = self.create_task()
        task_id = task_created["body"]["id"]
        LOGGER.info("Task created to editId: %s", task_id)
        url_task_update = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task_update, data=data)
        self.tasks_list.append(task_id)
        LOGGER.info("Update task id: %s", task_id)
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="task")



    def test_delete_task(self):

        task_created = self.create_task()
        task_id = task_created["body"]["id"]
        LOGGER.info("Task Id: %s", task_id)
        url_task_update = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS,
                                             url=url_task_update)
        ValidateResponse().validate_response(actual_response=response, method="delete", expected_status_code=204,
                                             feature="task")


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
    @classmethod
    def tearDownClass(cls):
        print("tearDown Class")
        # delete projects created
        for task in cls.tasks_list:
            url = f"{cls.url_tasks}/{task}"
            RestClient().send_request(method_name="delete", session=cls.session, url=url,
                                      headers=HEADERS)
            LOGGER.info("Deleting tasks: %s", task)