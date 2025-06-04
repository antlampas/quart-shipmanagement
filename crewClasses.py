#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re
import requests
import json

from types          import SimpleNamespace

from quart          import session

from sqlalchemy     import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from model          import db
from model          import PersonalBaseInformationsTable
from model          import CrewMemberTable
from model          import DutyTable
from model          import RankTable
from model          import DivisionTable
from model          import CrewMemberRankTable
from model          import CrewMemberDutyTable
from model          import CrewMemberDivisionTable
from model          import MemberOnboardLogEntryTable
from model          import MemberRankLogEntryTable
from model          import MemberDivisionLogEntryTable
from model          import MemberTaskLogEntryTable
from model          import MemberMissionLogEntryTable
from model          import selectPerson
from model          import selectCrew
from model          import selectRank
from model          import selectDuty
from model          import selectDivision

from utilities import isAlpha
from utilities import isNumber

from baseClasses    import Editable
from baseClasses    import Addable

from config         import KeycloakConfig

class CrewMember(Editable):
    def __init__(self,
                 FirstName = "",
                 LastName  = "",
                 Nickname  = "",
                 Rank      = "",
                 Division  = "",
                 Duties    = list(),
                 Serial    = 0,
                 Stic      = 0
                ):
        self.Error     = ""
        self.FirstName = FirstName
        self.LastName  = LastName
        self.Nickname  = Nickname
        self.Serial    = Serial
        self.Stic      = Stic
        self.Rank      = Rank
        self.Division  = Division
        self.Duties    = Duties
    def edit(self,attributes=dict()):
        self.Error = ""
        crewMember = None
        if attributes:
            for key,value in attributes:
                try:
                    attribute = getattr(self,key)
                    attribute = value
                except Exception as e:
                    self.Error = e
        return self.Error
    def serialize(self):
        self.Error = ''
        member = {
                    "FirstName" : self.FirstName,
                    "LastName"  : self.LastName,
                    "Nickname"  : self.Nickname,
                    "Rank"      : self.Rank,
                    "Division"  : self.Division,
                    "Duties"    : self.Duties,
                    "Serial"    : self.Serial,
                    "Stic"      : self.Stic
                 }
        return member
    def deserilize(self,crewMember=dict()):
        self.Error = ''
        for key,value in crewMember:
            if key == 'FirstName':
                self.FirstName = value
            elif key == 'LastName':
                self.LastName = value
            elif key == 'Nickname':
                self.Nickname = value
            elif key == 'Rank':
                self.Rank = value
            elif key == 'Division':
                self.Division = value
            elif key == 'Duties':
                self.Duties = value
            elif key == 'Serial':
                self.Serial = value
            elif key == 'Stic':
                self.Stic = value
            else:
                self.Error = "Attribute not valid"
                break
        return self.Error

class Crew(Addable):
    def __init__(self,crew=list()):
        self.Error = ""
        self.Crew  = crew
    def add(self,member=CrewMember()):
        self.Error = ""
        if re.match(isAlpha,member.FirstName) and \
           re.match(isAlpha,member.LastName)  and \
           re.match(isAlpha,member.Nickname)  and \
           re.match(isAlpha,member.Rank)      and \
           re.match(isAlpha,member.Division)  and \
           re.match(isAlpha,member.Duties)    and \
           re.match(isNumber,member.Serial)   and \
           re.match(isNumber,member.Stic):
           self.Crew.append(member)
        else:
            self.Error = "Invalid member data"
        return self.Error
    def remove(self,source="db",member=CrewMember()):
        self.Error = ""
        try:
            self.Crew.remove(member)
        except Exception as e:
            self.Error = e
        return self.Error
    def serialize(self):
        self.Error = ''
        crew = dict()
        for member in self.Crew:
            crew[member.Nickname] = member.serilize()
        return crew
    def deserilize(self,crew=dict()):
        self.Error = ''
