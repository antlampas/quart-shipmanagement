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
        if self.Source == "db":
            if self.Nickname:
                cmt = self._loadFromDB(Nickname=self.Nickname)
                if cmt:
                    if not re.match(isNumber,cmt.Serial)  and not stop_construct:
                        self.Error = "Member serial is not a number"
                        stop_construct = True
                    if not re.match(isNumber,cmt.Stic)  and not stop_construct:
                        self.Error = "Member STIC membership is not a number"
                        stop_construct = True
                    if (self.FirstName or self.LastName or self.Rank or \
                        self.Division or self.Duties or self.Serial or \
                        self.Stic) and not stop_construct:
                        if self._checkDB(cmt) and not stop_construct:
                               self.Error = "Crew member mismatches with database"
                               stop_construct = True
                    else:
                        self.FirstName = cmt.FirstName
                        self.LastName  = cmt.LastName
                        self.Rank      = cmt.Rank
                        self.Division  = cmt.Division
                        self.Duties    = cmt.Duties
                        self.Serial    = cmt.Serial
                        self.Stic      = cmt.Stic
                else:
                    self.Error = "Crew member not in database"
                    stop_construct = True
            else:
                self.Error = "No Nickname given"
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
            cmt = self._loadFromDB()
            if not self.Error:
                if cmt:
                    self.FirstName = cmt.FirstName
                    self.LastName  = cmt.LastName
                    self.Nickname  = cmt.Nickname
                    self.Serial    = cmt.Serial
                    self.Rank      = cmt.RankName
                    self.Division  = cmt.DivisionName
                    self.Duties    = cmt.Duties
                    self.Stic      = cmt.Stic
        return self.Error
    def _loadFromDB(self,Nickname):
        self.Error = ""
        with db.bind.Session() as s:
            with s.begin():
                cmt = None
                if Nickname:
                    cmt = s.scalar(selectCrew(Nickname))
                elif Serial:
                    cmt = s.scalar(selectCrew(Serial))
                else:
                    self.Error = "Search clause missing"

                if (not self.FirstName or  \
                    not self.LastName  or  \
                    not self.Division  or  \
                    not self.Rank      or  \
                    not self.Duties    or  \
                    not self.Serial    or  \
                    not self.Stic)     and \
                    not stop_construct:
                       self.FirstName = cmt.FirstName
                       self.LastName  = cmt.LastName
                       self.Nickname  = cmt.Nickname
                       self.Serial    = cmt.Serial
                       self.Rank      = cmt.RankName
                       self.Division  = cmt.DivisionName
                       self.Duties    = cmt.Duties
                       self.Stic      = cmt.Stic

                if not self.Error:
                    return cmt
                else:
                    return None
        return self.error
    def _saveToDB(self):
        if re.match(isAlpha, self.FirstName) and \
           re.match(isAlpha, self.LastName)  and \
           re.match(isAlpha, self.Nickname)  and \
           re.match(isAlpha, self.Rank)      and \
           re.match(isAlpha, self.Division):
            person             = PersonalBaseInformationsTable(FirstName = self.FirstName,
                                                               LastName  = self.LastName,
                                                               Nickname  = self.Nickname)
            crewMember         = CrewMemberTable(PersonalBaseInformationsId = crewMember.Id)
            crewMemberRank     = CrewMemberRankTable(MemberSerial=self.Serial,
                                                     RankName=self.rank)
            crewMemberDivision = CrewMemberDivisionTable(MemberSerial = self.Serial,
                                                         DivisionName = self.division)
            crewMemberDuty     = [ CrewMemberDutyTable(MemberSerial = self.Serial,
                                                       DutyName     = duty.name) for duty in self.Duties ]
            if crewMember:
                with db.bind.Session() as s:
                    with s.begin():
                        s.commit()
            else:
                with db.bind.Session() as s:
                    with s.begin():
                        s.add()
                        s.commit()
    def _checkDB(self,cmt=None):
        if cmt:
            if (self.FirstName != cmt.FirstName or  \
                self.LastName  != cmt.LastName  or  \
                self.Rank      != cmt.Rank      or  \
                self.Division  != cmt.Division  or  \
                self.Duties    != cmt.Duties    or  \
                self.Serial    != cmt.Serial    or  \
                self.Stic      != cmt.Stic):
                return True
            else:
                return False
        else:
            return False

