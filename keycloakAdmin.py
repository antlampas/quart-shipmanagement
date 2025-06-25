#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-31

import requests

from config import KeycloakConfig

command_prefix = f'{KeycloakConfig.KEYCLOAK_URL}' + \
                 f'/admin/realms/' + \
                 f'{KeycloakConfig.KEYCLOAK_REALM}'

def getAdminAccessToken():
    headers = {
                'content-type' : 'application/x-www-form-urlencoded'
              }
    data = {
             'client_id'  : KeycloakConfig.KEYCLOAK_ADMIN['client_id'],
             'grant_type' : KeycloakConfig.KEYCLOAK_ADMIN['grant_type'],
             'username'   : KeycloakConfig.KEYCLOAK_ADMIN['username'],
             'password'   : KeycloakConfig.KEYCLOAK_ADMIN['password']
           }
    response = requests.post(KeycloakConfig.KEYCLOAK_ADMIN['url'],
                             headers=headers,
                             data=data
                            )

    return response.json()['access_token']

def adminAction(action,params=dict()):
    token = getAdminToken()
    response = None
    headers  = {'authorization' : token}
    if action == 'getUser':
        if params:
            if 'username' in params:
                response = getUser(headers,params['username'])
            else:
                response = None
        else:
            response = getUser(headers)
    elif action == 'addUser':
        if params:
            if 'username' in params:
                response = addUser(headers,params['username'],params)
            else:
                response = None
        else:
            response = None
    elif action == 'saveUser':
        if params:
            if 'username' in params:
                response = saveUser(headers,params['username'],params)
            else:
                response = None
        else:
            response = None
    elif action == 'editUser':
        if params:
            if 'username' in params:
                response = editUser(headers,params['username'],params)
            else:
                response = None
        else:
            response = None
    elif action == 'removeUser':
        if params:
            if 'username' in params:
                response = removeUser(headers,params['username'])
            else:
                response = None
        else:
            response = None
    elif action == 'getRank':
        if params:
            if 'name' in params:
                if 'rank' in params['name']:
                    response = getGroup(headers,params['name'])
                else:
                    response = None
            else:
                response = None
        else:
            response = None
    elif action == 'saveRank':
        if params:
            if 'name' in params:
                if 'rank' in params['name']:
                    response = saveGroup(headers,params['name'],params)
                else:
                    response = None
            else:
                response = None
        else:
            response = None
    elif action == 'editRank':
        if params:
            if 'name' in params:
                if 'rank' in params['name']:
                    response = editGroup(headers,params['name'],params)
                else:
                    response = None
            else:
                response = None
        else:
            response = None
    elif action == 'removeRank':
        if params:
            if 'name' in params:
                if 'rank' in params['name']:
                    response = removeGroup(headers,params['name'])
            else:
                response = None
        else:
            response = None
    elif action == 'getDivision':
        if params:
            if 'name' in params:
                if 'division' in params['name']:
                    response = getGroup(headers,params['name'])
            else:
                response = None
        else:
            response = None
    elif action == 'saveDivision':
        if params:
            if 'name' in params:
                if 'division' in params['name']:
                    response = saveGroup(headers,params['name'],params)
                else:
                    response = None
            else:
                response = None
        else:
            response = None
    elif action == 'editDivision':
        if params:
            if 'name' in params:
                if 'division' in params['name']:
                    response = editGroup(headers,params['name'],params)
                else:
                    response = None
            else:
                response = None
        else:
            response = None
    elif action == 'removeDivision':
        if params:
            if 'name' in params:
                if 'division' in params['name']:
                    response = removeGroup(headers,params['name'])
            else:
                response = None
        else:
            response = None
    elif action == 'getDuty':
        if params:
            if 'name' in params:
                if 'duty' in params['name']:
                    response = getGroup(headers,params['name'])
            else:
                response = None
        else:
            response = None
    elif action == 'saveDuty':
        if params:
            if 'name' in params:
                if 'duty' in params['name']:
                    response = saveGroup(headers,params['name'],params)
                else:
                    response = None
            else:
                response = None
        else:
            response = None
    elif action == 'editDuty':
        if params:
            if 'name' in params:
                if 'duty' in params['name']:
                    response = editGroup(headers,params['name'],params)
                else:
                    response = None
            else:
                response = None
        else:
            response = None
    elif action == 'removeDuty':
        if params:
            if 'name' in params:
                if 'duty' in params['name']:
                    response = removeGroup(headers,params['name'])
            else:
                response = None
        else:
            response = None
    elif action == 'getTask':
        if params:
            if 'name' in params:
                response = {"Warning" : "Implement"}
            else:
                response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'saveTask':
        if params:
            response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'editTask':
        if params:
            response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'removeTask':
        if params:
            if 'name' in params:
                response = {"Warning" : "Implement"}
            else:
                response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'getMission':
        if params:
            if 'name' in params:
                response = {"Warning" : "Implement"}
            else:
                response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'saveMission':
        if params:
            response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'editMission':
        if params:
            response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'removeMission':
        if params:
            if 'name' in params:
                response = {"Warning" : "Implement"}
            else:
                response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}

    requests.get(command_prefix + '/protocol/openid−connect/logout')

    if response and not isinstance(response,dict):
        if response.code == 200 or \
           response.code == 201 or \
           response.code == 204:
            responseContent = response.content.json()
        if response.code == 403:
            return {"Error": "Forbidden"}
        if response.code == 400:
            return {"Error": "Bad Request"}
        if response.code == 500:
            return {"Error": "Internal Server Error"}
    elif isinstance(response,dict):
        responseContent = response
    else:
        responseContent = None
    return responseContent

