import requests

from config.config import HEADERS
from utils.rest_client import RestClient
from utils.singleton import Singleton
from api.validate_response import ValidateResponse


class TodoBase(metaclass=Singleton):

    def __init__(self):
        self.url_projects = "https://api.todoist.com/rest/v2/projects"
        self.url_sections = "https://api.todoist.com/rest/v2/sections"
        self.url_tasks = "https://api.todoist.com/rest/v2/tasks"
        self.session = requests.Session()

    def get_all_projects(self):
        """

        :return:
        """
        response = RestClient().send_request(method_name="get", session=self.session,
                                             url=self.url_projects, headers=HEADERS)
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="projects")

        return response

    def create_project(self, name_project):
        body_project = {
            "name": name_project
        }
        response = RestClient().send_request("post", session=self.session, url=self.url_projects,
                                             headers=HEADERS, data=body_project)
        return response

    def get_all_sections(self):
        response = RestClient().send_request("get", session=self.session,
                                             url=self.url_sections, headers=HEADERS)

        return response