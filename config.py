#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from os     import getenv
from json   import loads

class BaseConfig:
    SESSION_TYPE                = getenv('SESSION_TYPE')
    WTF_CSRF_ENABLED            = getenv('WTF_CSRF_ENABLED')
    WTF_CSRF_CHECK_DEFAULT      = getenv('WTF_CSRF_CHECK_DEFAULT')
    WTF_CSRF_METHODS            = getenv('WTF_CSRF_METHODS')
    WTF_CSRF_FIELD_NAME         = getenv('WTF_CSRF_FIELD_NAME')
    WTF_CSRF_HEADERS            = getenv('WTF_CSRF_HEADERS')
    WTF_CSRF_TIME_LIMIT         = getenv('WTF_CSRF_TIME_LIMIT')
    WTF_CSRF_SSL_STRICT         = getenv('WTF_CSRF_SSL_STRICT')
    WTF_I18N_ENABLED            = getenv('WTF_I18N_ENABLED')
    EDITING_TIME                = getenv('EDITING_TIME')
class ShipConfig:
    SHIPNAME                    = getenv('SHIPNAME')
    REGISTRYNUMBER              = getenv('REGISTRYNUMBER')
class DbConfig:
    DATABASEURL                 = getenv("SQLALCHEMY_DATABASE_URI")
class KeycloakConfig:
    KEYCLOAK_URL                = getenv("KEYCLOAK_URL")
    KEYCLOAK_REALM              = getenv("KEYCLOAK_REALM")
    OPENID_KEYCLOAK_CONFIG      = loads(getenv("OPENID_KEYCLOAK_CONFIG"))
    KEYCLOAK_ADMIN              = loads(getenv("KEYCLOAK_ADMIN"))
class Providers:
    Identity                    = getenv('IDENTITY_PROVIDER')
    Authentication              = getenv('AUTHENTICATION_PROVIDER')
    Authorization               = getenv('AUTHORIZATION_PROVIDER')
    People                      = getenv('PEOPLE_PROVIDER')
    Crew                        = getenv('CREW_PROVIDER')
    Ranks                       = getenv('RANKS_PROVIDER')
    Divisions                   = getenv('DIVISIONS_PROVIDER')
    Duties                      = getenv('DUTIES_PROVIDER')
    Tasks                       = getenv('TASKS_PROVIDER')
    Missions                    = getenv('MISSIONS_PROVIDER')
class Development(BaseConfig,DbConfig,KeycloakConfig,ShipConfig,Providers):
    DEBUG                       = True
    SECRET_KEY                  = getenv('SECRET_KEY_DEVELOPMENT')
    WTF_CSRF_SECRET_KEY         = getenv('WTF_CSRF_SECRET_KEY')
class Production(BaseConfig,DbConfig,KeycloakConfig,ShipConfig,Providers):
    DEBUG                       = False
    SECRET_KEY                  = getenv("SECRET_KEY_PRODUCTION")
    WTF_CSRF_SECRET_KEY         = getenv('WTF_CSRF_SECRET_KEY')

