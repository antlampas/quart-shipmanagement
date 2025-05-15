#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from quart          import Blueprint
from quart          import current_app
from quart          import render_template
from sqlalchemy     import select
from sqlalchemy.orm import Session

from model          import db
from model          import CrewMemberTable
from model          import MemberDutyLogEntryTable
from model          import MemberOnboardLogEntryTable
from model          import MemberRankLogEntryTable
from model          import MemberDivisionLogEntryTable
from model          import MemberTaskLogEntryTable
from model          import MemberMissionLogEntryTable

from authorization  import require_role
from authorization  import require_login

from permissions    import CrewOnBoardLogPermissions

from baseClasses    import Editable
from baseClasses    import Addable

from standardReturn import standardReturn

sectionName = "Crew Onboard Log"

crewOnboardLog_blueprint = Blueprint("crewOnboardLog",__name__,url_prefix='/crewOnboardLog',template_folder='templates/default')

class MemberOnboardLog:
    def __init__(self):
        self.CrewMember        = ""
        self.OnboardPeriods    = list()
        self.PreviousDivisions = list()
        self.PreviousDuties    = list()
        self.PreviousTasks     = list()
        self.PreviousMissions  = list()
    def read(self):
        log = list()

        with db.bind.Session() as s:
            with s.begin():
                crewMembers       = s.query(select(CrewMemberTable).distinct(CrewMemberTable.Nickname).subquery()).all()
                memberOnboardLog  = s.query(select(MemberOnboardLogEntryTable,CrewMemberTable).subquery()).all()
                memberDivisionLog = s.query(select(MemberDivisionLogEntryTable,CrewMemberTable).subquery()).all()
                memberDutyLog     = s.query(select(MemberDutyLogEntryTable,CrewMemberTable).subquery()).all()
                memberTaskLog     = s.query(select(MemberTaskLogEntryTable,CrewMemberTable).subquery()).all()
                memberMissionLog  = s.query(select(MemberMissionLogEntryTable,CrewMemberTable).subquery()).all()

                for i in (crewMembers,memberOnboardLog,memberDivisionLog,memberDutyLog,memberTaskLog,memberMissionLog):
                    if len(i) > 0:
                        log.append(i)

        return log

class OnboardLog:
    def __init__(self):
        self.logEntry = list()
    def read(self):
        log = list()

        with db.bind.Session() as s:
            with s.begin():
                crewMembers       = s.query(select(CrewMemberTable).distinct(CrewMemberTable.Nickname).where(CrewMemberTable.Nickname==member).subquery()).all()
                memberOnboardLog  = s.query(select(MemberOnboardLogEntryTable,CrewMemberTable).where(MemberOnboardLogEntryTable.CrewMember==member,MemberOnboardLogEntryTable.CrewMember==CrewMemberTable.Nickname).subquery()).all()
                memberDivisionLog = s.query(select(MemberDivisionLogEntryTable,CrewMemberTable).where(MemberDivisionLogEntryTable.CrewMember==member,MemberDivisionLogEntryTable.CrewMember==CrewMemberTable.Nickname).subquery()).all()
                memberDutyLog     = s.query(select(MemberDutyLogEntryTable,CrewMemberTable).where(MemberDutyLogEntryTable.CrewMember==member,MemberDutyLogEntryTable.CrewMember==CrewMemberTable.Nickname).subquery()).all()
                memberTaskLog     = s.query(select(MemberTaskLogEntryTable,CrewMemberTable).where(MemberTaskLogEntryTable.CrewMember==member,MemberTaskLogEntryTable.CrewMember==CrewMemberTable.Nickname).subquery()).all()
                memberMissionLog  = s.query(select(MemberMissionLogEntryTable,CrewMemberTable).where(MemberMissionLogEntryTable.CrewMember==member,MemberMissionLogEntryTable.CrewMember==CrewMemberTable.Nickname).subquery()).all()

                for i in (crewMembers,memberOnboardLog,memberDivisionLog,memberDutyLog,memberTaskLog,memberMissionLog):
                    if len(i) > 0:
                        log.append(i)

        return log

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
