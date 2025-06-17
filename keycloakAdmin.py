#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-31

import requests

command_prefix = f'{current_app.config['KEYCLOAK_URL']}' + \
                 f'/admin/realms/' + \
                 f'{current_app.config['KEYCLOAK_REALM']}'

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
    token = getAdminToken()
    response = None
    headers  = {'authorization' : token}
    if action == 'getUser':
        if 'username' in params:
            response = getUser(headers,params['username'])
        else:
            response = getUser()
    elif action == 'addUser':
        if 'username'  in params and \
           'firstName' in params and \
           'lastName'  in params:
            response = addUser(headers,params)
    responseContent = None
    if response:
        if response.code == 200:
            responseContent = response.content.json()
    requests.get(command_prefix + '/protocol/openid−connect/logout')
    return responseContent

#TODO:implement
def loadFromKeycloak(what='',pattern=''):
    if what == 'person':
        pass
    elif what == 'people':
        pass
    elif what == 'crewMember':
        pass
    elif what == 'crew':
        pass
    elif what == 'rank':
        pass
    elif what == 'ranks':
        pass
    elif what == 'division':
        pass
    elif what == 'divisions':
        pass
    elif what == 'duty':
        pass
    elif what == 'duties':
        pass
    elif what == 'task':
        pass
    elif what == 'tasks':
        pass
    elif what == 'mission':
        pass
    elif what == 'missions':
        pass
def removeFromKeycloak(what='',pattern=''):
    if what == 'person':
        pass
    elif what == 'people':
        pass
    elif what == 'crewMember':
        pass
    elif what == 'crew':
        pass
    elif what == 'rank':
        pass
    elif what == 'ranks':
        pass
    elif what == 'division':
        pass
    elif what == 'divisions':
        pass
    elif what == 'duty':
        pass
    elif what == 'duties':
        pass
    elif what == 'task':
        pass
    elif what == 'tasks':
        pass
    elif what == 'mission':
        pass
    elif what == 'missions':
        pass
def saveToKeycloak(what='',data=dict()):
    if what == 'person':
        pass
    elif what == 'people':
        pass
    elif what == 'crewMember':
        pass
    elif what == 'crew':
        pass
    elif what == 'rank':
        pass
    elif what == 'ranks':
        pass
    elif what == 'division':
        pass
    elif what == 'divisions':
        pass
    elif what == 'duty':
        pass
    elif what == 'duties':
        pass
    elif what == 'task':
        pass
    elif what == 'tasks':
        pass
    elif what == 'mission':
        pass
    elif what == 'missions':
        pass
def editKeycloak(what='',pattern=dict()):
    if what == 'person':
        pass
    elif what == 'people':
        pass
    elif what == 'crewMember':
        pass
    elif what == 'crew':
        pass
    elif what == 'rank':
        pass
    elif what == 'ranks':
        pass
    elif what == 'division':
        pass
    elif what == 'divisions':
        pass
    elif what == 'duty':
        pass
    elif what == 'duties':
        pass
    elif what == 'task':
        pass
    elif what == 'tasks':
        pass
    elif what == 'mission':
        pass
    elif what == 'missions':
        pass


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
