#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from sqlalchemy     import select
from sqlalchemy.orm import Session

from model          import db
from model          import CrewMemberTable
from model          import RankTable
from model          import selectRank

from utilities      import isAlpha
from utilities      import isNumber

from baseClasses    import Editable
from baseClasses    import Addable

class Rank(Editable):
    def __init__(self,source="db",Name="",Description=""):
        self.Error       = ""
        self.Source      = source
        self.Name        = Name
        self.Description = Description
    def edit(self,attributes:dict):
        for key,value in attributes:
            try:
                attribute = getattr(self,key)
                attribute = value
            except Exception as e:
                self.Error = e
        if self.Error:
            return self.Error
        #TODO: Make it work with keycloack too
        if self.Source=="db":
            rank = RankTable(Name=self.Name,Description=self.Description)
            with db.bind.Session() as s:
                with s.begin():
                    s.commit()
    def load(self,Rank=""):
        #TODO: Make it work with keycloack too
        if self.Source == "db":
            with db.bind.Session() as s:
                with s.begin():
                    if Rank:
                        rank = s.scalar(selectRank(Rank))
                        if rank:
                            self.Name        = rank.Name
                            self.Description = rank.Description
                        else:
                            self.Error = "No rank found"
                    else:
                        self.Error = "Search clause missing"
        return self.Error

class Ranks(Addable):
    def __init__(self,source="db"):
        self.Error  = ""
        self.Source = "db"
        self.Ranks  = list()
        #TODO: Make it work with keycloack too
        if self.Source == "db":
            with db.bind.Session() as s:
                with s.begin():
                    ranks = s.scalars(selectRank()).all()
                    if ranks:
                        for rank in ranks:
                            self.Ranks.append(rank)
                    else:
                        self.Error = "No duties found"
    def add(self,rank:Rank):
        if re.match(isAlpha,rank.Name):
            self.Crew.append(rank)
        return self.Error
    def remove(self,rank:Rank):
        try:
            #TODO: Make it work with keycloack too
            if self.source == "db":
                with db.bind.Session() as s:
                    with s.begin():
                        rankRecord = s.scalar(selectRank(rank.Name))
                        if rankRecord:
                            try:
                                s.remove(rankRecord)
                                s.commit()
                                self.Crew.remove(rankRecord)
                            except Exception as e:
                                self.Error = "Error committing to database"
                        else:
                            self.Error = "No rank found"
        except Exception as e:
            self.Error = e
        return self.Error
