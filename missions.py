#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from quart import Blueprint
from quart import current_app
from quart import render_template
from quart import request

from authorization  import require_role
from authorization  import require_login

from permissions    import MissionsPermissions

from missionsClasses import Mission
from missionsClasses import Missions

from standardReturn import standardReturn

missions_blueprint = Blueprint("missions",__name__,url_prefix='/missions',template_folder='templates/default')

sectionName = "Missions"

@missions_blueprint.route("/",methods=["GET"])
@refreshToken
async def missions():
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@missions_blueprint.route("/mission/<mission>",methods=["GET"])
@refreshToken
@require_login
async def view(mission):
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@missions_blueprint.route("/add",methods=["GET","POST"])
@refreshToken
@require_role(MissionsPermissions.addMissionRole)
async def add():
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@missions_blueprint.route("/remove",methods=["GET","POST"])
@refreshToken
@require_role(MissionsPermissions.removeMissionRole)
async def remove():
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@missions_blueprint.route("/edit",methods=["GET","POST"])
@refreshToken
@require_role(MissionsPermissions.editMissionRole)
async def edit():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
