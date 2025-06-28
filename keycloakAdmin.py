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
    token = getAdminAccessToken()
    response = None
    headers  = {'authorization' : token}
    if action == 'getUser':
        if params:
            if 'username' in params:
                response = getUser(headers,params['username'])
            else:
                response = {'Error' : 'No username provided'}
        else:
            response = getUser(headers)
    elif action == 'addUser':
        if params:
            if 'username' in params:
                response = addUser(headers,params['username'],params)
            else:
                response = {'Error' : 'No username provided'}
        else:
            response = {'Error' : 'No user attributes provided'}
    elif action == 'editUser':
        if params:
            if 'username' in params:
                response = editUser(headers,params['username'],params)
            else:
                response = {'Error' : 'No username provided'}
        else:
            response = {'Error' : 'No user attributes provided'}
    elif action == 'removeUser':
        if params:
            if 'username' in params:
                response = removeUser(headers,params['username'])
            else:
                response = {'Error' : 'No username provided'}
        else:
            response = {'Error' : 'No parameters provided'}
    elif action == 'getRank':
        if params:
            if 'name' in params:
                if 'ranks' in params['name']:
                    response = getGroup(headers,params['name'])
                else:
                    response = {'Error' : 'No rank name provided'}
            else:
                response = {'Error' : 'No rank attributes provided'}
        else:
            response = None
    elif action == 'addRank':
        if params:
            if 'name' in params:
                params['name'] = '/ranks/'+params['name']
                response = addGroup(headers,params['name'],params)
            else:
                response = {'Error' : 'No rank name provided'}
        else:
            response = {'Error' : 'No rank attributes provided'}
    elif action == 'editRank':
        if params:
            if 'name' in params:
                params['name'] = '/ranks/'+params['name']
                response = addGroup(headers,params['name'],params)
            else:
                response = {'Error' : 'No rank name provided'}
        else:
            response = {'Error' : 'No rank attributes provided'}
    elif action == 'removeRank':
        if params:
            if 'name' in params:
                params['name'] = '/ranks/'+params['name']
                response = addGroup(headers,params['name'],params)
            else:
                response = {'Error' : 'No rank name provided'}
        else:
            response = {'Error' : 'No rank attributes provided'}
    elif action == 'getDivision':
        if params:
            if 'name' in params:
                params['name'] = '/divisions/'+params['name']
                response = getGroup(headers,params['name'])
            else:
                response = {'Error' : 'No division name provided'}
        else:
            response = {'Error' : 'No division attributes provided'}
    elif action == 'addDivision':
        if params:
            if 'name' in params:
                params['name'] = '/divisions/'+params['name']
                response = addGroup(headers,params['name'])
            else:
                response = {'Error' : 'No division name provided'}
        else:
            response = {'Error' : 'No division attributes provided'}
    elif action == 'editDivision':
        if params:
            if 'name' in params:
                params['name'] = '/divisions/'+params['name']
                response = editGroup(headers,params['name'])
            else:
                response = {'Error' : 'No division name provided'}
        else:
            response = {'Error' : 'No division attributes provided'}
    elif action == 'removeDivision':
        if params:
            if 'name' in params:
                params['name'] = '/divisions/'+params['name']
                response = removeGroup(headers,params['name'])
            else:
                response = {'Error' : 'No division name provided'}
        else:
            response = {'Error' : 'No division attributes provided'}
    elif action == 'getDuty':
        if params:
            if 'name' in params:
                params['name'] = '/duties/'+params['name']
                response = getGroup(headers,params['name'])
            else:
                response = {'Error' : 'No duty name provided'}
        else:
            response = {'Error' : 'No duty attributes provided'}
    elif action == 'addDuty':
        if params:
            if 'name' in params:
                params['name'] = '/duties/'+params['name']
                response = addGroup(headers,params['name'])
            else:
                response = {'Error' : 'No duty name provided'}
        else:
            response = {'Error' : 'No duty attributes provided'}
    elif action == 'editDuty':
        if params:
            if 'name' in params:
                params['name'] = '/duties/'+params['name']
                response = editGroup(headers,params['name'])
            else:
                response = {'Error' : 'No duty name provided'}
        else:
            response = {'Error' : 'No duty attributes provided'}
    elif action == 'removeDuty':
        if params:
            if 'name' in params:
                params['name'] = '/duties/'+params['name']
                response = removeGroup(headers,params['name'])
            else:
                response = {'Error' : 'No duty name provided'}
        else:
            response = {'Error' : 'No duty attributes provided'}
    elif action == 'getTask':
        if params:
            if 'name' in params:
                response = {"Warning" : "Implement"}
            else:
                response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'addTask':
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
    elif action == 'addMission':
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
        elif response.code == 403:
            return {"Error": "Forbidden"}
        elif response.code == 400:
            return {"Error": "Bad Request"}
        elif response.code == 500:
            return {"Error": "Internal Server Error"}
        else:
            return {"Error": "Error code: " + response.code}
    elif isinstance(response,dict):
        responseContent = response
    else:
        responseContent = {"Error": "Unknown error"}
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
def addToKeycloak(what='',pattern=dict()):
    data = None
    if what == 'person':
        if pattern:
            data = adminAction('addUser',pattern)
        else:
            data = None
    elif what == 'people':
        if not pattern:
            data = adminAction('addUser')
        else:
            data = adminAction('addUser',pattern)
    elif what == 'crewMember':
        if pattern:
            data = adminAction('addUser',pattern)
        else:
            data = None
    elif what == 'crew':
        if not pattern:
            data = adminAction('addUser')
        else:
            data = adminAction('addUser',pattern)
    elif what == 'rank':
        if pattern:
            data = adminAction('addRank',pattern)
        else:
            data = None
    elif what == 'ranks':
        if not pattern:
            data = adminAction('addRank')
        else:
            data = adminAction('addRank',pattern)
    elif what == 'division':
        if pattern:
            data = adminAction('addDivision',pattern)
        else:
            data = None
    elif what == 'divisions':
        if not pattern:
            data = adminAction('addDivision')
        else:
            data = adminAction('addDivision',pattern)
    elif what == 'duty':
        if pattern:
            data = adminAction('addDuty',pattern)
        else:
            data = None
    elif what == 'duties':
        if not pattern:
            data = adminAction('addDuties')
        else:
            data = adminAction('addDuties',pattern)
    elif what == 'task':
        if pattern:
            data = adminAction('addTask',pattern)
        else:
            data = None
    elif what == 'tasks':
        if not pattern:
            data = adminAction('addTasks')
        else:
            data = adminAction('addTasks',pattern)
    elif what == 'mission':
        if pattern:
            data = adminAction('addMission',pattern)
        else:
            data = None
    elif what == 'missions':
        if not pattern:
            data = adminAction('addMission')
        else:
            data = adminAction('addMission',pattern)
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
    if group:
        response = requests.delete(command_prefix + f'/groups/{group}',
                                   headers=headers
                                  )
    else:
        response = None
    return response
def addGroup(headers,group=dict()):
    global command_prefix
    response = None
    if group:
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
    if group and attributes:
        response = requests.put(command_prefix + f'/groups/{group}',
                                headers=headers,
                                data=attributes
                               )
    else:
        response = None
    return response

#TODO: Implement these functions
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

#TODO: Implement these functions
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
