#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-29

from crewClasses import CrewMember
from crewClasses import Crew
from loaders     import load

def isCrewMemberPresent(member=CrewMember()):
    """
    Checks if the single member of the crew is in datastore
    """
    if member.Nickname:
        memberDB = load('crewMember',member.Nickname)
        if memberDB:
            return True
        else:
            return False
    else:
        return False

def crewMatchDatastore(crew=Crew()):
    """
    Checks if the list of the crew matches the crew list in datastore
    """
    crewDB = load('crew')
    if crewDB:
        crewList = Crew(crewDB)
        if crew == crewList:
            return True
        else:
            return False
    else:
        return False