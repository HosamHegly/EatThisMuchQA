import os
from dotenv import load_dotenv
from jira import JIRA

import config
import json
from Utils.json_reader import get_config_data

# Load environment variables

def connect_jira():
    from pathlib import Path

    load_dotenv()
    config = get_config_data()
    token = os.getenv("TOKEN")
    jira_url = config["jira-server"]
    jira_user = config["jira-user"]

    return JIRA(basic_auth=(jira_user, token), options={"server": jira_url})


class JiraClient:
    def __init__(self):
        self.auth_jira = connect_jira()

    def create_issue(self, summary, description, project_key="NEW", issue_type="Bug"):
        issue_dict = {
            'project': {'key': project_key},
            'summary': f'Failed test: {summary}',
            'description': description,
            'issuetype': {'name': issue_type},
        }
        new_issue = self.auth_jira.create_issue(fields=issue_dict)
        return new_issue.key

