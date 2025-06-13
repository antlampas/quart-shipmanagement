#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

class BaseConfig:
    DATABASEURL                 = ''
    SESSION_TYPE                = ''

class KeycloakConfig:
    KEYCLOAK_URL                = ''
    KEYCLOAK_REALM              = ''
    OPENID_KEYCLOAK_CONFIG      = {
                                    'client_id':     '',
                                    'client_secret': '',
                                    'configuration': f'',
                                    'check_nonce':   False
                                  }
    KEYCLOAK_ADMIN              = {
                                    'url'        : f'{KEYCLOAK_URL}/realms/' + \
                                                   f'{KEYCLOAK_REALM}' + \
                                                   '/protocol/' + \
                                                   'openid-connect/token',
                                    'client_id'  : '',
                                    'grant_type' : '',
                                    'username'   : '',
                                    'password'   : ''
                                  }
class IdentityProvider:
    SOURCE = ''

class ShipConfig:
    SHIPNAME       = ''
    REGISTRYNUMBER = ''

class Development(BaseConfig,KeycloakConfig,ShipConfig,IdentityProvider):
    DEBUG                       = True
    SECRET_KEY                  = ''

class Production(BaseConfig,KeycloakConfig,ShipConfig,IdentityProvider):
    DEBUG                       = False
    SECRET_KEY                  = ''
