import os
import json
from jira import JIRA
from datetime import datetime, timedelta

def get_issues_due_by_date(due_date):
    # 從環境變數中獲取 Jira 伺服器地址、使用者名稱和密碼
    jira_server = os.getenv('JIRA_INSTANCE_URL', None)
    jira_username = os.getenv('JIRA_USERNAME', None)
    jira_password = os.getenv('JIRA_API_TOKEN', None)

    # 連線到 Jira
    jira_options = {'server': jira_server}
    jira = JIRA(options=jira_options, basic_auth=(jira_username, jira_password))

    # 取得當前使用者名稱
    user = jira.current_user()

    # 找出所有被指派給當前使用者且截止日期在指定日期之前的 issue
    jql = 'assignee={} AND due <= "{}"'.format(user, due_date)
    issues = jira.search_issues(jql)

    # 將所有找到的 issue 及其截止日期存入一個列表
    issues_list = []
    for issue in issues:
        issue_dict = {
            'key': issue.key,
            'summary': issue.fields.summary,
            'deadline': issue.fields.duedate
        }
        issues_list.append(issue_dict)

    return issues_list

# 使用範例
due_date = (datetime.now() + timedelta(weeks=1)).strftime('%Y/%m/%d')
print(get_issues_due_by_date(due_date))