#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from os     import getenv
from json   import loads

class BaseConfig:
    SESSION_TYPE                = "redis"
    WTF_CSRF_ENABLED            = True
    WTF_CSRF_CHECK_DEFAULT      = True
    WTF_CSRF_METHODS            = ['POST']
    WTF_CSRF_FIELD_NAME         = 'csrf_token'
    WTF_CSRF_HEADERS            = ['X-CSRFToken','X-CSRF-Token']
    WTF_CSRF_TIME_LIMIT         = 3600
    WTF_CSRF_SSL_STRICT         = True
    WTF_I18N_ENABLED            = True
    EDITING_TIME                = 300 #In seconds
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
    Identity                    = ['']
    Authentication              = ['']
    Authorization               = ['']
    People                      = ['']
    Crew                        = ['']
    Ranks                       = ['']
    Divisions                   = ['']
    Duties                      = ['']
    Tasks                       = ['']
    Missions                    = ['']
class Development(BaseConfig,DbConfig,KeycloakConfig,ShipConfig,Providers):
    DEBUG                       = True
    SECRET_KEY                  = getenv("SECRET_KEY_DEVELOPMENT")
    WTF_CSRF_SECRET_KEY         = SECRET_KEY
class Production(BaseConfig,DbConfig,KeycloakConfig,ShipConfig,Providers):
    DEBUG                       = False
    SECRET_KEY                  = getenv("SECRET_KEY_PRODUCTION")
    WTF_CSRF_SECRET_KEY         = SECRET_KEY

