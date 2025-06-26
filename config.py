#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from os     import getenv
from json   import loads

class BaseConfig:
    SESSION_TYPE                = "redis"
class ShipConfig:
    SHIPNAME                    = ''
    REGISTRYNUMBER              = ''
class DbConfig:
    DATABASEURL                 = getenv("SQLALCHEMY_DATABASE_URI")
class KeycloakConfig:
    KEYCLOAK_URL                = getenv("KEYCLOAK_URL")
    KEYCLOAK_REALM              = getenv("KEYCLOAK_REALM")
    OPENID_KEYCLOAK_CONFIG      = loads(getenv("OPENID_KEYCLOAK_CONFIG"))
    KEYCLOAK_ADMIN              = loads(getenv("KEYCLOAK_ADMIN"))
class Providers:
    Identity       = ['']
    Authentication = ['']
    Authorization  = ['']
    People         = ['']
    Crew           = ['']
    Ranks          = ['']
    Divisions      = ['']
    Duties         = ['']
    Tasks          = ['']
    Missions       = ['']
class Development(BaseConfig,DbConfig,KeycloakConfig,ShipConfig,Providers):
    DEBUG                       = True
    SECRET_KEY                  = getenv("SECRET_KEY_DEVELOPMENT")
class Production(BaseConfig,DbConfig,KeycloakConfig,ShipConfig,Providers):
    DEBUG                       = False
    SECRET_KEY                  = getenv("SECRET_KEY_PRODUCTION")
