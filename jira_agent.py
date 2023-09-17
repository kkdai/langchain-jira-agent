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
    assignee: str = Field(..., description="The assignee of the issue")
    status: str = Field(..., description="The status of the issue, e.g. OPEN, IN PROGRESS, DONE. Not-closed issues will be treat as OPEN and IN PROGRESS .")

class JiraSearchTool(BaseTool):
    name = "search_jira_issue"
    description = "Search issues in Jira"

    def _run(self, issue_title:str, assignee: str, status: str):
        issue_results = search_jira_issue(issue_title, assignee, status)
        return issue_results

    def _arun(self, issue_title:str, assignee: str, status: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = SearchIssueInput

def search_jira_issue(issue_title=None, assignee=None, status=None):
    print(issue_title)
    # 建立 JIRA 連線
    try:
        jira = JIRA(server=jira_server, basic_auth=(jira_username, jira_password))
    except Exception as e:
        return {"status": "failure", "reason": str(e)}

    # 建立 JQL 查詢語句
    jql_str = f'project = DEVRELTW'
    if issue_title:
        jql_str += f' AND summary ~ "{issue_title}"'
    if assignee:
        jql_str += f' AND assignee = "{assignee}"'
    if status:
        status_list = status.split(',')
        status_list = [s.strip() for s in status_list]  # remove leading and trailing spaces
        # Search status in a list of status_list
        jql_str += ' AND status IN ({})'.format(", ".join(f'"{s}"' for s in status_list))
        # jql_str += f' AND status IN ({", ".join(f"\"{s}\"" for s in status_list)})'
        #jql_str += f' AND status IN ({", ".join(f'"{s}"' for s in status_list)})'

    # 搜尋 issue
    try:
        issue_list = []
        for singleIssue in jira.search_issues(jql_str):
            issue_list.append({
                "issue_key": singleIssue.key,
                "summary": singleIssue.fields.summary,
                "reporter": singleIssue.fields.reporter.displayName,
                "assignee": singleIssue.fields.assignee.displayName if singleIssue.fields.assignee else None,
                "status": singleIssue.fields.status.name
            })
        return {"status": "success", "issues": issue_list}
    except Exception as e:
        return {"status": "failure", "reason": str(e)}
    

def main():
    # 使用範例
    # search_data = SearchIssueInput(issue_title="Blog")

    # tool = JiraSearchTool()
    response = search_jira_issue("清大", assignee=None, status="OPEN, IN PROGRESS")
    print(response)

if __name__ == "__main__":
    main()
