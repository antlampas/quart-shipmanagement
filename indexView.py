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
    return await standardReturn("index.html",sectionName)