def loadFromKeycloak(what='',pattern=''):
    data = None
    if what == 'person':
        if pattern:
            data = adminAction('getUser',pattern)
        else:
            data = None
    elif what == 'people':
        if not pattern:
            data = adminAction('getUser')
        else:
            data = adminAction('getUser',pattern)
    elif what == 'crewMember':
        if pattern:
            data = adminAction('getUser',pattern)
        else:
            data = None
    elif what == 'crew':
        if not pattern:
            data = adminAction('getUser')
        else:
            data = adminAction('getUser',pattern)
    elif what == 'rank':
        if pattern:
            data = adminAction('getRank',pattern)
        else:
            data = None
    elif what == 'ranks':
        if not pattern:
            data = adminAction('getRanks')
        else:
            data = adminAction('getRanks',pattern)
    elif what == 'division':
        if pattern:
            data = adminAction('getDivision',pattern)
        else:
            data = None
    elif what == 'divisions':
        if not pattern:
            data = adminAction('getDivisions')
        else:
            data = adminAction('getDivisions',pattern)
    elif what == 'duty':
        if pattern:
            data = adminAction('getDuty',pattern)
        else:
            data = None
    elif what == 'duties':
        if not pattern:
            data = adminAction('getDuties')
        else:
            data = adminAction('getDuties',pattern)
    elif what == 'task':
        if pattern:
            data = adminAction('getTask',pattern)
        else:
            data = None
    elif what == 'tasks':
        if not pattern:
            data = adminAction('getTasks')
        else:
            data = adminAction('getTasks',pattern)
    elif what == 'mission':
        if pattern:
            data = adminAction('getMission',pattern)
        else:
            data = None
    elif what == 'missions':
        if not pattern:
            data = adminAction('getMissions')
        else:
            data = adminAction('getMissions',pattern)
    return data
