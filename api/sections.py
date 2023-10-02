import logging
import unittest

import requests

from api.todo_base import TodoBase
from api.validate_response import ValidateResponse
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Sections(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url_section = "https://api.todoist.com/rest/v2/sections"
        cls.url_projects= "https://api.todoist.com/rest/v2/projects"
        cls.session = requests.Session()
        cls.todo = TodoBase()
        cls.projects_list = []
        cls.section_list = []



    def test_create_session(self):
        """
        Test to create session
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
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="section")
        self.projects_list.append(project_id)


    def test_get_all_sections(self):
        """
        Test get all projects
        """
        response = RestClient().send_request("get", session=self.session, url=self.url_section,
                                             headers=HEADERS)
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                            feature="sections")

    def test_get_all_sections_by_project(self):
        url_sections = ""
        response = self.todo.get_all_projects()
        project_id = response["body"][0]["id"]
        if project_id:
            url_sections = f"{self.url_section}?project_id={project_id}"

        response = RestClient().send_request("get", session=self.session, url=url_sections,
                                             headers=HEADERS)
        self.projects_list.append(project_id)

    def test_get_section(self):
        response = self.todo.get_all_sections()
        section_id = response["body"][0]["id"]
        LOGGER.info("Section Id: %s", section_id)
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_section)

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
    def test_delete_section(self):

        response = self.todo.get_all_sections()
        section_id = response["body"][0]["id"]
        LOGGER.info("Section Id to delete : %s", section_id)
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS,
                                             url=url_section)



    @classmethod
    def tearDownClass(cls):
        print("tearDown Class")
        # delete projects created
        for project in cls.projects_list:
            url = f"{cls.url_projects}/{project}"
            RestClient().send_request(method_name="delete", session=cls.session, url=url,
                                      headers=HEADERS)
            LOGGER.info("Deleting project: %s", project)
