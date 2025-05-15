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
                 source    = "db",
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
        self.Source    = source
        self.FirstName = FirstName
        self.LastName  = LastName
        self.Nickname  = Nickname
        self.Serial    = Serial
        self.Stic      = Stic
        self.Rank      = Rank
        self.Division  = Division
        self.Duties    = Duties

        stop_construct = False
        #TODO: Make it work with keycloack too
        if self.Source == "db" and self.Nickname and not stop_construct:
            crewMemberInformations = None
            with db.bind.Session() as s:
                with s.begin():
                    crewMemberInformations = s.scalar(selectCrew(self.Nickname))
            if crewMemberInformations:
                if not re.match(isNumber,crewMemberInformations.Serial)  and not stop_construct:
                    self.Error = "Member serial is not a number"
                    stop_construct = True
                if not re.match(isNumber,crewMemberInformations.Stic)  and not stop_construct:
                    self.Error = "Member STIC membership is not a number"
                    stop_construct = True
                if (self.FirstName != crewMemberInformations.FirstName or \
                   self.LastName  != crewMemberInformations.LastName  or  \
                   self.Nickname  != crewMemberInformations.Nickname  or  \
                   self.Rank      != crewMemberInformations.Rank      or  \
                   self.Division  != crewMemberInformations.Division  or  \
                   self.Duties    != crewMemberInformations.Duties    or  \
                   self.Serial    != crewMemberInformations.Serial    or  \
                   self.Stic      != crewMemberInformations.Stic)     and \
                   not stop_construct:
                       self.Error = "Crew member mismatches with database"
                       stop_construct = True
            else:
                self.Error = "Crew member not in database"
                stop_construct = True
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
        if self.Error:
            return self.Error
        #TODO: Make it work with keycloack too
        if self.Source == "db":
            with db.bind.Session() as s:
                with s.begin():
                    crewMember = s.scalar(selectCrew(self.Nickname))
            #TODO: ricomincia da qui
            if crewMember:
                if re.match(isAlpha, self.FirstName) and \
                   re.match(isAlpha, self.LastName)  and \
                   re.match(isAlpha, self.Nickname)  and \
                   re.match(isAlpha, self.Rank)      and \
                   re.match(isAlpha, self.Division):
                    person             = PersonalBaseInformationsTable(FirstName=self.FirstName,LastName=self.LastName,Nickname=self.Nickname)
                    crewMember         = CrewMemberTable(PersonalBaseInformationsId=crewMember.Id)
                    crewMemberRank     = CrewMemberRankTable(MemberSerial=self.Serial,RankName=self.rank)
                    crewMemberDivision = CrewMemberDivisionTable(MemberSerial=self.Serial,DivisionName=self.division)
                    crewMemberDuty     = [ CrewMemberDutyTable(MemberSerial=self.Serial,DutyName=duty.name) for duty in self.Duties ]
                    if crewMember:
                        with db.bind.Session() as s:
                            with s.begin():
                                s.commit()
                    else:
                        with db.bind.Session() as s:
                            with s.begin():
                                s.add()
                                s.commit()
                else:
                    self.Error = "Invalid attributes"
        return self.Error
    def load(self,Nickname="",Serial=0):
        self.Error = ""
        #TODO: Make it work with keycloack too
        if self.Source == "db":
            with db.bind.Session() as s:
                with s.begin():
                    crewMemberInformations = list()
                    if Nickname:
                        crewMemberInformations = s.scalar(selectCrew(Nickname))
                    elif Serial:
                        crewMemberInformations = s.scalar(selectCrew(Serial))
                    else:
                        self.Error = "Search clause missing"
                    if not self.Error:
                        if crewMemberInformations:
                            self.FirstName = crewMemberInformations.FirstName
                            self.LastName  = crewMemberInformations.LastName
                            self.Nickname  = crewMemberInformations.Nickname
                            self.Serial    = crewMemberInformations.Serial
                            self.Rank      = s.query(CrewMemberDutyTable).filter_by(MemberSerial=memberSerial).first().RankName
                            self.Division  = s.query(CrewMemberDutyTable).filter_by(MemberSerial=memberSerial).first().DivisionName
                            self.Duties    = [ duty.Dutyname for duty in s.query(CrewMemberDutyTable).filter_by(MemberSerial=memberSerial).all() ]
                            self.Stic      = s.query(CrewMemberDutyTable).filter_by(MemberSerial=memberSerial).first().Stic
                        else:
                            self.Error = "Crew member not found"
        return self.Error

