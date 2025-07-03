#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from quart          import Blueprint
from quart          import current_app
from sqlalchemy     import select
from sqlalchemy.orm import Session

from authorization  import require_role
from authorization  import require_login

from permissions    import CrewOnBoardLogPermissions

from standardReturn import standardReturn

sectionName = "Crew Onboard Log"

crewOnboardLog_blueprint = Blueprint("crewOnboardLog",__name__,url_prefix='/crewOnboardLog',template_folder='templates/default')

@crewOnboardLog_blueprint.route("/",methods=["GET"])
@require_login
async def readLog():
    onboardLog = MemberOnboardLog()
    return standardReturn("crewOnboardLog.html",sectionName,log=onboardLog.read())

@crewOnboardLog_blueprint.route("/<member>",methods=["GET"])
@require_login
async def readMemberLog(member):
    onboardLog = OnboardLog()
    return standardReturn("crewOnboardLog.html",sectionName,log=onboardLog.read())
