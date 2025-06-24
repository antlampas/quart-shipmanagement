#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-31

import requests

token = ''

command_prefix = f'{current_app.config["KEYCLOAK_URL"]}' + \
                 f'/admin/realms/' + \
                 f'{current_app.config["KEYCLOAK_REALM"]}'

def getAdminAccessToken():
    headers = {
                'content-type' : 'application/x-www-form-urlencoded'
              }
    data = {
             'client_id'  : current_app.config['KEYCLOAK_ADMIN']['client_id'],
             'grant_type' : current_app.config['KEYCLOAK_ADMIN']['grant_type'],
             'username'   : current_app.config['KEYCLOAK_ADMIN']['username'],
             'password'   : current_app.config['KEYCLOAK_ADMIN']['password']
           }
    response = requests.post(current_app.config['KEYCLOAK_ADMIN']['url'],
                             headers=headers,
                             data=data
                            )

    return response.json()['access_token']

def adminAction(action,params=dict()):
    global token
    if not token:
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
            response = addUser(headers,params['username'],params)
        else:
            response = None
    elif action == 'saveUser':
        if params:
            response = saveUser(headers,params['username'],params)
        else:
            response = None
    elif action == 'editUser':
        if params:
            response = editUser(headers,params['username'],params)
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
    elif action == 'saveRank':
        if params:
            if 'rank' in params['name']:
                response = saveGroup(headers,params['name'],params)
        else:
            response = None
    elif action == 'editRank':
        if params:
            if 'rank' in params['name']:
                response = editGroup(headers,params['name'],params)
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
            if 'division' in params['name']:
                response = saveGroup(headers,params['name'],params)
        else:
            response = None
    elif action == 'editDivision':
        if params:
            if 'division' in params['name']:
                response = editGroup(headers,params['name'],params)
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
            if 'duty' in params['name']:
                response = saveGroup(headers,params['name'],params)
        else:
            response = None
    elif action == 'editDuty':
        if params:
            if 'duty' in params['name']:
                response = editGroup(headers,params['name'],params)
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
                response = None
            else:
                response = None
        else:
            response = None
    elif action == 'saveTask':
        if params:
            response = None
        else:
            response = None
    elif action == 'editTask':
        if params:
            response = None
        else:
            response = None
    elif action == 'removeTask':
        if params:
            if 'name' in params:
                response = None
            else:
                response = None
        else:
            response = None
    elif action == 'getMission':
        if params:
            if 'name' in params:
                response = None
            else:
                response = None
        else:
            response = None
    elif action == 'saveMission':
        if params:
            response = None
        else:
            response = None
    elif action == 'editMission':
        if params:
            response = None
        else:
            response = None
    elif action == 'removeMission':
        if params:
            if 'name' in params:
                response = None
            else:
                response = None
        else:
            response = None

    if response:
        if response.code == 200:
            responseContent = response.content.json()
        if response.code == 403:
            pass
    requests.get(command_prefix + '/protocol/openid−connect/logout')
    return responseContent

#TODO:implement
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
            data = adminAction('getGroup',pattern)
        else:
            data = None
    elif what == 'ranks':
        if not pattern:
            data = adminAction('getGroup')
        else:
            data = adminAction('getGroup',pattern)
    elif what == 'division':
        if pattern:
            data = adminAction('getGroup',pattern)
        else:
            data = None
    elif what == 'divisions':
        if not pattern:
            data = adminAction('getGroup')
        else:
            data = adminAction('getGroup',pattern)
    elif what == 'duty':
        if pattern:
            data = adminAction('getGroup',pattern)
        else:
            data = None
    elif what == 'duties':
        if not pattern:
            data = adminAction('getGroup')
        else:
            data = adminAction('getGroup',pattern)
    elif what == 'task':
        if pattern:
            data = adminAction('getGroup',pattern)
        else:
            data = None
    elif what == 'tasks':
        if not pattern:
            data = adminAction('getGroup')
        else:
            data = adminAction('getGroup',pattern)
    elif what == 'mission':
        if pattern:
            data = adminAction('getGroup',pattern)
        else:
            data = None
    elif what == 'missions':
        if not pattern:
            data = adminAction('getGroup')
        else:
            data = adminAction('getGroup',pattern)
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
            data = adminAction('removeGroup',pattern)
        else:
            data = None
    elif what == 'ranks':
        if not pattern:
            data = adminAction('removeGroup')
        else:
            data = adminAction('removeGroup',pattern)
    elif what == 'division':
        if pattern:
            data = adminAction('removeGroup',pattern)
        else:
            data = None
    elif what == 'divisions':
        if not pattern:
            data = adminAction('removeGroup')
        else:
            data = adminAction('removeGroup',pattern)
    elif what == 'duty':
        if pattern:
            data = adminAction('removeGroup',pattern)
        else:
            data = None
    elif what == 'duties':
        if not pattern:
            data = adminAction('removeGroup')
        else:
            data = adminAction('removeGroup',pattern)
    elif what == 'task':
        if pattern:
            data = adminAction('removeGroup',pattern)
        else:
            data = None
    elif what == 'tasks':
        if not pattern:
            data = adminAction('removeGroup')
        else:
            data = adminAction('removeGroup',pattern)
    elif what == 'mission':
        if pattern:
            data = adminAction('removeGroup',pattern)
        else:
            data = None
    elif what == 'missions':
        if not pattern:
            data = adminAction('removeGroup')
        else:
            data = adminAction('removeGroup',pattern)
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
            data = adminAction('saveDuty')
        else:
            data = adminAction('saveDuty',pattern)
    elif what == 'task':
        if pattern:
            data = adminAction('saveTask',pattern)
        else:
            data = None
    elif what == 'tasks':
        if not pattern:
            data = adminAction('saveTask')
        else:
            data = adminAction('saveTask',pattern)
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
            data = adminAction('editGroup',pattern)
        else:
            data = None
    elif what == 'ranks':
        if not pattern:
            data = adminAction('editGroup')
        else:
            data = adminAction('editGroup',pattern)
    elif what == 'division':
        if pattern:
            data = adminAction('editGroup',pattern)
        else:
            data = None
    elif what == 'divisions':
        if not pattern:
            data = adminAction('editGroup')
        else:
            data = adminAction('editGroup',pattern)
    elif what == 'duty':
        if pattern:
            data = adminAction('editGroup',pattern)
        else:
            data = None
    elif what == 'duties':
        if not pattern:
            data = adminAction('editGroup')
        else:
            data = adminAction('editGroup',pattern)
    elif what == 'task':
        if pattern:
            data = adminAction('editGroup',pattern)
        else:
            data = None
    elif what == 'tasks':
        if not pattern:
            data = adminAction('editGroup')
        else:
            data = adminAction('editGroup',pattern)
    elif what == 'mission':
        if pattern:
            data = adminAction('editGroup',pattern)
        else:
            data = None
    elif what == 'missions':
        if not pattern:
            data = adminAction('editGroup')
        else:
            data = adminAction('editGroup',pattern)
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
