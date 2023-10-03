import logging
import unittest

import requests

from api.validate_response import ValidateResponse
from api.todo_base import TodoBase
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Sections(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url_section = "https://api.todoist.com/rest/v2/sections"
        cls.url_projects = "https://api.todoist.com/rest/v2/sections"
        cls.session = requests.Session()
        cls.todo = TodoBase()
        cls.projects_list = []

    def test_create_section(self):
        """
        Test to create section
        :return:
        """

        project_created = self.todo.create_project("Project for section")
        project_id = project_created["body"]["id"]
        body_section = {
            "project_id": project_id,
            "name": "Section created by MB"
        }

        response = RestClient().send_request("post", session=self.session, url=self.url_section,
                                             headers=HEADERS, data=body_section)
        LOGGER.debug("Section id generated: %s", response["body"]["id"])
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="section")
        self.projects_list.append(project_id)
    def test_get_all_sections(self):
        """
        Test get all sections
        """
        response = RestClient().send_request("get", session=self.session, url=self.url_section,
                                             headers=HEADERS)
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                            feature="sections")


    def test_get_all_sections_by_project(self):
        project_id_all = self.todo.get_all_projects()
        project_id = project_id_all["body"][0]["id"]
        if project_id:
            url_section = f"{self.url_section}?project_id={project_id}"

        response = RestClient().send_request("get", session=self.session, url=self.url_section,
                                             headers=HEADERS)
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                            feature="sections")

    def test_get_section(self):
        response = self.todo.get_all_sections()
        section_id = response["body"][0]["id"]
        LOGGER.info("Section Id: %s", section_id)
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_section)
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="section")


    def test_update_section(self):
        data = {
            "name": "Section Edited"
        }
        response = self.todo.get_all_sections()
        section_id = response["body"][0]["id"]
        LOGGER.info("Section Id edited : %s", section_id)
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_section, data=data)
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="section")


    def test_delete_section(self):

        project_created_to_sections = self.todo.create_project("Project for section")
        project_id = project_created_to_sections["body"]["id"]
        body_section = {
            "project_id": project_id,
            "name": "Section created by MB"
        }
        response = RestClient().send_request("post", session=self.session, url=self.url_section,
                                             headers=HEADERS, data=body_section)
        section_id = response["body"]["id"]
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS,
                                             url=url_section)
        ValidateResponse().validate_response(actual_response=response, method="delete", expected_status_code=204,
                                             feature="project")
        self.projects_list.append(project_id)

    @classmethod
    def tearDownClass(cls):
        print("tearDown Class")
        # delete projects created
        for project in cls.projects_list:
            url = f"{cls.url_projects}/{project}"
            RestClient().send_request(method_name="delete", session=cls.session, url=url,
                                      headers=HEADERS)
            LOGGER.info("Deleting project: %s", project)