#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from quart import current_app
from quart import session
from quart import abort

from jose import jwt

from standardReturn import standardReturn

def require_role(*requiredRoles):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if 'auth_token' in session:
                token                 = jwt.get_unverified_claims(session['auth_token']['access_token'])
                userRoles             = token['groups']
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
                token      = jwt.get_unverified_claims(session['auth_token']['access_token'])
                user       = token['username']
                userGroups = token['groups']
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

def require_login(func):
    async def wrapper(*args, **kwargs):
        if 'auth_token' in session:
            return await func(*args, **kwargs)
        else:
            return await standardReturn("error.html",sectionName="Error",ERROR="Unauthenticated")
    wrapper.__name__ = func.__name__
    return wrapper

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
