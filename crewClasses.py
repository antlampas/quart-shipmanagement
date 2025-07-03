#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from utilities   import isAlpha
from utilities   import isNumber

from baseClasses import Editable
from baseClasses import Addable

class CrewMember(Editable):
    def __init__(self,
                 FirstName = '',
                 LastName  = '',
                 Nickname  = '',
                 Rank      = '',
                 Division  = '',
                 Duties    = list(),
                 Serial    = '0',
                 Stic      = '0'
                ):
        self.Error     = ''
        self.FirstName = ''
        self.LastName  = ''
        self.Nickname  = ''
        self.Serial    = 0
        self.Stic      = 0
        self.Rank      = ''
        self.Division  = ''
        self.Duties    = list()
        if re.match(isAlpha,FirstName) and \
           re.match(isAlpha,LastName)  and \
           re.match(isAlpha,Nickname)  and \
           re.match(isNumber,Serial)   and \
           re.match(isNumber,Stic)     and \
           re.match(isAlpha,Rank)      and \
           re.match(isAlpha,Division):
            self.FirstName = FirstName
            self.LastName  = LastName
            self.Nickname  = Nickname
            self.Serial    = Serial
            self.Stic      = Stic
            self.Rank      = Rank
            self.Division  = Division
            for Duty in Duties:
                if re.match(isAlpha,Duty):
                    self.Duties.append(Duty)
                else:
                    self.Error = "Invalid duty"
                    self.Duties = list()
                    break
        else:
            self.Error = 'Invalid data'
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
                    "firstName" : self.FirstName,
                    "lastName"  : self.LastName,
                    "nickname"  : self.Nickname,
                    "rank"      : self.Rank,
                    "division"  : self.Division,
                    "duties"    : self.Duties,
                    "serial"    : self.Serial,
                    "stic"      : self.Stic
                 }
        return member
    def deserialize(self,crewMember=dict()):
        self.Error = ''
        for key,value in crewMember.items():
            if key.upper() == 'FirstName'.upper():
                self.FirstName = value
            elif key.upper() == 'LastName'.upper():
                self.LastName = value
            elif key.upper() == 'Nickname'.upper():
                self.Nickname = value
            elif key.upper() == 'Rank'.upper():
                self.Rank = value
            elif key.upper() == 'Division'.upper():
                self.Division = value
            elif key.upper() == 'Duties'.upper():
                self.Duties = value
            elif key.upper() == 'Serial'.upper():
                self.Serial = value
            elif key.upper() == 'Stic'.upper():
                self.Stic = value
            else:
                self.Error = "Attribute not valid"
        return self.Error

class Crew(Addable):
    def __init__(self,crew=list()):
        self.Error = ""
        self.Crew  = crew
    def add(self,member=None):
        self.Error = ""
        if member is CrewMember:
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
        else:
            self.Error = "Incorrect type"
        return self.Error
    def remove(self,member=CrewMember()):
        self.Error = ""
        try:
            if member is CrewMember():
                i = self.Crew.index(member)
                self.Crew.remove(i)
            else:
                self.Error = "Member not valid"
        except Exception as e:
            self.Error = e
        return self.Error
    def serialize(self):
        self.Error = ''
        crew = dict()
        for member in self.Crew:
            crew[member.Nickname] = member.serialize()
        return crew
    def deserialize(self,crew=dict()):
        self.Error = ''
        if crew:
            for key,member in crew:
                if re.match(isAlpha,key):
                    if member is dict():
                        if ('FirstName'.upper() in member.upper() and \
                            re.match(isAlpha,member['FirstName'])) and \
                           ('LastName' in member and \
                            re.match(isAlpha,member['LastName'])) and \
                           ('Nickname' in member and \
                            re.match(isAlpha,member['Nickname'])) and \
                           ('Rank' in member and \
                            re.match(isAlpha,member['Rank'])) and \
                           ('Division' in member and \
                            re.match(isAlpha,member['Division'])) and \
                           ('Serial' in member and \
                            re.match(isNumber,member['Serial'])) and \
                           ('Stic' in member and \
                            re.match(isNumber,member['Stic'])):
                            duties = list()
                            for duty in member['Duties']:
                                if re.match(isAlpha,duty['Name']) and \
                                   re.match(isText,duty['Description']):
                                    d = Duty()
                                    duties.append(Duty(duty['Name'],
                                                  duty['Description'])
                                                 )
                                else:
                                    duties = list()
                                    self.Error = 'Invalid duty'
                                    break
                            if duties:
                                self.Crew.append(CrewMember(member['FirstName'],
                                                 member['LastName'],
                                                 member['Nickname'],
                                                 member['Rank'],
                                                 member['Division'],
                                                 member['Serial'],
                                                 member['Stic'],
                                                 duties)
                                                )
                        else:
                            self.Error = "Invalid first name"
                    else:
                        self.Error = "Invalid crew member"
        else:
            self.Error = "No crew given"
        return self.Error
