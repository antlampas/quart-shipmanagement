#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from sqlalchemy     import select
from sqlalchemy.orm import Session

from model          import db
from model          import CrewMemberTable
from model          import DutyTable
from model          import selectDuty

from utilities      import isAlpha
from utilities      import isNumber

from baseClasses    import Editable
from baseClasses    import Addable

class Duty(Editable):
    def __init__(self,source="db",name="",description=""):
        self.Error       = ""
        self.Source      = source
        self.Name        = name
        self.Description = description
    def edit(self,attributes=dict()):
        self.Error = ""
        duty       = None
        if self.source == "db":
            with db.bind.Session() as s:
                with s.begin():
                    duty = s.scalar(selectDuty(self.Name))
        for key,value in attributes:
            try:
                attribute = getattr(self,key)
                attribute = value
            except Exception as e:
                self.Error = e
        if re.match(isAlpha,self.Name):
            self.Error = "Duty name not valid"
        if self.Error:
            return self.Error
        #TODO: Make it work with keycloack too
        if self.Source == "db":
            if duty:
                duty.Name        = self.Name
                duty.Description = self.Description
                with db.bind.Session() as s:
                    with s.begin():
                        s.commit()
            else:
                duty = DutyTable(Name=self.Name,Description=self.Description)
                with db.bind.Session() as s:
                    with s.begin():
                        s.add(duty)
                        s.commit()
        return self.Error
    def load(self):
        pass

class Duties(Addable):
    def __init__(self,source="db",duties=list()):
        self.Error  = ""
        self.Source = source
        self.Duties = duties
        dutiesDB = list()
        #TODO: Make it work with keycloack too
        if self.Source == "db":
            with db.bind.Session() as s:
                with s.begin():
                    dutiesDB = s.scalars(selectCrew()).all()
            if dutiesDB:
                for duty in dutiesDB:
                    if re.match(isAlpha,duty.Name):
                        self.duties.append(DutyTable(duty.Name,duty.Description))
                    else:
                        self.Error = "Duty name not valid"
                        return self.Error
            else:
                self.Error = "No duties found"
    def add(self,duty=""):
        self.Error  = ""
        if duty:
            if re.match(isAlpha,duty.Name):
                self.duties.append(duty)
            else:
                self.Error = "Duty name is not valid"
        return self.Error
    def remove(self,duty=""):
        self.Error = ""
        try:
            self.duties.remove(duty)
        except Exception as e:
            self.Error = e
        return self.Error
    def load(self):
        pass
