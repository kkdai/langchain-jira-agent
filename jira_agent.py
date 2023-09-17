import os
from jira import JIRA
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool


jira_server = os.getenv('JIRA_INSTANCE_URL', None)
jira_username = os.getenv('JIRA_USERNAME', None)
jira_password = os.getenv('JIRA_API_TOKEN', None)

class SearchIssueInput(BaseModel):
    """Search Jira issue input parameters."""
    # project_key: str = Field(..., description="The key of the project")
    issue_title: str = Field(..., description="The title of the issue")

class JiraSearchTool(BaseTool):
    name = "search_jira_issue"
    description = "Search issues in Jira"

    def _run(self, issue_title:str):
        issue_results = search_jira_issue(issue_title)
        return issue_results

    def _arun(self, issue_title:str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = SearchIssueInput

def search_jira_issue(issue_title=None):
    print(issue_title)
    # 建立 JIRA 連線
    try:
        jira = JIRA(server=jira_server, basic_auth=(jira_username, jira_password))
    except Exception as e:
        return {"status": "failure", "reason": str(e)}

    # 建立 JQL 查詢語句
    jql_str = f'project = DEVRELTW'
    jql_str += f' AND summary ~ "{issue_title}"'

    # 搜尋 issue
    try:
        issue_list = []
        for singleIssue in jira.search_issues(jql_str):
            issue_list.append({
                "issue_key": singleIssue.key,
                "summary": singleIssue.fields.summary,
                "reporter": singleIssue.fields.reporter.displayName
            })
        return {"status": "success", "issues": issue_list}
    except Exception as e:
        return {"status": "failure", "reason": str(e)}

def main():
    # 使用範例
    # search_data = SearchIssueInput(issue_title="Blog")

    # tool = JiraSearchTool()
    response = search_jira_issue("Blog")
    print(response)

if __name__ == "__main__":
    main()
