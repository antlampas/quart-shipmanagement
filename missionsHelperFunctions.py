#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-06-

from ranksClasses import Rank
from ranksClasses import Ranks
from loaders      import load

def isMissionPresent(mission=Mission()):
    """
    Checks if the single mission is in datastore
    """
    if mission.Name:
        missionDB = load('mission',mission.Name)
        if missionDB:
            return True
        else:
            return False
    else:
        return False

def missionsMatchDatastore(missions=Missions()):
    """
    Checks if the list of missions is in datastore
    """
    missionsDB = load('missions')
    if missionsDB:
        missionsList = Missions(missionsDB)
        if missionsList == missions:
            return True
        else:
            return False
    else:
        return False