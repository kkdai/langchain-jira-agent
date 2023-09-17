import os
from jira import JIRA
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool


jira_server = os.getenv('JIRA_INSTANCE_URL', None) # e.g. https://jira.example.com
jira_username = os.getenv('JIRA_USERNAME', None) # e.g. jira_username
jira_password = os.getenv('JIRA_API_TOKEN', None) # e.g. jira_user_password.

class SearchIssueInput(BaseModel):
    """Search Jira issue input parameters."""
    # project_key: str = Field(..., description="The key of the project")
    issue_title: str = Field(..., description="The title of the issue")
    assignee: str = Field(..., description="The assignee of the issue")
    status: str = Field(..., description="The status of the issue, e.g. OPEN, IN PROGRESS, DONE. Not-closed issues will be treat as OPEN and IN PROGRESS .")
    project: str = Field(..., description="The project of the issues. If not specified, all projects will be searched. If specified, the project key should be provided. e.g. ")

class JiraSearchTool(BaseTool):
    name = "search_jira_issue"
    description = "Search issues in Jira"

    def _run(self, issue_title:str, assignee: str, status: str, project: str):
        issue_results = search_jira_issue(issue_title, assignee, status)
        return issue_results

    def _arun(self, issue_title:str, assignee: str, status: str, project: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = SearchIssueInput

def get_jira_issue_details(issue_key):
    # 建立 JIRA 連線
    try:
        jira = JIRA(server=jira_server, basic_auth=(jira_username, jira_password))
    except Exception as e:
        return {"status": "failure", "reason": str(e)}

    # 查詢 issue
    try:
        issue = jira.issue(issue_key)
        assignee = issue.fields.assignee.displayName if issue.fields.assignee else None
        status = issue.fields.status.name

        # 取得最新的兩個 comments
        comments = issue.fields.comment.comments
        latest_comments = comments[-2:] if len(comments) > 2 else comments
        latest_comments = [{"author": comment.author.displayName, "body": comment.body} for comment in latest_comments]

        return {
            "status": "success",
            "issue_details": {
                "issue_key": issue_key,
                "assignee": assignee,
                "status": status,
                "latest_comments": latest_comments
            }
        }
    except Exception as e:
        return {"status": "failure", "reason": str(e)}
    
def main():
    # 使用範例
    response2 = get_jira_issue_details("JIRA-1234")
    print(response2)

if __name__ == "__main__":
    main()
