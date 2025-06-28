#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import requests

from jose           import jwt

from functools      import wraps
from datetime       import datetime
from jose           import jwt

from quart          import current_app
from quart          import request
from quart          import session
from quart          import abort
from quart          import redirect
from quart          import url_for

from standardReturn import standardReturn

def isTokenExpired():
    if 'auth_token' in session:
        if 'access_token' in session and (session['access_token']['exp'] < datetime.now().timestamp()):
            return True
        else:
            return False
    else:
        return False

def refreshToken(identityProvider="keycloak"):
    cId = current_app.config['OPENID_KEYCLOAK_CONFIG']['client_id']
    cs = current_app.config['OPENID_KEYCLOAK_CONFIG']['client_secret']
    if 'auth_token' in session:
        accessToken = session['auth_token']['access_token']
        refreshToken = session['auth_token']['refresh_token']
        if isTokenExpired():
            if identityProvider == 'keycloak':
                url = f'{current_app.config["KEYCLOAK_URL"]}' + \
                '/realms/' + \
                f'{current_app.config["KEYCLOAK_REALM"]}' + \
                '/protocol/openid-connect/token'
                h = {
                        'Authorization' : accessToken,
                        'Body type'     : 'x-www-form-urlencoded'
                    }
                d = {
                        'client_id'     : cId,
                        'client_secret' : cs,
                        'refresh_token' : refreshToken,
                        'grant_type'    : 'refresh_token'
                    }

                token = requests.post(url,headers=h,data=d)
                token = requests.post(url,data=d)

                if token.status_code == 200:
                    tokenJson = token.json()
                    session['access_token'] = jwt.get_unverified_claims(tokenJson['access_token'])
                    return True
                else:
                    return False

def require_login(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if 'auth_token' in session:
            return await func(*args, **kwargs)
        else:
            return await standardReturn("error.html",
                                  sectionName="Error",
                                  ERROR="Unauthenticated"
                                 )
    return wrapper

def require_role(*requiredRoles):
    def decorator(func):
        @wraps(func)
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
                    return await standardReturn("error.html",
                                          sectionName="Error",
                                          ERROR="Unauthorized"
                                         )
            else:
                return await standardReturn("error.html",
                                      sectionName="Error",
                                      ERROR="Unauthenticated"
                                     )
        return wrapper
    return decorator

def require_user(users=[],groups=[]):
    def decorator(func):
        @wraps(func)
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
                    return await standardReturn("error.html",
                                          sectionName="Error",
                                          ERROR="Unauthorized"
                                         )
            else:
                return await standardReturn("error.html",
                                      sectionName="Error",
                                      ERROR="Unauthenticated"
                                     )
        return wrapper
    return decorator

def authorize_action(action):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args,**kwargs):
            if 'auth_token' in session:
                #TODO: implement jwt encoding for the request
                #TODO: implement jwt send
                #TODO: implement response wait and decode
                pass
            else:
                return await standardReturn("error.html",
                                      sectionName="Error",
                                      ERROR="Unauthenticated"
                                     )
        return wrapper
    return decorator
