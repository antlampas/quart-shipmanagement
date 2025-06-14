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
                try:
                    attribute = getattr(self,key)
                    attribute = value
                except Exception as e:
                    self.Error = e
        return self.Error
    def serialize(self):
        self.Error = ''
        division = {
                        "Name"        : self.Name,
                        "Description" : self.Description
                   }
    def deserilize(self,division=dict()):
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
        for division in divisions:
            if division is Division:
                if re.match(isAlpha,division.Name):
                    if re.match(isAlphanumeric,division.Description):
                        self.Divisions.append(division)
                    else:
                        self.Error = "Division description not text"
                        break
                else:
                    self.Error = "Division name not alpha"
                    break
            else:
                self.Error("Division not valid")
                break
    def add(self,division=None):
        self.Error = ""
        if division is Division:
            if re.match(isAlpha,division.Name) and \
               re.match(isAlphanumeric,division.Description):