def removeFromKeycloak(what='',pattern=''):
    data = None
    if what == 'person':
        if pattern:
            data = adminAction('removeUser',pattern)
        else:
            data = None
    elif what == 'people':
        if not pattern:
            data = adminAction('removeUser')
        else:
            data = adminAction('removeUser',pattern)
    elif what == 'crewMember':
        if pattern:
            data = adminAction('removeUser',pattern)
        else:
            data = None
    elif what == 'crew':
        if not pattern:
            data = adminAction('removeUser')
        else:
            data = adminAction('removeUser',pattern)
    elif what == 'rank':
        if pattern:
            data = adminAction('removeRank',pattern)
        else:
            data = None
    elif what == 'ranks':
        if not pattern:
            data = adminAction('removeRanks')
        else:
            data = adminAction('removeRanks',pattern)
    elif what == 'division':
        if pattern:
            data = adminAction('removeDivision',pattern)
        else:
            data = None
    elif what == 'divisions':
        if not pattern:
            data = adminAction('removeDivisions')
        else:
            data = adminAction('removeDivisions',pattern)
    elif what == 'duty':
        if pattern:
            data = adminAction('removeDuty',pattern)
        else:
            data = None
    elif what == 'duties':
        if not pattern:
            data = adminAction('removeDuties')
        else:
            data = adminAction('removeDuties',pattern)
    elif what == 'task':
        if pattern:
            data = adminAction('removeTask',pattern)
        else:
            data = None
    elif what == 'tasks':
        if not pattern:
            data = adminAction('removeTasks')
        else:
            data = adminAction('removeTasks',pattern)
    elif what == 'mission':
        if pattern:
            data = adminAction('removeMission',pattern)
        else:
            data = None
    elif what == 'missions':
        if not pattern:
            data = adminAction('removeMissions')
        else:
            data = adminAction('removeMissions',pattern)
    return data
def saveToKeycloak(what='',data=dict()):
    data = None
    if what == 'person':
        if pattern:
            data = adminAction('saveUser',pattern)
        else:
            data = None
    elif what == 'people':
        if not pattern:
            data = adminAction('saveUser')
        else:
            data = adminAction('saveUser',pattern)
    elif what == 'crewMember':
        if pattern:
            data = adminAction('saveUser',pattern)
        else:
            data = None
    elif what == 'crew':
        if not pattern:
            data = adminAction('saveUser')
        else:
            data = adminAction('saveUser',pattern)
    elif what == 'rank':
        if pattern:
            data = adminAction('saveRank',pattern)
        else:
            data = None
    elif what == 'ranks':
        if not pattern:
            data = adminAction('saveRank')
        else:
            data = adminAction('saveRank',pattern)
    elif what == 'division':
        if pattern:
            data = adminAction('saveDivision',pattern)
        else:
            data = None
    elif what == 'divisions':
        if not pattern:
            data = adminAction('saveDivision')
        else:
            data = adminAction('saveDivision',pattern)
    elif what == 'duty':
        if pattern:
            data = adminAction('saveDuty',pattern)
        else:
            data = None
    elif what == 'duties':
        if not pattern:
            data = adminAction('saveDuties')
        else:
            data = adminAction('saveDuties',pattern)
    elif what == 'task':
        if pattern:
            data = adminAction('saveTask',pattern)
        else:
            data = None
    elif what == 'tasks':
        if not pattern:
            data = adminAction('saveTasks')
        else:
            data = adminAction('saveTasks',pattern)
    elif what == 'mission':
        if pattern:
            data = adminAction('saveMission',pattern)
        else:
            data = None
    elif what == 'missions':
        if not pattern:
            data = adminAction('saveMission')
        else:
            data = adminAction('saveMission',pattern)
    return data
