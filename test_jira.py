# -*- coding: utf-8 -*-
"""
    jira2github.test_jira
    ~~~~~~~~~

    test jira for configuration

    :copyright: ahsky2@gmail.com
    :license: GPL V3 license.
"""
from sets import Set
from jira import JIRA
import config
from models import JiraIssue, JiraComment

jira = JIRA(config.JIRA_SERVER, basic_auth=(config.JIRA_USER, config.JIRA_PASSWORD))
issues = jira.search_issues(jql_str=config.JIRA_JQL, startAt=0, maxResults=1000)

print 'Jira Issue Length : {}'.format(issues.total)

jira_issue_types = []
jira_issue_status = []
jira_issue_users = []

for issue in issues:
    jira_issue_assignee = None
    if issue.fields.assignee is None:
        jira_issue_assignee = issue.fields.creator.name
    else:
        jira_issue_assignee = issue.fields.assignee.name

    jira_issue = JiraIssue(issue.key,
                           issue.fields.summary,
                           issue.fields.description,
                           jira_issue_assignee,
                           issue.fields.creator.name,
                           issue.fields.issuetype.name,
                           issue.fields.status.name,
                           issue.fields.created)

    jira_issue_types.append(jira_issue.issue_type)
    jira_issue_status.append(jira_issue.status)
    jira_issue_users.append(jira_issue.creator)
    jira_issue_users.append(jira_issue.assignee)

    for comment in jira.issue(issue.key).fields.comment.comments:
        jira_issue_users.append(comment.author.name)

print 'Jira Issue Type : {}'.format(list(Set(jira_issue_types)))
print 'Jira Issue Status : {}'.format(list(Set(jira_issue_status)))
print 'Jira Issue Assignee : {}'.format(list(Set(jira_issue_users)))
