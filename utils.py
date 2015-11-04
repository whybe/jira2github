# -*- coding: utf-8 -*-
"""
    jira2github.utils
    ~~~~~~~~~

    utilities

    :copyright: ahsky2@gmail.com
    :license: GPL V3 license.
"""
import re
from github import UnknownObjectException
from enum import Enum
import random
import config


class JiraAttr(Enum):
    TYPE = 1
    STATUS = 2
    USER = 3


class GithubAttr(Enum):
    LABEL = 1
    STATE = 2
    LOGIN = 3


def convert(val, jira_attr, github_attr):
    if jira_attr == JiraAttr.TYPE and github_attr == GithubAttr.LABEL:
        return config.JIRA_ISSUE_TYPE_TO_GITHUB_ISSUE_LABEL[val]
    elif jira_attr == JiraAttr.STATUS and github_attr == GithubAttr.LABEL:
        return config.JIRA_ISSUE_STATUS_TO_GITHUB_ISSUE_LABEL[val]
    elif jira_attr == JiraAttr.STATUS and github_attr == GithubAttr.STATE:
        return config.JIRA_ISSUE_STATUS_TO_GITHUB_ISSUE_STATE[val]
    elif jira_attr == JiraAttr.USER and github_attr == GithubAttr.LOGIN:
        return config.JIRA_USER_TO_GITHUB_LOGIN[val]


def random_color():
    r = lambda: random.randint(0, 255)
    return '%02X%02X%02X' % (r(), r(), r())


def create_label(label, github_repo):
    github_label = None
    try:
        github_label = github_repo.get_label(label)
        # print 'already label {} exists'.format(github_label.name)
    except UnknownObjectException:
        github_label = github_repo.create_label(label, random_color())
        print 'create label {}'.format(github_label.name)

    return github_label


def gen_comment(jira_comment):
    comment = u'''{}

> Written by @{}
> Created at {}'''
    return comment.format(j2m(jira_comment.body),
                          convert(jira_comment.author, JiraAttr.USER, GithubAttr.LOGIN),
                          jira_comment.created)


def gen_body(jira_issue):
    body = u'''{}

> Written by @{}
> Created at {}
> Link to {}{}'''
    return body.format(j2m(jira_issue.description),
                       convert(jira_issue.creator, JiraAttr.USER, GithubAttr.LOGIN),
                       jira_issue.created,
                       config.JIRA_ISSUE_LINK_BASE,
                       jira_issue.key)


def j2m(c):
    c = re.sub(r'{code:?(.*)}', r'```\1', c)
    return c
