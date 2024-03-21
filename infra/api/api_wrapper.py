import requests
import logging
from Utils.json_reader import get_config_data
from Utils.logging_setup import setup_logging
from infra.jira_client import *

class APIWrapper:

    def __init__(self):
        self.response = None
        self.my_request = requests
        self.config = get_config_data()
        setup_logging()
        self.logger = logging.getLogger(__name__)

    def api_get_request(self, url, body=None, header=None):
        self.logger.info(f"Making GET request to {url} with body: {body}")
        self.response = self.my_request.get(url, params=body, headers=header)
        self.logger.info(f"Received response: {self.response.status_code}")
        return self.response

    def api_post_request(self, url, body=None, header=None):
        self.logger.info(f"Making POST request to {url} with body: {body}")
        self.response = self.my_request.post(url, json=body, headers=header)
        self.logger.info(f"Received response: {self.response.status_code}")
        return self.response

    def api_put_request(self, url, body=None, header=None):
        self.logger.info(f"Making PUT request to {url} with body: {body}")
        self.response = self.my_request.put(url, json=body, headers=header)
        self.logger.info(f"Received response: {self.response.status_code}")
        return self.response

    def api_delete_request(self, url, header=None):
        self.logger.info(f"Making DELETE request to {url}")
        self.response = self.my_request.delete(url=url, headers=header)
        self.logger.info(f"Received response: {self.response.status_code}")
        return self.response

    def api_patch_request(self, url, body=None, header=None):
        self.logger.info(f"Making PATCH request to {url} with body: {body}")
        self.response = self.my_request.patch(url, json=body, headers=header)
        self.logger.info(f"Received response: {self.response.status_code}")
        return self.response

