"""
(c) Copyright Jalasoft. 2023

projects.py
    configuration of logger file
"""
import logging
import unittest
import requests
from nose2.tools import params

from api.validate_response import ValidateResponse
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Projects(unittest.TestCase):
    """
    Class for projects endpoint
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup Class only executed one time
        """
        cls.url_base = "https://api.todoist.com/rest/v2/projects"
        cls.session = requests.Session()
        cls.project_id_update = ""
        cls.projects_list = []

    def test_get_all_projects(self):
        """
        Test get all projects
        """
        response = RestClient().send_request(method_name="get", session=self.session,
                                             url=self.url_base, headers=HEADERS)
        print(type(response))
        print(response)
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="projects")

    @params("Project 2", "1111111")
    def test_create_project(self, name_project):
        """
        Test for create project
        """
        body_project = {
            "name": name_project
        }
        response = RestClient().send_request("post", session=self.session, url=self.url_base,
                                             headers=HEADERS,
                                             data=body_project)
        LOGGER.info("Response for create project: %s", response["body"])
        project_id = response["body"]["id"]
        LOGGER.debug("Project id generated: %s", project_id)
        self.projects_list.append(project_id)
        ValidateResponse().validate_response(actual_response=response, method="post", expected_status_code=200,
                                             feature="project")

    def test_get_project(self):
        """
        Test get Project
        """
        project_created = self.create_project("Project X")
        project_id = project_created["body"]["id"]
        url = f"{self.url_base}/{project_id}"
        response = RestClient().send_request("get", session=self.session,
                                             url=url, headers=HEADERS)
        self.projects_list.append(project_id)
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="project")

    def test_delete_project(self):
        """
        Test delete project
        :return:
        """
        project_created = self.create_project("Project Delete")
        project_id = project_created["body"]["id"]
        url = f"{self.url_base}/{project_id}"
        response = RestClient().send_request(method_name="delete", session=self.session, url=url,
                                             headers=HEADERS)
        ValidateResponse().validate_response(actual_response=response, method="delete", expected_status_code=204,
                                             feature="project")

    def test_update_project(self):
        """
        Test update project
        :return:
        """
        project_created = self.create_project("Project Update")
        project_id_update = project_created["body"]["id"]
        url = f"{self.url_base}/{project_id_update}"
        data_update = {
            "name": "Project 2",
            "color": "red"
        }
        response = RestClient().send_request("post", session=self.session, url=url,
                                             headers=HEADERS, data=data_update)
        self.projects_list.append(project_id_update)
        ValidateResponse().validate_response(actual_response=response, method="post", expected_status_code=200,
                                             feature="project")

    def create_project(self, name_project):
        body_project = {
            "name": name_project
        }
        response = RestClient().send_request("post", session=self.session, url=self.url_base,
                                             headers=HEADERS, data=body_project)
        return response

    @classmethod
    def tearDownClass(cls):
        print("tearDown Class")
        # delete projects created
        for project in cls.projects_list:
            url = f"{cls.url_base}/{project}"
            RestClient().send_request(method_name="delete", session=cls.session, url=url,
                                      headers=HEADERS)
            LOGGER.info("Deleting project: %s", project)