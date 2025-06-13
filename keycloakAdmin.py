import requests

from authorization import getAdminAccessToken

command_prefix = f'{current_app.config['KEYCLOAK_URL']}' + \
                 f'/admin/realms/' + \
                 f'{current_app.config['KEYCLOAK_REALM']}'

def adminAction(token,action,params=dict()):
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
    if response:
        if response.code == 200:
            return response.content.json()
        else:
            return None

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

#TODO: continua da qui
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
