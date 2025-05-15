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

from baseClasses    import Editable
from baseClasses    import Addable

class Division(Editable):
    def __init__(self,source="db",name="",description=""):
        self.Error       = ""
        self.Source      = Source
        self.Name        = Name
        self.Description = Description
        #TODO: look for the division in the source
    def edit(self,attributes=dict()):
        self.Error = ""
        division   = None
        #TODO: look for the division in the source

class Divisions(Addable):
    def __init__(self,source="db",divisions=list()):
        self.Error     = ""
        self.Source    = source
        self.Divisions = divisions
        #TODO: look for the division in the source
