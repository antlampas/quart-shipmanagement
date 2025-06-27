#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from threading      import Timer

from quart            import Blueprint
from quart            import current_app
from quart            import request
from quart            import redirect
from sqlalchemy       import select
from sqlalchemy.orm   import Session

from time             import sleep

from authorization    import require_role
from authorization    import require_login
from authorization    import refreshToken

from permissions      import DivisionsPermissions

from loaders import get
from loaders import remove
from loaders import add
from loaders import edit

from divisionsClasses import Division
from divisionsClasses import Divisions

from forms import AddDivisionForm
from forms import EditDivisionForm
from forms import RemoveDivisionForm

from standardReturn import standardReturn

divisions_blueprint = Blueprint("divisions",__name__,url_prefix='/divisions',template_folder='templates/default')

sectionName = "Divisions"

@refreshToken
@require_role(DivisionsPermissions.View)
@divisions_blueprint.route("/",methods=["GET"])
async def divisions():
    global sectionName
    divisions = get('divisions')
    if divisions:
        return await standardReturn("divisions.html",
                                    sectionName,
                                    DIVISIONS=divisions
                                   )
    else:
        errorMessage="No division found"
        return await standardReturn("divisions.html",
                                    sectionName,
                                    DIVISIONS=errorMessage
                                   )

@refreshToken
@require_role(DivisionsPermissions.View)
@divisions_blueprint.route("/division/<name>",methods=["GET"])
async def view(name):
    global sectionName
    division = get('division',name)
    if division:
        return await standardReturn("divisions.html",
                                    sectionName,
                                    DIVISION=division
                                   )
    else:
        return await standardReturn("error.html",
                                    sectionName,
                                    ERROR="Crew member not found"
                                   )

@refreshToken
@require_role(DivisionsPermissions.Add)
@divisions_blueprint.route("/add",methods=["GET","POST"])
async def add():
    global sectionName
    form = AddDivisionForm()
    if request.method == 'GET':
        return await standardReturn("divisionsAdd.html",sectionName,FORM=form)
    elif request.method == 'POST':
        name        = (await request.form)['Name']
        description = (await request.form)['Description']
        division = DivisionTable(Name=name,Description=description)
        if form.validate_on_submit():
            add('division',{'Name' : name,'Description' : description})
            return await standardReturn("divisionsAdd.html",sectionName,FORM=form,MESSAGE="Success")
        else:
            return await standardReturn("error.html",sectionName,ERROR="Invalid data")
    else:
        return await renderstandardReturn_template("error.html",sectionName,ERROR="Invalid method")

@refreshToken
@require_role(DivisionsPermissions.Remove)
@divisions_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    global sectionName
    form = RemoveDivisionForm()
    divisions = list()
    if request.method == 'GET':
        divisions = get('divisions')
        if divisions:
            form.Name.choices = [(d['Name'],d['Name']) for d in divisions]
        return await standardReturn("divisionsRemove.html",sectionName,FORM=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            division = (await request.form).getlist('Name')
            for i in division:
                remove('division',i)
            form = RemoveDivisionForm()
            divisions = get('divisions')
            if divisions:
                form.Name.choices = [(d['Name'],d['Name']) for d in divisions]
            return await standardReturn("divisionsRemove.html",sectionName,FORM=form,MESSAGE="Success")
        else:
            return await standardReturn("error.html",sectionName,ERROR="Invalid data")
    else:
        return await standardReturn("error.html",sectionName,ERROR="Invalid method")

@refreshToken
@require_role(DivisionsPermissions.Edit)
@divisions_blueprint.route("/edit/",methods=["GET","POST"])
async def edit():
    return await standardReturn("error.html",sectionName,ERROR="No division provided")

@refreshToken
@require_role(DivisionsPermissions.Edit)
@divisions_blueprint.route("/edit/<name>",methods=["GET","POST"])
async def editDivision(name):
    global sectionName
    form = EditDivisionForm()
    division = get('division',name)
    if division:
        def f(): del session['divisionEdit']
        timer = Timer(current_app.config['EDITING_TIME'],f)
        if request.method == 'GET':
            form.Name.data        = division.Name
            form.Description.data = division.Description
            return await standardReturn("divisionsEdit.html",sectionName,FORM=form)
        elif request.method == 'POST':
            name        = (await request.form)['Name']
            description = (await request.form)['Description']
            if form.validate_on_submit():
                edit('division',{'Name' : name,'Division' : division})
            form.Name.data     = name
            form.Division.data = division
            return await standardReturn("divisionsEdit.html",sectionName,FORM=form,MESSAGE="Success")
        else:
            return await standardReturn("error.html",sectionName,ERROR="Invalid method")
    else:
        return await standardReturn("divisionsEdit.html",sectionName,FORM=form,MESSAGE="No division found")