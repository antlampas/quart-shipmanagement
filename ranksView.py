#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from threading      import Timer

from quart          import Blueprint
from quart          import current_app
from quart          import request
from quart          import render_template

from sqlalchemy     import select
from sqlalchemy.orm import Session

from model          import db
from model          import CrewMemberTable
from model          import RankTable

from forms          import AddRankForm
from forms          import RemoveRankForm
from forms          import EditRankForm

from authorization  import require_role
from authorization  import require_login
from authorization  import refreshToken

from permissions    import RanksPermissions

from ranksClasses   import Rank
from ranksClasses   import Ranks

from standardReturn import standardReturn

ranks_blueprint = Blueprint("ranks",__name__,url_prefix='/ranks',template_folder='templates/default')

sectionName = "Ranks"


@require_role(RanksPermissions.View)
@ranks_blueprint.route("/",methods=["GET"])
async def ranks():
    return await standardReturn("implement.html",sectionName,implement="Implement!")


@require_role(RanksPermissions.View)
@ranks_blueprint.route("/rank/<rank>",methods=["GET"])
async def view(rank):
    return await standardReturn("implement.html",sectionName,implement="Implement!")


@require_role(RanksPermissions.Add)
@ranks_blueprint.route("/add",methods=["GET","POST"])
async def add():
    return await standardReturn("implement.html",sectionName,implement="Implement!")


@require_role(RanksPermissions.Remove)
@ranks_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    return await standardReturn("implement.html",sectionName,implement="Implement!")


@require_role(RanksPermissions.Edit)
@ranks_blueprint.route("/edit",methods=["GET","POST"])
async def edit():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
