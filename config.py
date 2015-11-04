# -*- coding: utf-8 -*-
"""
    jira2github.config
    ~~~~~~~~~

    Configuration of Jira nad GitHub

    :copyright: ahsky2@gmail.com
    :license: GPL V3 license.
"""

JIRA_SERVER = 'http://yourdomain/jira'
JIRA_USER = 'admin'
JIRA_PASSWORD = 'admin'
JIRA_JQL = 'project = PRJ ORDER BY issue asc'
JIRA_ISSUE_LINK_BASE = 'http://yourdomain/jira/browse/'

GITHUB_USER = 'yourgithubid'
GITHUB_PASSWORD = 'yourgithubpassword'
GITHUB_ORGANIZATION = 'yourorganization'
GITHUB_REPO = 'yourrepository'

JIRA_ISSUE_TYPE_TO_GITHUB_ISSUE_LABEL = {'Epic': 'epic',
                                         'Story': 'story',
                                         'Task': 'task',
                                         'Sub-task': 'Sub-task',
                                         'Bug': 'bug'}
JIRA_ISSUE_STATUS_TO_GITHUB_ISSUE_LABEL = {'Backlog': None,
                                           'To Do': 'ready',
                                           'In Progress': 'in progress',
                                           'Done': None}
JIRA_ISSUE_STATUS_TO_GITHUB_ISSUE_STATE = {'Backlog': 'open',
                                           'To Do': 'open',
                                           'In Progress': 'open',
                                           'Done': 'close'}
JIRA_USER_TO_GITHUB_LOGIN = {'jirausername1': 'githubusername1',
                             'jirausername2': 'githubusername2',
                             'jirausername3': 'githubusername3'}
