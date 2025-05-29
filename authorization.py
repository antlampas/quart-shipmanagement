#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import requests

from datetime import datetime
from jose     import jwt

from quart    import current_app
from quart    import request
from quart    import session
from quart    import abort
from quart    import redirect
from quart    import url_for

from standardReturn import standardReturn

def isTokenExpired():
    if 'auth_token' in session:
        if session['access_token']['exp'] < datetime.now().timestamp():
            return True
        else:
            return False
    else:
        return False

def refreshToken(func):
    async def wrapper(*args, **kwargs):
        if 'auth_token' in session:
            if isTokenExpired():
                url = f'{current_app.config["KEYCLOAK_URL"]}/auth/realms/{current_app.config["KEYCLOAK_REALM"]}/protocol/openid-connect/token'
                h = {
                    'Authorization' : session['auth_token']['access_token'],
                    'Body type'     : 'x-www-form-urlencoded'
                    }
                d = {
                    'client_id'     : current_app.config['OPENID_KEYCLOAK_CONFIG']['client_id'],
                    'client_secret' : current_app.config['OPENID_KEYCLOAK_CONFIG']['client_secret'],
                    'refresh_token' : session['auth_token']['refresh_token'],
                    'grant_type'    : 'refresh_token'
                    }

                token = requests.post(url,headers=h,data=d)
                token = requests.post(url,data=d)

                if token.status_code == 200:
                    print('OK')
                    print(token)
                    session['access_token'] = token.json()['access_token']
                    return await func(*args, **kwargs)
                elif token.status_code == 404:
                    return await standardReturn("error.html",sectionName="Error",ERROR="Identity provider not found")
                elif token.status_code == 400:
                    print('Bad Request')
                    print(token.request.body)
                    return redirect(request.scheme+"://"+request.host+'/relogin?redirect_url='+request.path)
            else:
                return await func(*args, **kwargs)
        else:
            return await func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def require_login(func):
    async def wrapper(*args, **kwargs):
        if 'auth_token' in session:
            return await func(*args, **kwargs)
        else:
            return await standardReturn("error.html",sectionName="Error",ERROR="Unauthenticated")
    wrapper.__name__ = func.__name__
    return wrapper

def require_role(*requiredRoles):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if 'auth_token' in session:
                userRoles             = session['access_token']['groups']
                numberOfRequiredRoles = len(requiredRoles)
                rolesMatched          = 0
                for requiredRole in requiredRoles:
                    for userRole in userRoles:
                        if requiredRole in userRole:
                            rolesMatched += 1
                if rolesMatched == numberOfRequiredRoles:
                    return await func(*args, **kwargs)
                else:
                    return await standardReturn("error.html",sectionName="Error",ERROR="Unauthorized")
            else:
                return await standardReturn("error.html",sectionName="Error",ERROR="Unauthenticated")
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

def require_user(users=[],groups=[]):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if 'auth_token' in session:
                user       = session['access_token']['username']
                userGroups = session['access_token']['groups']
                isUserInUsers = (user in users)
                isUserInGroup = False
                for userGroup in userGroups:
                    for group in groups:
                        if group in userGroup:
                            isUserInGroup = True
                if isUserInUsers or isUserInGroup:
                    return await func(*args, **kwargs)
                else:
                    return await standardReturn("error.html",sectionName="Error",ERROR="Unauthorized")
            else:
                return await standardReturn("error.html",sectionName="Error",ERROR="Unauthenticated")
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

def authorize_action(action):
    def decorator(func):
        async def wrapper(*args,**kwargs):
            if 'auth_token' in session:
                #TODO: implement jwt encoding for the request
                #TODO: implement jwt send
                #TODO: implement response wait and decode
                pass
            else:
                return await standardReturn("error.html",sectionName="Error",ERROR="Unauthenticated")
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
