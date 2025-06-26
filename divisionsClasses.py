#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from sqlalchemy     import select
from sqlalchemy.orm import Session

from model          import db
from model          import CrewMemberTable
from model          import DivisionTable
from model          import selectDivision

from utilities      import isAlpha
from utilities      import isNumber
from utilities      import isAlphanumeric
from utilities      import isText

from baseClasses    import Editable
from baseClasses    import Addable

class Division(Editable):
    def __init__(self,name="",description=""):
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
        division   = None
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
        division = {
                        "Name"        : self.Name,
                        "Description" : self.Description
                   }
        return division
    def deserialize(self,division=dict()):
        self.Error = ''
        if attribute:
            for key,value in division:
                if key == "Name":
                    self.Name = value
                elif key == "Description":
                    self.Description = value
                else:
                    self.Error = "Attribute not valid"
                    break
            return self.Error

class Divisions(Addable):
    def __init__(self,divisions=list()):
        self.Error     = ""
        self.Divisions = list()
        if divisions:
            for division in divisions:
                if division is Division:
                    if re.match(isAlpha,division.Name):
                        if re.match(isAlphanumeric,division.Description):
                            self.Divisions.append(division)
                        else:
                            self.Error = "Description not text"
                            break
                    else:
                        self.Error = "Name not alpha"
                        break
                else:
                    self.Error = "Division not valid"
                    break
        else:
            self.Error = 'No divisions provided'
    def add(self,division=None):
        self.Error = ""
        if division:
            if division is Division:
                if re.match(isAlpha,division.Name):
                    if re.match(isAlphanumeric,division.Description):
                       self.Divisions.append(division)
                    else:
                        self.Error = "Description not text"
                        break
                else:
                    self.Error = "Name not alpha"
                    break
            else:
                self.Error = "Division not valid"
        else:
            self.Error = "No division provided"
        return self.Error
    def remove(self,division=None):
        self.Error = ""
        if division:
            try:
                if division is Division:
                    i = self.Divisions.index(division)
                    self.Divisions.remove(i)
                else:
                    self.Error = "Division not valid"
            except Exception as e:
                self.Error = e
        else:
            self.Error = "No division provided"
        return self.Error
    def serialize(self):
        self.Error = ''
        divisions = dict()
        for division in self.Divisions:
            divisions[division.Name] = division.serialize()
        return divisions
    def deserialize(self,divisions=dict()):
        self.Error = ''
        if divisions:
            for key,division in divisions:
                if re.match(isAlpha,key):
                    if division is dict():
                        if 'Name' in division and re.match(isAlpha,division['Name']):
                            if 'Description' in division and re.match(isAlpha,division['Description']):
                                self.Divisions.append(Division(division['Name'],division['Description']))
                            else:
                                self.Error = "Invalid description"
                                break
                        else:
                            self.Error = "Invalid Name"
                            break
                    else:
                        self.Error = "Division not valid"
                        break
        else:
            self.Error = "No divisions given"
        return self.Error
