#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-06-24

from dutiesClasses import Duty
from dutiesClasses import Duties
from loaders       import load

def isDutyPresent(duty=Duty()):
    """
    Checks if the single duty is in datastore
    """
    if Duty.Name:
        dutyDB = load('duty',duty.Name)
        if dutyDB:
            return True
        else:
            return False
    else:
        return False

def dutiesMatchDatastore(duties=Duties()):
    """
    Checks if the list of duties is in datastore
    """
    dutiesDB = load('duties')
    if dutiesDB:
        dutiesList = Duties(dutiesDB)
        if dutiesList == duties:
            return True
        else:
            return False
    else:
        return False