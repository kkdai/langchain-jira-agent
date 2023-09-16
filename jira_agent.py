import os
from jira import JIRA
from typing import Optional, Type
from pydantic import BaseModel, Field

jira_server = os.getenv('JIRA_INSTANCE_URL', None)
jira_username = os.getenv('JIRA_USERNAME', None)
jira_password = os.getenv('JIRA_API_TOKEN', None)

class SearchIssueInput(BaseModel):
    """Search Jira issue input parameters."""
    # project_key: str = Field(..., description="The key of the project")
    issue_title: Optional[str] = Field(None, description="The title of the issue")

class JiraSearchTool:
    name = "search_jira_issue"
    description = "Search issues in Jira"

    def _run(self, search_data: SearchIssueInput):
        issue_results = search_jira_issue(search_data.dict())
        return issue_results

    def _arun(self, search_data: SearchIssueInput):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = SearchIssueInput

def search_jira_issue(search_dict):
    # 建立 JIRA 連線
    try:
        jira = JIRA(server=jira_server, basic_auth=(jira_username, jira_password))
    except Exception as e:
        return {"status": "failure", "reason": str(e)}

    # 建立 JQL 查詢語句
    jql_str = f'project = DEVRELTW'
    if search_dict.get('issue_title'):
        jql_str += f' AND summary ~ "{search_dict["issue_title"]}"'

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
    search_data = SearchIssueInput(issue_title="Blog")

    tool = JiraSearchTool()
    response = tool._run(search_data)
    print(response)

if __name__ == "__main__":
    main()
