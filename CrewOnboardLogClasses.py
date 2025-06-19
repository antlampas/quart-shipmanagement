#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-06-15

import re

from baseClasses import Editable
from baseClasses import Addable

from utilities   import isAlpha
from utilities   import isNumber
from utilities   import isText

class MemberOnboardLog:
    def __init__(self,memberLog=dict()):
        self.CrewMember        = ""
        self.OnboardPeriods    = list()
        self.PreviousDivisions = list()
        self.PreviousDuties    = list()
        self.PreviousTasks     = list()
        self.PreviousMissions  = list()
    def edit(self,attributes=dict()):
        self.Error = ""
        pass
    def serialize(self):
        self.Error = ''
        pass
    def deserialize(self,memberLog=dict()):
        self.Error = ''
        pass

class OnboardLog:
    def __init__(self,logEntry=list()):
        self.logEntry = list()
    def add(self,task=None):
        self.Error = ""
        pass
    def serialize(self):
        self.Error = ''
        pass
    def remove(self,task=None):
        self.Error = ""
        pass
    def deserialize(self,memberLogs=dict()):
        self.Error = ''
        pass
