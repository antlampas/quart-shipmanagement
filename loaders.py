#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-06-24

from config        import Providers

from model         import loadFromDB
from model         import removeFromDB
from model         import saveToDB
from model         import editDB

from keycloakAdmin import loadFromKeycloak
from keycloakAdmin import removeFromKeycloak
from keycloakAdmin import addToKeycloak
from keycloakAdmin import editKeycloak

def get(what='',pattern=dict()):
    data = None
    if what:
        if what == 'person' or what == 'people':
            if 'keycloak' in Providers.People:
                data = loadFromKeycloak(what,pattern)
            if 'database' in Providers.People:
                data = loadFromDB(what,pattern)
        elif what == 'crewMember' or what == 'crew':
            if 'keycloak' in Providers.Crew:
                data = loadFromKeycloak(what,pattern)
            if 'database' in Providers.Crew:
                data = loadFromDB(what,pattern)
        elif what == 'rank' or what == 'ranks':
            if 'keycloak' in Providers.Ranks:
                data = loadFromKeycloak(what,pattern)
            if 'database' in Providers.Ranks:
                data = loadFromDB(what,pattern)
        elif what == 'division' or what == 'divisions':
            if 'keycloak' in Providers.Divisions:
                data = loadFromKeycloak(what,pattern)
            if 'database' in Providers.Divisions:
                data = loadFromDB(what,pattern)
        elif what == 'duty' or what == 'duties':
            if 'keycloak' in Providers.Duties:
                data = loadFromKeycloak(what,pattern)
            if 'database' in Providers.Duties:
                data = loadFromDB(what,pattern)
        elif what == 'task' or what == 'tasks':
            if 'keycloak' in Providers.Tasks:
                data = loadFromKeycloak(what,pattern)
            if 'database' in Providers.Tasks:
                data = loadFromDB(what,pattern)
        elif what == 'mission' or what == 'missions':
            if 'keycloak' in Providers.Missions:
                data = loadFromKeycloak(what,pattern)
            if 'database' in Providers.Missions:
                data = loadFromDB(what,pattern)
        else:
            return None
        return data
    else:
        return None
def remove(what='',pattern=dict()):
    data = None
    if what:
        if what == 'person' or what == 'people':
            if 'keycloak' in Providers.People:
                data = removeFromKeycloak(what,pattern)
            if 'database' in Providers.People:
                data = removeFromDB(what,pattern)
        elif what == 'crewMember' or what == 'crew':
            if 'keycloak' in Providers.Crew:
                data = removeFromKeycloak(what,pattern)
            if 'database' in Providers.Crew:
                data = removeFromDB(what,pattern)
        elif what == 'rank' or what == 'ranks':
            if 'keycloak' in Providers.Ranks:
                data = removeFromKeycloak(what,pattern)
            if 'database' in Providers.Ranks:
                data = removeFromDB(what,pattern)
        elif what == 'division' or what == 'divisions':
            if 'keycloak' in Providers.Divisions:
                data = removeFromKeycloak(what,pattern)
            if 'database' in Providers.Divisions:
                data = removeFromDB(what,pattern)
        elif what == 'duty' or what == 'duties':
            if 'keycloak' in Providers.Duties:
                data = removeFromKeycloak(what,pattern)
            if 'database' in Providers.Duties:
                data = removeFromDB(what,pattern)
        elif what == 'task' or what == 'tasks':
            if 'keycloak' in Providers.Tasks:
                data = removeFromKeycloak(what,pattern)
            if 'database' in Providers.Tasks:
                data = removeFromDB(what,pattern)
        elif what == 'mission' or what == 'missions':
            if 'keycloak' in Providers.Missions:
                data = removeFromKeycloak(what,pattern)
            if 'database' in Providers.Missions:
                data = removeFromDB(what,pattern)
        else:
            return None
        return data
    else:
        return None
def add(what='',pattern=dict()):
    if what:
        if what == 'person' or what == 'people':
            if 'keycloak' in Providers.People:
                data = addToKeycloak(what,pattern)
            if 'database' in Providers.People:
                data = saveToDB(what,pattern)
        elif what == 'crewMember' or what == 'crew':
            if 'keycloak' in Providers.Crew:
                data = addToKeycloak(what,pattern)
            if 'database' in Providers.Crew:
                data = saveToDB(what,pattern)
        elif what == 'rank' or what == 'ranks':
            if 'keycloak' in Providers.Ranks:
                data = addToKeycloak(what,pattern)
            if 'database' in Providers.Ranks:
                data = saveToDB(what,pattern)
        elif what == 'division' or what == 'divisions':
            if 'keycloak' in Providers.Divisions:
                data = addToKeycloak(what,pattern)
            if 'database' in Providers.Divisions:
                data = saveToDB(what,pattern)
        elif what == 'duty' or what == 'duties':
            if 'keycloak' in Providers.Duties:
                data = addToKeycloak(what,pattern)
            if 'database' in Providers.Duties:
                data = saveToDB(what,pattern)
        elif what == 'task' or what == 'tasks':
            if 'keycloak' in Providers.Tasks:
                data = addToKeycloak(what,pattern)
            if 'database' in Providers.Tasks:
                data = saveToDB(what,pattern)
        elif what == 'mission' or what == 'missions':
            if 'keycloak' in Providers.Missions:
                data = addToKeycloak(what,pattern)
            if 'database' in Providers.Missions:
                data = saveToDB(what,pattern)
        else:
            return None
        return data
    else:
        return None
def edit(what='',pattern=dict()):
    data = None
    if what:
        if what == 'person' or what == 'people':
            if 'keycloak' in Providers.People:
                data = editKeycloak(what,pattern)
            if 'database' in Providers.People:
                data = editDB(what,pattern)
        elif what == 'crewMember' or what == 'crew':
            if 'keycloak' in Providers.Crew:
                data = editKeycloak(what,pattern)
            if 'database' in Providers.Crew:
                data = editDB(what,pattern)
        elif what == 'rank' or what == 'ranks':
            if 'keycloak' in Providers.Ranks:
                data = editKeycloak(what,pattern)
            if 'database' in Providers.Ranks:
                data = editDB(what,pattern)
        elif what == 'division' or what == 'divisions':
            if 'keycloak' in Providers.Divisions:
                data = editKeycloak(what,pattern)
            if 'database' in Providers.Divisions:
                data = editDB(what,pattern)
        elif what == 'duty' or what == 'duties':
            if 'keycloak' in Providers.Duties:
                data = editKeycloak(what,pattern)
            if 'database' in Providers.Duties:
                data = editDB(what,pattern)
        elif what == 'task' or what == 'tasks':
            if 'keycloak' in Providers.Tasks:
                data = editKeycloak(what,pattern)
            if 'database' in Providers.Tasks:
                data = editDB(what,pattern)
        elif what == 'mission' or what == 'missions':
            if 'keycloak' in Providers.Missions:
                data = editKeycloak(what,pattern)
            if 'database' in Providers.Missions:
                data = editDB(what,pattern)
        else:
            return None
        return data
    else:
        return None