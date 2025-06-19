#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from model       import db
from model       import CrewMemberTable
from model       import TaskTable
from model       import MemberTaskLogEntryTable
from model       import selectTask

from baseClasses import Editable
from baseClasses import Addable

class Task(Editable):
    def __init__(self,Name='',Description=''):
        self.Error       = ""
        if re.match(isAlpha,name):
            self.Name  = name
        else:
            self.Error = "Name is not alpha"
            self.Name  = None
        if re.match(isText,description):
            self.Description = description
        else:
            self.Error        = "Description is not text"
            self.Description  = None
    def edit(self,attributes=dict()):
        self.Error = ""
        if attributes:
            for key,value in attributes:
                if key == 'Name' and re.match(isAlpha,key):
                    try:
                        attribute = getattr(self,key)
                        attribute = value
                    except Exception as e:
                        self.Error = e
                else:
                    self.Error = 'Invalid name'
                if key == 'Description' and re.match(isText,key):
                    try:
                        attribute = getattr(self,key)
                        attribute = value
                    except Exception as e:
                        self.Error = e
                else:
                    self.Error = 'Invalid description'
        return self.Error
    def serialize(self):
        self.Error = ''
        task = {
                        "Name"        : self.Name,
                        "Description" : self.Description
                   }
        return task
    def deserialize(self,task=dict()):
        self.Error = ''
        if attribute:
            for key,value in task:
                if key == "Name":
                    self.Name = value
                elif key == "Description":
                    self.Description = value
                else:
                    self.Error = "Attribute not valid"
                    break
            return self.Error
class Tasks(Addable):
    def __init__(self,tasks=list()):
        self.Error  = ""
        self.Tasks = list()
        if tasks:
            for task in tasks:
                if task is Task:
                    if re.match(isAlpha,task.Name):
                        if re.match(isAlphanumeric,task.Description):
                            self.Divisions.append(task)
                        else:
                            self.Error = "Description not text"
                            break
                    else:
                        self.Error = "Name not alpha"
                        break
                else:
                    self.Error = "Task not valid"
                    break
        else:
            self.Error = 'No tasks provided'
    def add(self,task=None):
        self.Error = ""
        if task:
            if task is Task:
                if re.match(isAlpha,task.Name):
                    if re.match(isAlphanumeric,task.Description):
                       self.Divisions.append(task)
                    else:
                        self.Error = "Description not text"
                else:
                    self.Error = "Name not alpha"
            else:
                self.Error = "Task not valid"
        else:
            self.Error = "No task provided"
        return self.Error
    def remove(self,task=None):
        self.Error = ""
        if task:
            try:
                if task is Task:
                    i = self.Tasks.index(division)
                    self.Tasks.remove(i)
                else:
                    self.Error = "Task not valid"
            except Exception as e:
                self.Error = e
        else:
            self.Error = "No task provided"
        return self.Error
    def serialize(self):
        self.Error = ''
        tasks = dict()
        for task in self.Tasks:
            tasks[tasks.Name] = task.serilize()
        return tasks
    def deserialize(self,tasks=dict()):
        self.Error = ''
        if tasks:
            for key,task in tasks:
                if re.match(isAlpha,key):
                    if task is dict():
                        if 'Name' in task and re.match(isAlpha,task['Name']):
                            if 'Description' in task and re.match(isAlpha,task['Description']):
                                self.Divisions.append(Task(task['Name'],task['Description']))
                            else:
                                self.Error = "Invalid description"
                                break
                        else:
                            self.Error = "Invalid Name"
                            break
                    else:
                        self.Error = "Task not valid"
                        break
        else:
            self.Error = "No tasks given"
        return self.Error
