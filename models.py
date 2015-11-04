# -*- coding: utf-8 -*-
"""
    jira2github.jira_issue
    ~~~~~~~~~

    JiraIssue class

    :copyright: ahsky2@gmail.com
    :license: GPL V3 license.
"""
import simplejson as json


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, JiraComment):
            return o.__dict__
        else:
            return json.JSONEncoder.default(o)


class JiraIssue(object):
    def __init__(self, key, summary, description, assignee, creator, issue_type, status, created):
        self.key = key
        self.summary = summary
        self.description = description
        self.assignee = assignee
        self.creator = creator
        self.issue_type = issue_type
        self.status = status
        self.created = created
        self.comments = []

    def __repr__(self):
        return '<JiraIssue {}>'.format(self.key)

    def __str__(self):
        return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)


class JiraComment(object):
    def __init__(self, author, body, created):
        self.author = author
        self.body = body
        self.created = created

    def __repr__(self):
        return '<JiraComment>'.format()

    def __str__(self):
        return json.dumps(self.__dict__, indent=4, separators=(',', ': '))
