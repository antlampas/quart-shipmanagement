#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from sqlalchemy     import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from model          import db
from model          import CrewMemberTable
from model          import TaskTable
from model          import MissionBaseInformationsTable
from model          import MissionTable
from model          import MemberMissionLogEntryTable

from utilities      import isAlpha
from utilities      import isNumber

from baseClasses    import Editable
from baseClasses    import Addable

class Mission(Editable):
    def __init__(self,
                 name             = '',
                 description      = '',
                 requiredDuration = '',
                 startedAt        = '',
                 endedAt          = '',
                 status           = '',
                 tasks            = list()
                ):
        self.Error            = ''
        self.Name             = ''
        self.Description      = ''
        self.RequiredDuration = ''
        self.StartAt          = ''
        self.EndedAt          = ''
        self.Status           = ''
        self.Tasks            = ''

        if re.match(isAlpha,name):
            self.Name             = name
        if re.match(isAlpha,description):
            self.Description      = description
        if re.match(isNumber,requiredDuration):
            self.RequiredDuration = requiredDuration
        if re.match(isNumber,startAt):
            self.StartAt          = startAt
        if re.match(isNumber,endedAt):
            self.EndedAt          = endedAt
        if re.match(isAlpha,status):
            self.Status           = status
        self.Tasks            = tasks

    def edit(self,mission:MissionTable):
        pass
    def serilize(self):
        pass
    def deserilize(self,division=dict()):
        pass

class Missions(Addable):
    def __init__(self,missions=list()):
        pass
    def add(self,mission=None):
        pass
    def remove(self,mission=None):
        pass
    def serilize(self):
        pass
    def deserilize(self,division=dict()):
        pass