def editKeycloak(what='',pattern=dict()):
    data = None
    if what == 'person':
        if pattern:
            data = adminAction('editUser',pattern)
        else:
            data = None
    elif what == 'people':
        if not pattern:
            data = adminAction('editUser')
        else:
            data = adminAction('editUser',pattern)
    elif what == 'crewMember':
        if pattern:
            data = adminAction('editUser',pattern)
        else:
            data = None
    elif what == 'crew':
        if not pattern:
            data = adminAction('editUser')
        else:
            data = adminAction('editUser',pattern)
    elif what == 'rank':
        if pattern:
            data = adminAction('editRank',pattern)
        else:
            data = None
    elif what == 'ranks':
        if not pattern:
            data = adminAction('editRanks')
        else:
            data = adminAction('editRanks',pattern)
    elif what == 'division':
        if pattern:
            data = adminAction('editDivision',pattern)
        else:
            data = None
    elif what == 'divisions':
        if not pattern:
            data = adminAction('editDivisions')
        else:
            data = adminAction('editDivisions',pattern)
    elif what == 'duty':
        if pattern:
            data = adminAction('editDuty',pattern)
        else:
            data = None
    elif what == 'duties':
        if not pattern:
            data = adminAction('editDuties')
        else:
            data = adminAction('editDuties',pattern)
    elif what == 'task':
        if pattern:
            data = adminAction('editTask')
        else:
            data = None
    elif what == 'tasks':
        if not pattern:
            data = adminAction('editTasks')
        else:
            data = adminAction('editTasks',pattern)
    elif what == 'mission':
        if pattern:
            data = adminAction('editMission')
        else:
            data = None
    elif what == 'missions':
        if not pattern:
            data = adminAction('editMission')
        else:
            data = adminAction('editMission',pattern)
    return data

def getUser(headers,user=''):
    global command_prefix
    response = None
    if user:
        response = requests.get(command_prefix + '/users',
                                headers=headers,
                                params={'username' : user}
                               )
    else:
        response = requests.get(command_prefix + '/users',headers=headers)
    return response
def removeUser(headers,user=''):
    global command_prefix
    response = None
    if user:
        response = requests.delete(command_prefix + f'/users/{user}',
                                   headers=headers
                                  )
    else:
        response = None
    return response
def addUser(headers,user=dict()):
    global command_prefix
    response = None
    if user:
        response = requests.post(command_prefix + '/users',
                                headers=headers,
                                data=user
                               )
    else:
        response = None
    return response
def editUser(headers,user='',attributes=dict()):
    global command_prefix
    response = None
    if user and attributes:
        response = requests.put(command_prefix + f'/users/{user}',
                                headers=headers,
                                data=attributes
                               )
    else:
        response = None
    return response

#TODO: check these functions
def getGroup(headers,group=''):
    global command_prefix
    response = None
    if group:
        response = requests.get(command_prefix + '/groups',
                                headers=headers,
                                params={'group-id' : group}
                               )
    else:
        response = requests.get(command_prefix + '/users',headers=headers)
    return response
def removeGroup(headers,group=''):
    global command_prefix
    response = None
    if user:
        response = requests.delete(command_prefix + f'/groups/{group}',
                                   headers=headers
                                  )
    else:
        response = None
    return response
def addGroup(headers,group=dict()):
    global command_prefix
    response = None
    if user:
        response = requests.post(command_prefix + '/groups',
                                headers=headers,
                                data=group
                               )
    else:
        response = None
    return response
def editGroup(headers,group='',attributes=dict()):
    global command_prefix
    response = None
    if user and attributes:
        response = requests.put(command_prefix + f'/groups/{group}',
                                headers=headers,
                                data=attributes
                               )
    else:
        response = None
    return response

def getTask(headers,task=''):
    global command_prefix
    response = None
    pass #TODO: implement
def removeTask(headers,task=''):
    global command_prefix
    response = None
    pass #TODO: implement
def addTask(headers,task=dict()):
    global command_prefix
    response = None
    pass #TODO: implement
def editTask(headers,task='',attributes=dict()):
    global command_prefix
    response = None
    pass #TODO: implement

def getMission(headers,mission=''):
    global command_prefix
    response = None
    pass #TODO: implement
def removeMission(headers,mission=''):
    global command_prefix
    response = None
    pass #TODO: implement
def addMission(headers,mission=dict()):
    global command_prefix
    response = None
    pass #TODO: implement
def editMission(headers,mission='',attributes=dict()):
    global command_prefix
    response = None
    pass #TODO: implement
