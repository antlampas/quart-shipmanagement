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
    def __init__(self,source="db",Name="",Description=""):
        self.Error       = ""
        self.Source      = source
        self.Name        = Name
        self.Description = Description
        #TODO: Make it work with keycloack too
        if self.Source == "db":
            taskDB = TaskTable
            with db.bind.Session() as s:
                with s.begin():
                    taskDB = s.scalar(selectTask(self.Name))
            if taskDB:
                if task.Name != taskDB.name or taskDB.Description != taskDB.Description:
                    self.Error = "Task mismatches with database"
                    raise self.Error
            else:
                self.Error = "Task not in database"
    def edit(self,attributes:dict):
        self.Error = ""
        try:
            attribute = getattr(self,key)
            attribute = value
        except Exception as e:
            self.Error = e
        if self.Error:
            return self.Error
        #TODO: Make it work with keycloack too
        if self.Source == "db":
            if re.match(isAlpha,self.Name):
                task = TaskTable(self.Name,self.Description)
                with db.bind.Session() as s:
                    with s.begin():
                        s.commit()
        return self.Error
    def load(self,Name=""):
        pass

class Tasks(Addable):
    def __init__(self,source="db"):
        self.Error  = ""
        self.Source = source
        self.Tasks = list()
        #TODO: Make it work with keycloack too
    def add(self,task:Task):
        pass
    def remove(self,task:Task):
        pass
