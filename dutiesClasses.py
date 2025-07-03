#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from sqlalchemy     import select
from sqlalchemy.orm import Session

from model          import db
from model          import CrewMemberTable
from model          import DutyTable
from model          import selectDuty

from utilities      import isAlpha
from utilities      import isNumber
from utilities      import isAlphanumeric
from utilities      import isText

from baseClasses    import Editable
from baseClasses    import Addable

class Duty(Editable):
    def __init__(self,name='',description=''):
        self.Error       = ""
        if re.match(isAlpha,name):
            self.Name        = name
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
        duty       = None
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
        duty = {
                "name"        : self.Name,
                "description" : self.Description
               }
        return duty
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
class Duties(Addable):
    def __init__(self,duties=list()):
        self.Error  = ""
        self.Duties = duties
        for duty in duties:
            if duty is Duty:
                if re.match(isAlpha,duty.Name):
                    if re.match(isAlphanumeric,duty.Description):
                        self.Divisions.append(duty)
                    else:
                        self.Error = "Description not text"
                        break
                else:
                    self.Error = "Name not alpha"
                    break
            else:
                self.Error = "Duty not valid"
                break
    def add(self,duty=""):
        self.Error  = ""
        if duty:
            if duty is Duties:
                if re.match(isAlpha,duty.Name):
                    if re.match(isAlphanumeric,duty.Description):
                       self.Divisions.append(duty)
                    else:
                        self.Error = "Description not text"
                else:
                    self.Error = "Name not alpha"
            else:
                self.Error = "Duty not valid"
        else:
            self.Error = "No duty provided"
        return self.Error
    def remove(self,duty=None):
        self.Error = ""
        if duty:
            try:
                if duty is Duty:
                    i = self.Divisions.index(duty)
                    self.Divisions.remove(i)
                else:
                    self.Error = "Duty not valid"
            except Exception as e:
                self.Error = e
        else:
            self.Error = "No duty provided"
        return self.Error
    def serialize(self):
        self.Error = ''
        divisions = dict()
        for duty in self.Duties:
            duties[duty.Name] = duty.serialize()
        return duties
    def deserialize(self,duties=dict()):
        self.Error = ''
        if duties:
            for key,duty in duties:
                if re.match(isAlpha,key):
                    if duty is dict():
                        if 'Name' in duty and re.match(isAlpha,duty['Name']):
                            if 'Description' in duty and re.match(isAlpha,duty['Description']):
                                self.Duties.append(Duty(duty['Name'],duty['Description']))
                            else:
                                self.Error = "Invalid description"
                                break
                        else:
                            self.Error = "Invalid Name"
                            break
                    else:
                        self.Error = "Invalid duty"
                        break
        else:
            self.Error = "No duties given"
        return self.Error
