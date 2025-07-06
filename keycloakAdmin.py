#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-31

import requests
import json

from uuid import uuid4

from config import KeycloakConfig

adminToken   = ''
command_prefix = KeycloakConfig.KEYCLOAK_ADMIN['url']

def getAdminToken():
    global adminToken
    headers = {
                'content-type' : 'application/x-www-form-urlencoded'
              }
    data = {
             'client_id'  : KeycloakConfig.KEYCLOAK_ADMIN['client_id'],
             'grant_type' : KeycloakConfig.KEYCLOAK_ADMIN['grant_type'],
             'username'   : KeycloakConfig.KEYCLOAK_ADMIN['username'],
             'password'   : KeycloakConfig.KEYCLOAK_ADMIN['password']
           }
    response = requests.post(f'{KeycloakConfig.KEYCLOAK_URL}' + \
                             f'/realms/' + \
                             f'{KeycloakConfig.KEYCLOAK_REALM}' + \
                             '/protocol/openid-connect/token',
                             headers=headers,
                             data=data
                            )
    adminToken = response.json()
    return response.json()
def getAdminAccessToken():
    global adminToken
    return adminToken['access_token']
def getAdminRefreshToken():
    global adminToken
    return adminToken['refresh_token']
def removeAdminToken():
    global adminToken
    adminToken = ''
    return True
def adminLogout():
    accessToken  = getAdminAccessToken()
    refreshToken = getAdminRefreshToken()
    logoutInfo = {
        'client_id'     : KeycloakConfig.KEYCLOAK_ADMIN['client_id'],
        'refresh_token' : refreshToken,
        }
    requests.post(f'{KeycloakConfig.KEYCLOAK_URL}' + \
                           f'/realms/' + \
                           f'{KeycloakConfig.KEYCLOAK_REALM}' + \
                           '/protocol/openid-connect/logout',
                           headers={
                                    'Content-Type' : \
                                    'application/x-www-form-urlencoded',
                                    'Authorization' : 'Bearer ' + accessToken
                                   },
                           data=logoutInfo
                          )
    removeAdminToken()
