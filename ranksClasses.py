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
        rank   = None
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
    def serialize(self):
        self.Error = ''
        rank = {
                        "Name"        : self.Name,
                        "Description" : self.Description
                   }
        return rank
    def deserialize(self,rank=dict()):
        self.Error = ''
        if attribute:
            for key,value in rank:
                if key == "Name":
                    self.Name = value
                elif key == "Description":
                    self.Description = value
                else:
                    self.Error = "Attribute not valid"
                    break
            return self.Error

class Ranks(Addable):
    def __init__(self,ranks=list()):
        self.Error  = ""
        self.Ranks  = list()
        if ranks:
            for rank in ranks:
                if rank is Rank:
                    if re.match(isAlpha,rank.Name):
                        if re.match(isAlphanumeric,rank.Description):
                            self.Ranks.append(rank)
                        else:
                            self.Ranks = list()
                            self.Error = "Description not text"
                            break
                    else:
                        self.Ranks = list()
                        self.Error = "Name not alpha"
                        break
                else:
                    self.Ranks = list()
                    self.Error = "Rank not valid"
                    break
        else:
            self.Error = 'No ranks provided'
    def add(self,rank=None):
        self.Error = ""
        if rank:
            if rank is Rank:
                if re.match(isAlpha,rank.Name):
                    if re.match(isAlphanumeric,rank.Description):
                       self.Divisions.append(rank)
                    else:
                        self.Error = "Description not text"
                else:
                    self.Error = "Name not alpha"
            else:
                self.Error = "Rank not valid"
        else:
            self.Error = "No Rank provided"
        return self.Error
    def remove(self,rank=None):
        self.Error = ""
        if rank:
            try:
                if rank is Rank:
                    i = self.Ranks.index(rank)
                    self.Ranks.remove(i)
                else:
                    self.Error = "Rank not valid"
            except Exception as e:
                self.Error = e
        else:
            self.Error = "No rank provided"
        return self.Error
    def serialize(self):
        self.Error = ''
        ranks = dict()
        for rank in self.Ranks:
            ranks[rank.Name] = rank.serilize()
        return ranks
    def deserialize(self,ranks=dict()):
        self.Error = ''
        if ranks:
            for key,rank in ranks:
                if re.match(isAlpha,key):
                    if rank is dict():
                        if 'Name' in rank and re.match(isAlpha,rank['Name']):
                            if 'Description' in rank and re.match(isAlpha,rank['Description']):
                                self.Ranks.append(Ranks(rank['Name'],rank['Description']))
                            else:
                                self.Error = "Invalid description"
                                break
                        else:
                            self.Error = "Invalid Name"
                            break
                    else:
                        self.Error = "Rank not valid"
                        break
        else:
            self.Error = "No ranks given"
        return self.Error
