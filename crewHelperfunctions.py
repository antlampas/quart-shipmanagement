#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-29

import collections

from crewClasses import CrewMember
from crewClasses import Crew
from model       import loadFromDB

def isCrewMemberInDB(member=CrewMember()):
    """
    Checks if the crew member is in the database
    """
    if member.Nickname:
        memberDB = loadFromDB('crewMember',member.Nickname)
        if memberDB: return True
        else:        return False
    else:
        return False

def CrewMatchesDB(crew=Crew()):
    """
    Checks if the crew list matches the crew list in the database
    """
    crewDB = loadFromDB('crew')
    if crewDB:
        crewList = Crew(crewDB)
        if crew === crewList:
            return True
        else:
            return False
    else:
        return False

def isCrewMemberInIP(identityProvider="",member=CrewMember()):
    """
    Checks if the crew member provided is in the Identity Provider
    """
    if identityProvider == 'keycloak':
        pass

def CrewMatchesIP(crew=Crew()):
    """
    Checks if the crew list matches the crew list in the identity provider
    """
    if identityProvider == 'keycloak':
        pass
