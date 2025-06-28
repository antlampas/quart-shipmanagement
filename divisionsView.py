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

@require_role(DivisionsPermissions.View)
@divisions_blueprint.route("/",methods=["GET"])
async def divisions():
    global sectionName
    divisions = get('divisions')
    if 'Error' not in divisions and 'Warning' not in divisions:
        return await standardReturn("divisions.html",
                                    sectionName,
                                    DIVISIONS=divisions
                                   )
    else:
        message="No division found"
        return await standardReturn("divisions.html",
                                    sectionName,
                                    DIVISIONS=message
                                   )

@require_role(DivisionsPermissions.View)
@divisions_blueprint.route("/division/<name>",methods=["GET"])
async def view(name):
    global sectionName
    division = get('division',name)
    if 'Error' not in divisions and 'Warning' not in divisions:
        return await standardReturn("divisions.html",
                                    sectionName,
                                    DIVISION=division
                                   )
    else:
        message = "Division not found"
        return await standardReturn("divisions.html",
                                    sectionName,
                                    DIVISION=message
                                   )

@require_role(DivisionsPermissions.Add)
@divisions_blueprint.route("/add",methods=["GET","POST"])
async def addDivision():
    global sectionName
    division = Division()
    form     = AddDivisionForm()
    if request.method == 'GET':
        return await standardReturn("divisionsAdd.html",
                                    f'Add {sectionName}',
                                    FORM=form
                                   )
    elif request.method == 'POST':
        if await form.validate_on_submit():
            message = ""
            name        = (await request.form)['Name']
            description = (await request.form)['Description']
            division = Division(name,description)
            added = add('division',division.serialize())
            if 'Error' in added and 'Warning' in added:
                message = added
            else:
                message = "Division added"
        else:
            message = "Invalid data"
        return await standardReturn("divisionsAdd.html",
                                    f'Add {sectionName}',
                                    FORM=form,
                                    MESSAGE=message
                                   )
    else:
        return await standardReturn("error.html",
                                    f'Add {sectionName}',
                                    ERROR="Invalid method"
                                   )

@require_role(DivisionsPermissions.Remove)
@divisions_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    global sectionName
    message   = ''
    form      = RemoveDivisionForm()
    divisions = list()
    if request.method == 'GET':
        divisions = get('divisions')
        if 'Error' not in removed and 'Warning' not in removed:
            form.Name.choices = [(d['Name'],d['Name']) for d in divisions]
        return await standardReturn("divisionsRemove.html",
                                    f'Remove {sectionName}',
                                    FORM=form,
                                    MESSAGE=message
                                   )
    elif request.method == 'POST':
        if await form.validate_on_submit():
            divisions = (await request.form).getlist('Name')
            for division in divisions:
                removed = remove('division',i)
                if 'Error' in removed and 'Warning' in removed:
                    message = f'Unable to remove {division}'
                    break
            if not message:
                message = "Divisions removed"
            form = RemoveDivisionForm()
            divisions = get('divisions')
            if 'Error' not in removed and 'Warning' not in removed:
                form.Name.choices = [(d['Name'],d['Name']) for d in divisions]
            return await standardReturn("divisionsRemove.html",
                                        f'Remove {sectionName}',
                                        FORM=form,
                                        MESSAGE=message
                                       )
        else:
            message="Invalid data"
            return await standardReturn("divisionsRemove.html",
                                        f'Remove {sectionName}',
                                        FORM=form,
                                        MESSAGE=message
                                       )
    else:
        return await standardReturn("error.html",
                                    f'Remove {sectionName}',
                                    ERROR="Invalid method"
                                   )

@require_role(DivisionsPermissions.Edit)
@divisions_blueprint.route("/edit/",methods=["GET","POST"])
async def edit():
    return await standardReturn("error.html",
                                f'Edit {sectionName}',
                                ERROR="No division provided"
                               )

@require_role(DivisionsPermissions.Edit)
@divisions_blueprint.route("/edit/<name>",methods=["GET","POST"])
async def editDivision(name):
    global sectionName
    def f(): del session['divisionEdit']
    timer = Timer(current_app.config['EDITING_TIME'],f)
    form = EditDivisionForm()
    message = ''
    if request.method == 'GET':
        division = get('division',name)
        if 'Error' not in division and 'Warning' not in division:
            form.Name.data        = division.Name
            form.Description.data = division.Description
        else:
            message = "Invalid name"
        return await standardReturn("divisionsEdit.html",
                                    f'Edit {sectionName}',
                                    FORM=form,
                                    MESSAGE=message
                                   )
    elif request.method == 'POST':
        name        = (await request.form)['Name']
        description = (await request.form)['Description']
        if await form.validate_on_submit():
            form.Name.data        = name
            form.Description.data = description
            edited = edit('division',
                          {
                            'Name'        : name,
                            'Description' : description
                          }
                         )
            if 'Error' not in edited and 'Warning' not in edited:
                message=f'{name} edited'
            else:
                message = 'Edit went wrong'
        return await standardReturn("divisionsEdit.html",
                                    f'Edit {sectionName}',
                                    FORM=form,
                                    MESSAGE="Success"
                                   )
    else:
        return await standardReturn("error.html",
                                    f'Edit {sectionName}',
                                    ERROR="Invalid method"
                                   )