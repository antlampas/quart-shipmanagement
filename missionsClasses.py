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
                 source           = "db",
                 Name             = "",
                 Description      = "",
                 RequiredDuration = "",
                 StartedAt        = "",
                 EndedAt          = "",
                 Status           = "",
                 Tasks            = list()
                ):
        self.Error            = ""
        self.Source           = Source
        self.Name             = Name
        self.Description      = Description
        self.RequiredDuration = RequiredDuration
        self.StartAt          = StartAt
        self.EndedAt          = EndedAt
        self.Status           = Status
        self.Tasks            = Tasks
        #TODO: Make it work with keycloack too
        if self.Source == "db":
            with db.bind.Session() as s:
                with s.begin():
                    #TODO: check database
                    pass
    def edit(self,mission:MissionTable):
        pass
    def load(self,mission:MissionTable):
        pass

class Missions(Addable):
    def __init__(self,source="db",missions=list()):
        pass
    def add(self,mission:Mission):
        pass
    def remove(self,mission:Mission):
        pass
