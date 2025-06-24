#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-06-24

from divisionsClasses import Division
from divisionsClasses import Divisions
from loaders          import load

def isDivisionPresent(division=Division()):
    """
    Checks if the single division is in datastore
    """
    if division.Name:
        divisionDB = load('division',division.Name)
        if divisionDB:
            return True
        else:
            return False
    else:
        return False

def divisionsMatchDatastore(divisions=Divisions()):
    """
    Checks if the list of divisions is in datastore
    """
    divisionsDB = load('divisions')
    if divisionsDB:
        divisionsList = Divisions(divisionsDB)
        if divisionsList == divisions:
            return True
        else:
            return False
    else:
        return False
