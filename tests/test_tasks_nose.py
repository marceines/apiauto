import unittest
import requests
from nose2.tools import params

"""
Test for nose2
"""


class Tasks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Setup Class only executed one time
        """
        print("Setup Class")
        cls.token = "e6a4ab6ecc9c4c8c5d0bf75d3b84871f3eb7f2cd"
        cls.headers = {
            "Authorization": "Bearer {}".format(cls.token)
        }
        cls.url_base = "https://api.todoist.com/rest/v2/tasks"

        # create task to be used in tests
        body_task = {
               "content":"mb test task",
               "due_string":"tomorrow at 12:00",
               "due_lang":"en",
               "priority":4
        }
        response = requests.post(cls.url_base, headers=cls.headers, data=body_task)

        cls.task_id = response.json()["id"]
        cls.task_id_update = ""
        cls.tasks_list = []


    def test_get_all_tasks(self):
        """
        Test get all tasks
        """
        response = requests.get(self.url_base, headers=self.headers)
        assert response.status_code == 200

    @params("Marce 2", "task 3", "task 4")
    def test_create_task(self, name_task):
        """
        Test for create task
        """
        self.name_task = []
        body_task = {
            "name": name_task,
            "due_string": "tomorrow at 12:00",
            "due_lang": "en",
            "priority": 4
        }
        response = requests.post(self.url_base, headers=self.headers, data=body_task)
        print(response.json())
        self.task_id_update = response.json()["id"]
        self.tasks_list.append(self.task_id_update)
        assert response.status_code == 200

    def test_get_task(self):
        """
        Test get tasks
        """
        url = f"{self.url_base}/{self.task_id}"
        response = requests.get(url, headers=self.headers)
        print(response.json())
        assert response.status_code == 200

    def test_delete_task(self):
        url = f"{self.url_base}/{self.task_id}"
        print(f"Test Delete: {self.task_id}")
        response = requests.delete(url, headers=self.headers)
        # validate task has been deleted
        assert response.status_code == 204

    def test_update_task(self):
        url = f"{self.url_base}/{self.task_id_update}"
        data_update = {
            "name": "task 2",
            "color": "red"
        }
        response = requests.post(url, headers=self.headers, data=data_update)
        print(response.json())
        assert response.status_code == 200

    @classmethod
    def tearDownClass(cls):
        print("tearDown Class")
        # delete tasks created
        for task in cls.tasks_list:
            url = f"{cls.url_base}/{task}"
            requests.delete(url, headers=cls.headers)
            print(f"Deleting task: {task}")