def adminAction(action,params=dict()):
    getAdminToken()
    accessToken  = getAdminAccessToken()
    response     = None
    headers      = {
                    'Content-Type'  : 'application/json',
                    'Authorization' : 'Bearer ' + accessToken
                   }
    if action == 'getUser':
        if params:
            if 'nickname' in params:
                response = getUser(headers,params)
            else:
                response = {'Error' : 'No nickname provided'}
        else:
            response = getUser(headers)
    elif action == 'addUser':
        if params:
            if 'nickname' in params:
                response = addUser(headers,params)
            else:
                response = {'Error' : 'No nickname provided'}
        else:
            response = {'Error' : 'No user attributes provided'}
    elif action == 'editUser':
        if params:
            if 'nickname' in params:
                response = editUser(headers,params)
            else:
                response = {'Error' : 'No nickname provided'}
        else:
            response = {'Error' : 'No user attributes provided'}
    elif action == 'removeUser':
        if params:
            if 'nickname' in params:
                response = removeUser(headers,params['nickname'])
            else:
                response = {'Error' : 'No nickname provided'}
        else:
            response = {'Error' : 'No parameters provided'}
    elif action == 'getRank':
        if params:
            params['parent'] = 'ranks'
            if 'name' in params:
                if 'ranks' in params['name']:
                    response = getGroup(headers,params['name'])
                else:
                    response = {'Error' : 'No rank name provided'}
            else:
                response = {'Error' : 'No rank attributes provided'}
        else:
            response = None
    elif action == 'getRanks':
        params['parent'] = 'ranks'
        response = getGroup(headers,params)
    elif action == 'addRank':
        if params:
            params['parent'] = 'ranks'
            if 'name' in params:
                response = addGroup(headers,params)
            else:
                response = {'Error' : 'No rank name provided'}
        else:
            response = {'Error' : 'No rank attributes provided'}
    elif action == 'editRank':
        if params:
            params['parent'] = 'ranks'
            if 'name' in params:
                response = addGroup(headers,params)
            else:
                response = {'Error' : 'No rank name provided'}
        else:
            response = {'Error' : 'No rank attributes provided'}
    elif action == 'removeRank':
        if params:
            params['parent'] = 'ranks'
            if 'name' in params:
                response = addGroup(headers,params)
            else:
                response = {'Error' : 'No rank name provided'}
        else:
            response = {'Error' : 'No rank attributes provided'}
    elif action == 'getDivision':
        if params:
            params['parent'] = 'divisions'
            if 'name' in params:
                response = getGroup(headers,params)
            else:
                response = {'Error' : 'No division name provided'}
        else:
            response = {'Error' : 'No division attributes provided'}
    elif action == 'getDivisions':
        params['parent'] = 'divisions'
        response = getGroup(headers,params)
    elif action == 'addDivision':
        if params:
            params['parent'] = 'divisions'
            if 'name' in params:
                response = addGroup(headers,params)
            else:
                response = {'Error' : 'No division name provided'}
        else:
            response = {'Error' : 'No division attributes provided'}
    elif action == 'editDivision':
        if params:
            params['parent'] = 'divisions'
            if 'name' in params:
                response = editGroup(headers,params['name'])
            else:
                response = {'Error' : 'No division name provided'}
        else:
            response = {'Error' : 'No division attributes provided'}
    elif action == 'removeDivision':
        if params:
            params['parent'] = 'divisions'
            if 'name' in params:
                response = removeGroup(headers,params['name'])
            else:
                response = {'Error' : 'No division name provided'}
        else:
            response = {'Error' : 'No division attributes provided'}
    elif action == 'getDuty':
        if params:
            params['parent'] = 'duties'
            if 'name' in params:
                response = getGroup(headers,params['name'])
            else:
                response = {'Error' : 'No duty name provided'}
        else:
            response = {'Error' : 'No duty attributes provided'}
    elif action == 'getDuties':
        params['parent'] = 'duties'
        response = getGroup(headers,params)
    elif action == 'addDuty':
        if params:
            if 'name' in params:
                params['parent'] = 'duties'
                response = addGroup(headers,params)
            else:
                response = {'Error' : 'No duty name provided'}
        else:
            response = {'Error' : 'No duty attributes provided'}
    elif action == 'editDuty':
        if params:
            params['parent'] = 'duties'
            if 'name' in params:
                response = editGroup(headers,params['name'])
            else:
                response = {'Error' : 'No duty name provided'}
        else:
            response = {'Error' : 'No duty attributes provided'}
    elif action == 'removeDuty':
        if params:
            params['parent'] = 'duties'
            if 'name' in params:
                response = removeGroup(headers,params['name'])
            else:
                response = {'Error' : 'No duty name provided'}
        else:
            response = {'Error' : 'No duty attributes provided'}
    elif action == 'getTask':
        if params:
            params['parent'] = 'tasks'
            if 'name' in params:
                response = {"Warning" : "Implement"}
            else:
                response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'addTask':
        if params:
            params['parent'] = 'tasks'
            response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'editTask':
        if params:
            params['parent'] = 'tasks'
            response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'removeTask':
        if params:
            params['parent'] = 'tasks'
            if 'name' in params:
                response = {"Warning" : "Implement"}
            else:
                response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'getMission':
        if params:
            params['parent'] = 'missions'
            if 'name' in params:
                response = {"Warning" : "Implement"}
            else:
                response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'addMission':
        if params:
            params['parent'] = 'missions'
            response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'editMission':
        if params:
            params['parent'] = 'missions'
            response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    elif action == 'removeMission':
        if params:
            params['parent'] = 'missions'
            if 'name' in params:
                response = {"Warning" : "Implement"}
            else:
                response = {"Warning" : "Implement"}
        else:
            response = {"Warning" : "Implement"}
    else:
        return {'Error' : 'Invalid request'}

    adminLogout()
    if not isinstance(response,dict):
        if response.status_code == 200 or \
           response.status_code == 201 or \
           response.status_code == 204:
            if response.text:
                responseContent = response.json()
            else:
                responseContent = {'Info' : 'OK'}
        elif response.status_code == 403:
            return {"Error": "Forbidden"}
        elif response.status_code == 400:
            return {"Error": "Bad Request"}
        elif response.status_code == 401:
            return {"Error": "Unauthorized"}
        elif response.status_code == 409:
            return {"Error": "Conflict"}
        elif response.status_code == 500:
            return {"Error": "Internal Server Error"}
        else:
            return {"Error": "Error code: " + str(response.status_code)}
    elif isinstance(response,dict):
        responseContent = response
    return responseContent