class Crew(Addable):
    def __init__(self,source="db",crew=list()):
        self.Error                  = ""
        self.Source                 = source
        self.Crew                   = crew
        self.KeycloakAdminClient    = KeycloakConfig.KEYCLOAK_ADMIN['client_id']
        self.KeycloakAdminGrantType = KeycloakConfig.KEYCLOAK_ADMIN['grant_type']
        self.KeycloakAdminUser      = KeycloakConfig.KEYCLOAK_ADMIN['username']
        self.KeycloakAdminPass      = KeycloakConfig.KEYCLOAK_ADMIN['password']
        self.KeycloakBaseURL        = KeycloakConfig.KEYCLOAK_URL
        self.KeycloakRealm          = KeycloakConfig.KEYCLOAK_REALM
        self.KeycloakAccessToken    = None
        #TODO: Make it work with keycloack too
        if self.Source == "db":
            with db.bind.Session() as s:
                with s.begin():
                    crewDB     = self._loadFromDB()
                    crewDBlist = list()
                    if crewDB:
                        for member in crewDB:
                            DBmember = CreMember(FirstName = crewDB.FirstName
                                                 LastName  = crewDB.LastName
                                                 Rank      = crewDB.Rank
                                                 Division  = crewDB.Division
                                                 Duties    = crewDB.Duties
                                                 Serial    = crewDB.Serial
                                                 Stic      = crewDB.Stic
                                                )
                            crewDBlist.append(DBmember)
                        if crew:
                            if crew != crewDBlist:
                            self.Error = "Given crew list mismatches with database"
                        else:
                            self.Crew = crewDBlist
                    else:
                        self.Error = "No crew in database"
        elif self.Source == "keycloak":
            if not crew:
                keycloakAccessRequest    = f'{self.KeycloakBaseURL}/realms/{self.KeycloakRealm}/protocol/openid-connect/token'
                keycloakUsersListRequest = f'{self.KeycloakBaseURL}/admin/realms/{self.KeycloakRealm}/users'
                if not self.KeycloakAccessToken:
                    keycloakAccess    = requests.post(keycloakAccessRequest,
                                                      headers = {
                                                                  'content-type' : 'application/x-www-form-urlencoded'
                                                                },
                                                      data    = {
                                                                  'client_id'  : self.KeycloakAdminClient,
                                                                  'grant_type' : self.KeycloakAdminGrantType,
                                                                  'username'   : self.KeycloakAdminUser,
                                                                  'password'   : self.KeycloakAdminPass
                                                                }
                                                     )
                    self.KeycloakAccessToken   = json.loads(keycloakAccess.text)['access_token']
                keycloakUsers = requests.get(keycloakUsersListRequest,
                                             headers = {
                                                         'Authorization' : \
                                                             f'bearer {self.KeycloakAccessToken}'
                                                       }
                                            )
                usersList = json.loads(keycloakUsers.text)
                if 'error' in usersList:
                    if 'HTTP 401 Unauthorized' in userList['error']:
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
                        keycloakUsers = requests.get(keycloakUsersListRequest,
                                                     headers = {
                                                                 'Authorization' : f'bearer {self.KeycloakAccessToken}'
                                                               }
                                                    )
                        self.KeycloakAccessToken   = json.loads(keycloakAccess.text)['access_token']
                        usersList = json.loads(keycloakUsers.text)
                    else:
                        self.Error = userList['error']
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
    def _loadFromDB(self):
        crewDB = s.scalars(selectCrew()).all()
        return crewDB
    def _saveToDB(self):
        pass
    def checkDB(self,cmt=None):
        pass
