#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from threading      import Timer

from quart import Blueprint
from quart import current_app
from quart import render_template
from quart import request

from authorization  import require_role
from authorization  import require_login
from authorization  import refreshToken

from permissions    import MissionsPermissions

from missionsClasses import Mission
from missionsClasses import Missions

from standardReturn import standardReturn

missions_blueprint = Blueprint("missions",__name__,url_prefix='/missions',template_folder='templates/default')

sectionName = "Missions"

@refreshToken
@missions_blueprint.route("/",methods=["GET"])
async def missions():
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@refreshToken
@require_role(MissionsPermissions.View)
@missions_blueprint.route("/mission/<mission>",methods=["GET"])
async def view(mission):
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@refreshToken
@require_role(MissionsPermissions.Add)
@missions_blueprint.route("/add",methods=["GET","POST"])
async def add():
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@refreshToken
@require_role(MissionsPermissions.Remove)
@missions_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@refreshToken
@require_role(MissionsPermissions.Edit)
@missions_blueprint.route("/edit",methods=["GET","POST"])
async def edit():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
