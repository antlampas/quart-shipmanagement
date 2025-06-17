#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from config import Providers

from model import loadFromDB
from model import RemoveFromDB
from model import saveToDB
from model import editDB

from keycloakAdmin import loadFromKeycloak
from keycloakAdmin import RemoveFromKeycloak
from keycloakAdmin import saveToKeycloak
from keycloakAdmin import editKeycloak

#### Regular expressions ####
isAlpha        = r"^[A-Za-z]+$"
isNumber       = r"^[0-9]+$"
isAlphanumeric = r"^[A-Za-z][0-9]+$"
isText         = r"^[A-Za-z][0-9][,;.:-_!/(/)àèéìòù]+$"
isPath         = r"\/[A-Za-z0-9]+"
#### End regular expressions ####

#### Utility functions ####
def load(what='',pattern=''):
    if what:
        if what == 'person' or what == 'people':
            if 'keycloak' in Providers.People:
                loadFromKeycloak(what,pattern)
            if 'database' in Providers.People:
                loadFromDB(what,pattern)
        elif what == 'crewMember' or what == 'crew':
            if 'keycloak' in Providers.Crew:
                loadFromKeycloak(what,pattern)
            if 'database' in Providers.Crew:
                loadFromDB(what,pattern)
        elif what == 'rank' or what == 'ranks':
            if 'keycloak' in Providers.Ranks:
                loadFromKeycloak(what,pattern)
            if 'database' in Providers.Ranks:
                loadFromDB(what,pattern)
        elif what == 'division' or what == 'divisions':
            if 'keycloak' in Providers.Divisions:
                loadFromKeycloak(what,pattern)
            if 'database' in Providers.Divisions:
                loadFromDB(what,pattern)
        elif what == 'duty' or what == 'duties':
            if 'keycloak' in Providers.Duties:
                paloadFromKeycloak(what,pattern)
            if 'database' in Providers.Duties:
                loadFromDB(what,pattern)
        elif what == 'task' or what == 'tasks':
            if 'keycloak' in Providers.Tasks:
                loadFromKeycloak(what,pattern)
            if 'database' in Providers.Tasks:
                loadFromDB(what,pattern)
        elif what == 'mission' or what == 'missions':
            if 'keycloak' in Providers.Missions:
                loadFromKeycloak(what,pattern)
            if 'database' in Providers.Missions:
                loadFromDB(what,pattern)
def remove(what='',pattern=''):
    if what:
        if what == 'person' or what == 'people':
            if 'keycloak' in Providers.People:
                removeFromKeycloak(what,pattern)
            if 'database' in Providers.People:
                removeFromDB(what,pattern)
        elif what == 'crewMember' or what == 'crew':
            if 'keycloak' in Providers.Crew:
                removeFromKeycloak(what,pattern)
            if 'database' in Providers.Crew:
                removeFromDB(what,pattern)
        elif what == 'rank' or what == 'ranks':
            if 'keycloak' in Providers.Ranks:
                removeFromKeycloak(what,pattern)
            if 'database' in Providers.Ranks:
                removeFromDB(what,pattern)
        elif what == 'division' or what == 'divisions':
            if 'keycloak' in Providers.Divisions:
                removeFromKeycloak(what,pattern)
            if 'database' in Providers.Divisions:
                removeFromDB(what,pattern)
        elif what == 'duty' or what == 'duties':
            if 'keycloak' in Providers.Duties:
                removeFromKeycloak(what,pattern)
            if 'database' in Providers.Duties:
                removeFromDB(what,pattern)
        elif what == 'task' or what == 'tasks':
            if 'keycloak' in Providers.Tasks:
                removeFromKeycloak(what,pattern)
            if 'database' in Providers.Tasks:
                removeFromDB(what,pattern)
        elif what == 'mission' or what == 'missions':
            if 'keycloak' in Providers.Missions:
                removeFromKeycloak(what,pattern)
            if 'database' in Providers.Missions:
                removeFromDB(what,pattern)
def save(what='',data=dict()):
    if what:
        if what == 'person' or what == 'people':
            if 'keycloak' in Providers.People:
                saveToKeycloak(what,pattern)
            if 'database' in Providers.People:
                saveToDB(what,pattern)
        elif what == 'crewMember' or what == 'crew':
            if 'keycloak' in Providers.Crew:
                saveToKeycloak(what,pattern)
            if 'database' in Providers.Crew:
                saveToDB(what,pattern)
        elif what == 'rank' or what == 'ranks':
            if 'keycloak' in Providers.Ranks:
                saveToKeycloak(what,pattern)
            if 'database' in Providers.Ranks:
                saveToDB(what,pattern)
        elif what == 'division' or what == 'divisions':
            if 'keycloak' in Providers.Divisions:
                saveToKeycloak(what,pattern)
            if 'database' in Providers.Divisions:
                saveToDB(what,pattern)
        elif what == 'duty' or what == 'duties':
            if 'keycloak' in Providers.Duties:
                saveToKeycloak(what,pattern)
            if 'database' in Providers.Duties:
                saveToDB(what,pattern)
        elif what == 'task' or what == 'tasks':
            if 'keycloak' in Providers.Tasks:
                saveToKeycloak(what,pattern)
            if 'database' in Providers.Tasks:
                saveToDB(what,pattern)
        elif what == 'mission' or what == 'missions':
            if 'keycloak' in Providers.Missions:
                saveToKeycloak(what,pattern)
            if 'database' in Providers.Missions:
                saveToDB(what,pattern)
def edit(what='',data=dict()):
    if what:
        if what == 'person' or what == 'people':
            if 'keycloak' in Providers.People:
                editKeycloak(what,pattern)
            if 'database' in Providers.People:
                editDB(what,pattern)
        elif what == 'crewMember' or what == 'crew':
            if 'keycloak' in Providers.Crew:
                editKeycloak(what,pattern)
            if 'database' in Providers.Crew:
                editDB(what,pattern)
        elif what == 'rank' or what == 'ranks':
            if 'keycloak' in Providers.Ranks:
                editKeycloak(what,pattern)
            if 'database' in Providers.Ranks:
                editDB(what,pattern)
        elif what == 'division' or what == 'divisions':
            if 'keycloak' in Providers.Divisions:
                editKeycloak(what,pattern)
            if 'database' in Providers.Divisions:
                editDB(what,pattern)
        elif what == 'duty' or what == 'duties':
            if 'keycloak' in Providers.Duties:
                editKeycloak(what,pattern)
            if 'database' in Providers.Duties:
                editDB(what,pattern)
        elif what == 'task' or what == 'tasks':
            if 'keycloak' in Providers.Tasks:
                editKeycloak(what,pattern)
            if 'database' in Providers.Tasks:
                editDB(what,pattern)
        elif what == 'mission' or what == 'missions':
            if 'keycloak' in Providers.Missions:
                editKeycloak(what,pattern)
            if 'database' in Providers.Missions:
                editDB(what,pattern)
#### End utility functions ####