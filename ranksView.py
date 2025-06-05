#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

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

@refreshToken
@require_login
@ranks_blueprint.route("/rank/<rank>",methods=["GET"])
async def rank(rank):
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack

@refreshToken
@require_role(RanksPermissions.addRankRole)
@ranks_blueprint.route("/add",methods=["GET","POST"])
async def add():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    # form = AddRankForm()
    # if request.method == 'GET':
    #     return await render_template("ranksAdd.html",FORM=form,sectionName)
    # elif request.method == 'POST':
    #     name         = (await request.form)['Name']
    #     description  = (await request.form)['Description']
    #     rank         = RankTable(Name=name,Description=description)
    #     if form.validate_on_submit():
    #         try:
    #             with db.bind.Session() as s:
    #                 with s.begin():
    #                     s.add(rank)
    #                     s.commit()
    #         except Exception as e:
    #             return await render_template("ranksAdd.html",FORM=form,sectionName,MESSAGE=str(e))
    #         return await render_template("ranksAdd.html",FORM=form,sectionName,MESSAGE="Success")
    # else:
    #     return await render_template("error.html",ERROR="Invalid method",sectionName)

@refreshToken
@require_role(RanksPermissions.removeRankRole)
@ranks_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack

@refreshToken
@require_role(RanksPermissions.editRankRole)
@ranks_blueprint.route("/edit",methods=["GET","POST"])
async def edit():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
