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
from model          import DutyTable

from forms          import AddDutyForm
from forms          import RemoveDutyForm
from forms          import EditDutyForm

from authorization  import require_role
from authorization  import require_login
from authorization  import refreshToken

from permissions    import DutiesPermissions

from dutiesClasses  import Duty
from dutiesClasses  import Duties

from standardReturn import standardReturn

sectionName = "Duties"

duties_blueprint = Blueprint("duties",__name__,url_prefix='/duties',template_folder='templates/default')

@refreshToken
@require_role(DutiesPermissions.View)
@duties_blueprint.route("/",methods=["GET"])
async def duties():
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@refreshToken
@require_role(DutiesPermissions.View)
@duties_blueprint.route("/duty/<duty>",methods=["GET"])
async def view(duty):
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@refreshToken
@require_role(DutiesPermissions.Add)
@duties_blueprint.route("/add",methods=["GET","POST"])
async def add():
    #return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    form = AddDutyForm()
    if request.method == 'GET':
        return await render_template("dutiesAdd.html",sectionName,FORM=form)
    elif request.method == 'POST':
        name         = (await request.form)['Name']
        description  = (await request.form)['Description']
        duty         = DutyTable(Name=name,Description=description)
        if form.validate_on_submit():
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        s.add(duty)
                        s.commit()
            except Exception as e:
                return await render_template("dutiesAdd.html",sectionName,FORM=form,MESSAGE=str(e))
            return await render_template("dutiesAdd.html",sectionName,FORM=form,MESSAGE="Success")
    else:
        return await render_template("error.html",sectionName,ERROR="Invalid method")

@refreshToken
@require_role(DutiesPermissions.Remove)
@duties_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack

@refreshToken
@require_role(DutiesPermissions.Edit)
@duties_blueprint.route("/edit",methods=["GET","POST"])
async def edit():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
