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
                 Serial    = 0,
                 Stic      = 0
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
        if re.match(isAlpha,FirstName):
            self.FirstName = FirstName
            if re.match(isAlpha,LastName):
                self.LastName  = LastName
                if re.match(isAlpha,Nickname):
                    self.Nickname  = Nickname
                    if re.match(isNumber,Serial):
                        self.Serial    = Serial
                        if re.match(isNumber,Stic):
                            self.Stic      = Stic
                            if re.match(isAlpha,Rank):
                                self.Rank      = Rank
                                if re.match(isAlpha,Division):
                                    self.Division  = Division
                                    for Duty in Duties:
                                        if re.match(isAlpha,Duty.Name) and re.match(isText,Duty.Description):
                                            self.Duties.append(Duty)
                                        else:
                                            self.Error = "Invalid duties"
                                            self.Duties = list()
                                            break
                                else:
                                    self.Error = 'Invalid division'
                            else:
                                self.Error = 'Invalid Rank'
                        else:
                            self.Error = 'Invalid STIC number'
                    else:
                        self.Error = 'Invalid serial number'
                else:
                    self.Error = 'Invalid Nickname'
            else:
                self.Error = 'Invalid last name'
        else:
            self.Error = 'Invalid first name'
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
    def deserialize(self,crewMember=dict()):
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
            crew[member.Nickname] = member.serilize()
        return crew
    def deserialize(self,crew=dict()):
        self.Error = ''
        if crew:
            for key,member in crew:
                if re.match(isAlpha,key):
                    if member is dict():
                        if 'FirstName' in member and re.match(isAlpha,member['FirstName']):
                            if 'LastName' in member and re.match(isAlpha,member['LastName']):
                                if 'Nickname' in member and re.match(isAlpha,member['Nickname']):
                                    if 'Rank' in member and re.match(isAlpha,member['Rank']):
                                        if 'Division' in member and re.match(isAlpha,member['Division']):
                                            if 'Serial' in member and re.match(isNumber,member['Serial']):
                                                if 'Stic' in member and re.match(isNumber,member['Stic']):
                                                    duties = list()
                                                    for duty in member['Duties']:
                                                        if re.match(isAlpha,duty['Name']) and re.match(isText,duty['Description']):
                                                            d = Duty()
                                                            duties.append(Duty(duty['Name'],duty['Description']))
                                                        else:
                                                            duties = list()
                                                            self.Error = 'Invalid duty'
                                                            break
                                                    if duties:
                                                        self.Crew.append(CrewMember(member['FirstName'],member['LastName'],member['Nickname'],member['Rank'],member['Division'],member['Serial'],member['Stic'],duties))
                                                else:
                                                    self.Error = 'Invalid stic number'
                                            else:
                                                self.Error = 'Invalid serial member'
                                        else:
                                            self.Error = 'Invalid division'
                                    else:
                                        self.Error = 'Invalid rank'
                                else:
                                    self.Error = 'Invalid nickname'
                            else:
                                self.Error = "Invalid last name"
                        else:
                            self.Error = "Invalid first name"
                    else:
                        self.Error = "Invalid crew member"
        else:
            self.Error = "No crew given"
        return self.Error
