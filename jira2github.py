# -*- coding: utf-8 -*-
"""
    jira2github
    ~~~~~~~~~

    migration tool from Jira to Github

    :copyright: ahsky2@gmail.com
    :license: GPL V3 license.
"""
from sets import Set
from jira import JIRA
import config
from models import JiraIssue, JiraComment
from github import Github
from utils import JiraAttr, GithubAttr, convert, create_label, gen_body, gen_comment

jira = JIRA(config.JIRA_SERVER, basic_auth=(config.JIRA_USER, config.JIRA_PASSWORD))
issues = jira.search_issues(jql_str=config.JIRA_JQL, startAt=0, maxResults=1000)

github = Github(config.GITHUB_USER, config.GITHUB_PASSWORD)
github_repo = github.get_organization(config.GITHUB_ORGANIZATION).get_repo(config.GITHUB_REPO)

for issue in issues:
    jira_issue_assignee = None
    if issue.fields.assignee is None:
        jira_issue_assignee = issue.fields.creator.name
    else:
        jira_issue_assignee = issue.fields.assignee.name

    jira_issue_description = issue.fields.description
    if jira_issue_description is None:
        jira_issue_description = ''

    jira_issue = JiraIssue(
        issue.key,
        issue.fields.summary,
        jira_issue_description,
        jira_issue_assignee,
        issue.fields.creator.name,
        issue.fields.issuetype.name,
        issue.fields.status.name,
        issue.fields.created)

    for comment in jira.issue(issue.key).fields.comment.comments:
        jira_issue.comments.append(
            JiraComment(
                comment.author.name,
                comment.body,
                comment.created))

    # if len(issue.fields.components) == 0:
    # if len(issue.fields.components) > 0 and issue.fields.components[0].name == 'Backend':
        # print issue.fields.components

    print jira_issue

    github_labels = []

    label = convert(jira_issue.issue_type, JiraAttr.TYPE, GithubAttr.LABEL)
    if label is not None:
        github_labels.append(create_label(label, github_repo))

    label = convert(jira_issue.status, JiraAttr.STATUS, GithubAttr.LABEL)
    if label is not None:
        github_labels.append(create_label(label, github_repo))

    github_issue = github_repo.create_issue(
        jira_issue.summary,
        body=gen_body(jira_issue),
        assignee=convert(jira_issue.assignee, JiraAttr.USER,
                         GithubAttr.LOGIN),
        labels=github_labels)

    github_issue.edit(state=convert(jira_issue.status, JiraAttr.STATUS, GithubAttr.STATE))

    print github_issue

    for comment in jira_issue.comments:
        github_comment = github_issue.create_comment(gen_comment(comment))
        print github_comment
