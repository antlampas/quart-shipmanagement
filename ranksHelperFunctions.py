#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-06-24

from ranksClasses import Rank
from ranksClasses import Ranks
from loaders      import load

def isRankPresent(rank=Rank()):
    """
    Checks if the single rank is in datastore
    """
    if rank.Name:
        rankDB = load('rank',rank.Name)
        if rankDB:
            return True
        else:
            return False
    else:
        return False

def ranksMatchDatastore(ranks=Ranks()):
    """
    Checks if the list of ranks is in datastore
    """
    ranksDB = load('ranks')
    if ranksDB:
        ranksList = Ranks(ranksDB)
        if ranksList == ranks:
            return True
        else:
            return False
    else:
        return False