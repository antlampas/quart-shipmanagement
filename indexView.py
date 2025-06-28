#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from quart import Blueprint
from quart import current_app
from quart import request
from quart import session

from authorization  import refreshToken
from standardReturn import standardReturn

index_blueprint = Blueprint("index",
                            __name__,
                            template_folder='templates/default'
                           )

sectionName = "Home Page"

from jose import jwt


@index_blueprint.route("/")
async def index():
    ## Da rimuovere prima dei commit ##
    if 'auth_token' in session:
        from datetime      import datetime
        idToken       = jwt.get_unverified_claims(session['auth_token']['id_token'])
        accessToken   = jwt.get_unverified_claims(session['auth_token']['access_token'])
        refreshToken  = jwt.get_unverified_claims(session['auth_token']['refresh_token'])
        tokenReleased = datetime.fromtimestamp(accessToken['iat'])
        tokenExpires  = datetime.fromtimestamp(accessToken['exp'])
        print(request.path)
        return await standardReturn("index.html",sectionName,AUTHTOKEN=session['auth_token'],IDTOKEN=idToken,ACCESSTOKEN=accessToken,REFRESHTOKEN=refreshToken,RELEASED=tokenReleased,EXPIRES=tokenExpires)
    ## End ##
    return await standardReturn("index.html",sectionName)