def loadFromKeycloak(what='',pattern=dict()):
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
            data = adminAction('getDivisions',dict())
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

def getUser(headers,user=dict()):
    global command_prefix
    response = None
    if user:
        if 'nickname' in user:
            username   = user['nickname']
            userLoaded = requests.get(f'{command_prefix}/users',
                                    headers=headers,
                                    params={'username' : username}
                                   )
            userTemp = userLoaded.json()[0]
            userId = userTemp['id']
            groupsLoaded = requests.get(f'{command_prefix}' + \
                                        '/users/' + \
                                        f'{userId}' + \
                                        '/groups',
                                        headers=headers
                                       )
            
            userTemp = [userTemp | {'groups': groupsLoaded.json()}]
            userTemp[0]['attributes']['Serial'] = \
                                          userTemp[0]['attributes']['Serial'][0]
            userTemp[0]['attributes']['STIC']   = \
                                            userTemp[0]['attributes']['STIC'][0]
            userLoaded._content   = json.dumps(userTemp).encode('utf-8')
            response = userLoaded
        else:
            response = {'Error' : 'No nickname provided'}
    else:
        response = requests.get(f'{command_prefix}/users',headers=headers)
    return response
def removeUser(headers,user=dict()):
    global command_prefix
    response = None
    if user:
        if 'nickname' in user:
            username = user['nickname']
            response = requests.delete(f'{command_prefix}/users/{username}',
                                       headers=headers
                                      )
    else:
        response = None
    return response
def addUser(headers,user=dict()):
    global command_prefix
    response = None
    if user:
        user['username'] = user['nickname']
        user['attributes'] = {
                              'Serial' : [user['serial']],
                              'STIC'   : [user['stic']]
                             }
        user['groups']     = [
                              '/ranks/'+user['rank'],
                              '/divisions/'+user['division']
                             ] + ['/duties/'+d for d in user['duties']]
        data = {
                'username'   : user['username'],
                'firstName'  : user['firstName'],
                'lastName'   : user['lastName'],
                'serial'     : user['attributes']['Serial'],
                'stic'       : user['attributes']['STIC'],
                'groups'     : user['groups'],
                'enabled'    : True
               }
        response = requests.post(f'{command_prefix}/users',
                                headers=headers,
                                data=json.dumps(data)
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

def getGroup(headers,pattern=dict()):
    global command_prefix
    response = requests.get(command_prefix + '/groups',headers=headers,params={'search' : pattern['parent']})
    del pattern['parent']
    id = response.json()[0]['id']
    response = requests.get(command_prefix + f'/groups/{id}/children',headers=headers)
    if 'name' in pattern:
        groupFound = False
        for group in response.json():
            if group['name'] == pattern['name']:
                response._content = json.dumps(group).encode('utf-8')
                groupFound = True
                break
        if not groupFound:
            response = {'Error' : 'Group not found'}
    return response
def removeGroup(headers,group=''):
    global command_prefix
    response = None
    if group:
        name = group['name'][group['name'].rfind('/')+1:]
        response = requests.delete(command_prefix + f'/groups/{name}',
                                   headers=headers
                                  )
    else:
        response = None
    return response
def addGroup(headers,group=dict()):
    global command_prefix
    if group:
        parentId = ''
        response = requests.get(f'{command_prefix}/groups',
                            params={'search' : group['parent']},
                            headers=headers
                           )
        del group['parent']
        parentId = str(response.json()[0]['id'])
        groupName = group['name']
        group['attributes'] = {'description' : [group['description']]}
        del group['description']
        headers = headers
        response = requests.post(f'{command_prefix}/groups/{parentId}/children',
                                 headers=headers,
                                 data=json.dumps(group)
                                )
    else:
        response = None
    return response
def editGroup(headers,group='',attributes=dict()):
    global command_prefix
    response = None
    if group and attributes:
        name = group['name'][group['name'].rfind('/')+1:]
        response = requests.put(command_prefix + f'/groups/{name}',
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
