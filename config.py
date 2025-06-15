#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from os import getenv

class BaseConfig:
    DATABASEURL                 = getenv("SQLALCHEMY_DATABASE_URI")
    SESSION_TYPE                = "redis"
class KeycloakConfig:
    KEYCLOAK_URL                = getenv("KEYCLOAK_URL")
    KEYCLOAK_REALM              = getenv("KEYCLOAK_REALM")
    OPENID_KEYCLOAK_CONFIG      = getenv("OPENID_KEYCLOAK_CONFIG")
    KEYCLOAK_ADMIN              = getenv("KEYCLOAK_ADMIN")
class Providers:
    Identity       = {}
    Authentication = {}
    Authorization  = {}
    Crew           = {}
    Ranks          = {}
    Divisions      = {}
    Duties         = {}
    Tasks          = {}
    Missions       = {}
class ShipConfig:
    SHIPNAME       = 'Picenum'
    REGISTRYNUMBER = '2025'
class Development(BaseConfig,KeycloakConfig,ShipConfig,Providers):
    DEBUG                       = True
    SECRET_KEY                  = getenv("SECRET_KEY_DEVELOPMENT")
class Production(BaseConfig,KeycloakConfig,ShipConfig,Providers):
    DEBUG                       = False
    SECRET_KEY                  = getenv("SECRET_KEY_PRODUCTION")
