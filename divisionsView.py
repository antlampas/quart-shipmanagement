#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from quart          import Blueprint
from quart          import current_app
from quart          import render_template
from quart          import request
from quart          import redirect
from sqlalchemy     import select
from sqlalchemy.orm import Session

from time           import sleep

from model          import db
from model          import DivisionTable
from model          import selectDivision
from forms          import AddDivisionForm
from forms          import RemoveDivisionForm
from forms          import EditDivisionForm

from authorization  import require_role
from authorization  import require_login
from authorization  import refreshToken

from permissions    import DivisionsPermissions

from baseClasses    import Editable
from baseClasses    import Addable

from standardReturn import standardReturn

divisions_blueprint = Blueprint("divisions",__name__,url_prefix='/divisions',template_folder='templates/default')

sectionName = "Divisions"

@refreshToken
@require_login
@divisions_blueprint.route("/",methods=["GET"])
async def divisions():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    # divisions = list()
    # with db.bind.Session() as s:
    #     with s.begin():
    #         divisions = s.scalars(selectDivision()).all()
    # if len(divisions) > 0:
    #     return await render_template("divisions.html",divisions=divisions,sectionName)
    # else:
    #     return await render_template("divisions.html",divisions=str("No divisions found"),sectionName)

@refreshToken
@require_login
@divisions_blueprint.route("/division/<division>",methods=["GET"])
async def division(division):
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    # divisionData = DivisionTable()
    # try:
    #     with db.bind.Session() as s:
    #         with s.begin():
    #             divisionData = s.scalar(selectDivision(division))
    # except Exception as e:
    #     return await render_template("division.html",division=str("No division found with that name"),sectionName)
    # return await render_template("division.html",division=divisionData,sectionName)

@refreshToken
@require_role(DivisionsPermissions.addDivisionRole)
@divisions_blueprint.route("/add",methods=["GET","POST"])
async def add():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    # if request.method == 'GET':
    #     form = AddDivisionForm()
    #     return await render_template("divisionsAdd.html",FORM=form,sectionName)
    # elif request.method == 'POST':
    #     name        = (await request.form)['Name']
    #     description = (await request.form)['Description']
    #
    #     division = DivisionTable(Name=name,Description=description)
    #
    #     if form.validate_on_submit():
    #         try:
    #             with db.bind.Session() as s:
    #                 with s.begin():
    #                     s.add(division)
    #                     s.commit()
    #         except Exception as e:
    #             return await render_template("divisionsAdd.html",FORM=form,sectionName,MESSAGE=str(e))
    #         return await render_template("divisionsAdd.html",FORM=form,sectionName,MESSAGE="Success")
    # else:
    #     return await render_template("error.html",ERROR="Invalid method",sectionName)

@refreshToken
@require_role(DivisionsPermissions.removeDivisionRole)
@divisions_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    # form = RemoveDivisionForm()
    # divisions = list()
    # if request.method == 'GET':
    #     try:
    #         with db.bind.Session() as s:
    #             with s.begin():
    #                 divisions = s.scalars(selectDivision()).all()
    #     except Exception as e:
    #         return await render_template("divisionsRemove.html",FORM=form,sectionName,MESSAGE=str(e))
    #     form.Name.choices = [(d.Name,d.Name) for d in divisions]
    #     return await render_template("divisionsRemove.html",FORM=form,sectionName)
    # elif request.method == 'POST':
    #     if form.validate_on_submit():
    #         division = (await request.form).getlist('Name')
    #         try:
    #             for i in division:
    #                 with db.bind.Session() as s:
    #                     with s.begin():
    #                         d = s.scalar(selectDivision(i))
    #                         s.delete(d)
    #                         s.commit()
    #         except Exception as e:
    #             return await render_template("divisionsRemove.html",FORM=form,sectionName,MESSAGE="1: "+str(e))
    #         form = RemoveDivisionForm()
    #         try:
    #             with db.bind.Session() as s:
    #                 with s.begin():
    #                     d = s.scalars(selectDivision()).all()
    #                     for i in d:
    #                         divisions = s.scalars(selectDivision()).all()
    #         except Exception as e:
    #             return await render_template("divisionsRemove.html",FORM=form,sectionName,MESSAGE="2: "+str(e))
    #         form.Name.choices = [(d.Name,d.Name) for d in divisions]
    #         return await render_template("divisionsRemove.html",FORM=form,sectionName,MESSAGE="Success")
    # return await render_template("implement.html",implement="Implement!",sectionName)

@refreshToken
@require_role(DivisionsPermissions.editDivisionRole)
@divisions_blueprint.route("/edit/<division>",methods=["GET","POST"])
async def edit(division):
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack
    # form = EditDivisionForm()
    # if request.method == 'GET':
    #     with db.bind.Session() as s:
    #         with s.begin():
    #             divisionDB = s.scalar(selectDivision(member)).one()
    #     form.Name.data        = divisionDB.Name
    #     form.Description.data = divisionDB.Description
    #     return await render_template("divisionEdit.html",FORM=form,sectionName)
    # elif request.method == 'POST':
    #     name        = (await request.form)['Name']
    #     description = (await request.form)['Description']
    #
    #     division = DivisionTable(Name=name,Description=description)
    #
    #     if form.validate_on_submit():
    #         try:
    #             with db.bind.Session() as s:
    #                 with s.begin():
    #                     s.edit(division)
    #                     s.commit()
    #         except Exception as e:
    #             return await render_template("divisionEdit.html",FORM=form,sectionName,MESSAGE=str(e))
    #         return await render_template("divisionEdit.html",FORM=form,sectionName,MESSAGE="Success")
    # else:
    #     return await render_template("error.html",ERROR="Invalid method",sectionName)
