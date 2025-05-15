class BaseConfig:
    DATABASEURL                 = ""
    SESSION_TYPE                = ""
    OPENID_KEYCLOAK_CONFIG      = {
                                    "client_id":     "",
                                    "client_secret": "",
                                    "configuration": "",
                                    "check_nonce":   False
                                }

class ShipConfig:
    SHIPNAME       = ""
    REGISTRYNUMBER = ""

class Development(BaseConfig,ShipConfig):
    DEBUG                       = True
    SECRET_KEY                  = ''

class Production(BaseConfig,ShipConfig):
    DEBUG                       = False
    SECRET_KEY                  = ''