class Crew(Addable):
    def __init__(self,source="db",crew=list()):
        self.Error  = ""
        self.Source = source
        self.Crew   = crew
        #TODO: Make it work with keycloack too
        if self.Source == "db":
            with db.bind.Session() as s:
                with s.begin():
                    crewDB = s.scalars(selectCrew()).all()
                    if crew:
                        if crew != crewDB:
                            self.Error = "Given crew list mismatches with database"
                    else:
                        self.Error = "No crew in database"
        if self.Source == "keycloak":
            if not crew:
                keycloakAdminUser = KeycloakConfig.KEYCLOAK_ADMIN['username']
                keycloakAdminPass = KeycloakConfig.KEYCLOAK_ADMIN['password']
                keycloakBaseURL   = KeycloakConfig.KEYCLOAK_URL
                keycloakRealm     = KeycloakConfig.KEYCLOAK_REALM
                keycloakAccessRequest    = f'{keycloakBaseURL}/realms/{keycloakRealm}/protocol/openid-connect/token'
                keycloakUsersListRequest = f'{keycloakBaseURL}/admin/realms/{keycloakRealm}/users'
                keycloakAccess    = requests.post(keycloakAccessRequest,
                                                  headers = {
                                                              'content-type' : 'application/x-www-form-urlencoded'
                                                            },
                                                  data    = {
                                                              'client_id'  : 'admin-cli',
                                                              'grant_type' : 'password',
                                                              'username'   :'francesco',
                                                              'password'   : '0123456789'
                                                            }
                                                 )
                accessToken   = json.loads(keycloakAccess.text)['access_token']
                keycloakUsers = requests.get(keycloakUsersListRequest,
                                             headers = {
                                                         'Authorization' : \
                                                             f'bearer {accessToken}'
                                                       }
                                            )
                usersList = json.loads(keycloakUsers.text)
                cm = SimpleNamespace()
                for user in usersList:
                    if 'groups' in user:
                        rank         = [ i.split("/")[len(i.split("/"))-1] for i in user['groups'] if 'Gradi'     in i ]
                        division     = [ i.split("/")[len(i.split("/"))-1] for i in user['groups'] if 'Divisioni' in i ]
                        duties       = [ i.split("/")[len(i.split("/"))-1] for i in user['groups'] if 'Doveri'    in i ]
                    else:
                        rank     = None
                        division = None
                        duties   = None
                    cm.FirstName = user['firstName']
                    cm.LastName  = user['lastName']
                    cm.Nickname  = user['username']
                    cm.Serial    = user['attributes']['SerialNumber'][0]
                    if 'STICmember' in user['attributes']:
                        cm.Stic      = user['attributes']['STICmember'][0]
                    else:
                        cm.Stic = 0
                    if rank:
                        cm.Rank = tank[0]
                    else:
                        cm.Rank = ""
                    if division:
                        cm.Division = division[0]
                    else:
                        cm.Division = ""
                    cm.Duties = duties
                    crewMember = CrewMember(FirstName = cm.FirstName,
                                            LastName  = cm.LastName,
                                            Nickname  = cm.Nickname,
                                            Serial    = cm.Serial,
                                            Stic      = cm.Stic,
                                            Rank      = cm.Rank,
                                            Division  = cm.Division,
                                            Duties    = cm.Duties
                                           )
                    self.Crew.append(crewMember)
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
           if self.Source == "db":
               crewDB = list()
               with db.bind.Session() as s:
                   with s.begin():
                       crewDB = s.scalars(selectCrew()).all()
               if crewDB:
                   if not member in crewDB:
                       self.Error = "Given crew list mismatches with database"
               else:
                   self.Error = "No crew in database"
        return self.Error
    def remove(self,source="db",Member=CrewMember()):
        self.Error = ""
        try:
            #TODO: Make it work with keycloack too
            if source == "db":
                with db.bind.Session() as s:
                    with s.begin():
                        member = s.scalar(selectCrew(Member.nickname))
                        if member:
                            try:
                                s.remove(member)
                                s.commit()
                                self.Crew.remove(member)
                            except Exception as e:
                                self.Error = "Error committing to database"
                        else:
                            self.Error = "Crew member not found"
        except Exception as e:
            self.Error = e
        return self.Error
