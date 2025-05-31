import requests

from authorization import getAdminAccessToken

def adminAction(token,action,params=dict()):
    response = None
    headers  = {'authorization' : token}
    if action == 'getUser':
        if 'username' in params:
            response = getUser(headers,params['username'])
        else:
            response = getUser()
    elif action == 'addUser':
        if 'username' in params and 'firstName' in params and 'lastName' in params:
            response = addUser(headers,params)
    return response

def getUser(headers,user=''):
    response = None
    if user:
        response = requests.get(f'{current_app.config['KEYCLOAK_URL']}/admin/realms/{current_app.config['KEYCLOAK_REALM']}/users',headers=headers,params={'username' : user})
    else:
        response = requests.get(f'{current_app.config['KEYCLOAK_URL']}/admin/realms/{current_app.config['KEYCLOAK_REALM']}/users',headers=headers)
    if response:
        if response.code == 200:
            return response.content.json()
        else:
            return None

def addUser(headers,user=dict()):
    response = None
    if user:
        response = requests.get(f'{current_app.config['KEYCLOAK_URL']}/admin/realms/{current_app.config['KEYCLOAK_REALM']}/users',headers=headers,data=user)
    else:
        response = None
    return response

def editUser(headers,user,attributes):
    pass

def removeUser(headers,user):
    pass

def getGroup(headers,group=''):
    pass

def addGroup(headers,group=''):
    pass

def editGroup(headers,group=''):
    pass

def removeGroup(headers,group=''):
    pass
