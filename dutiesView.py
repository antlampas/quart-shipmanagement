#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from   threading     import Timer
from   time          import sleep

from   quart         import Blueprint
from   quart         import current_app
from   quart         import request

from   authorization import require_role
from   authorization import require_login
from   authorization import refreshToken

from   permissions   import DutiesPermissions

from   loaders       import get
from   loaders       import remove
from   loaders       import add
from   loaders       import edit

from   dutiesClasses import Duty
from   dutiesClasses import Duties

from   forms         import AddDutyForm
from   forms         import RemoveDutyForm
from   forms         import EditDutyForm

from   standardReturn import standardReturn

duties_blueprint = Blueprint("duties",__name__,url_prefix='/duties',template_folder='templates/default')

sectionName = "Duties"

@require_role(DutiesPermissions.View)
@duties_blueprint.route("/",methods=["GET"])
async def duties():
    global sectionName
    d = get('duties')
    if 'Error' not in d and 'Warning' not in d:
        return await standardReturn("duties.html",
                                    sectionName,
                                    DUTIES=d
                                   )
    else:
        message="No duties found"
        return await standardReturn("divisions.html",
                                    sectionName,
                                    DUTIES=message
                                   )


@require_role(DutiesPermissions.View)
@duties_blueprint.route("/duty/<name>",methods=["GET"])
async def view(name):
    global sectionName
    d = get('duties',{'name' : name})
    if 'Error' not in d and 'Warning' not in d:
        return await standardReturn("duty.html",
                                    sectionName,
                                    DUTY=d
                                   )
    else:
        message = "Duty not found"
        return await standardReturn("duty.html",
                                    sectionName,
                                    DUTY=message
                                   )


@require_role(DutiesPermissions.Add)
@duties_blueprint.route("/add",methods=["GET","POST"])
async def addDuty():
    global sectionName
    message = ''
    duty    = Duty()
    form    = AddDutyForm()
    if request.method == 'GET':
        return await standardReturn("dutiesAdd.html",
                                    sectionName,
                                    FORM=form,
                                    MESSAGE=message
                                   )
    elif request.method == 'POST':
        if await form.validate_on_submit():
            name         = (await request.form)['Name']
            description  = (await request.form)['Description']
            duty         = Duty(name,description)
            d            = duty.serialize()
            added        = add('duty',d)
            if 'Error' in added or 'Warning' in added:
                message = added
            else:
                message = "Duty added"
        else:
            message = "Invalid data"
        return await standardReturn("dutiesAdd.html",
                                    f'Add {sectionName}',
                                    FORM=form,
                                    MESSAGE=message
                                   )
    else:
        return await standardReturn("error.html",
                                     sectionName,
                                     ERROR="Invalid method"
                                    )
@require_role(DutiesPermissions.Remove)
@duties_blueprint.route("/remove",methods=["GET","POST"])
async def removeDuty():
    global sectionName
    message   = ''
    form      = RemoveDivisionForm()
    duties = list()
    if request.method == 'GET':
        duties = get('duties')
        if 'Error' not in removed and 'Warning' not in removed:
            form.Name.choices = [(d['Name'],d['Name']) for d in duties]
        return await standardReturn("dutiesRemove.html",
                                    f'Remove {sectionName}',
                                    FORM=form,
                                    MESSAGE=message
                                   )
    elif request.method == 'POST':
        if await form.validate_on_submit():
            duties = (await request.form).getlist('Name')
            for duty in duties:
                removed = remove('duty',i)
                if 'Error' in removed and 'Warning' in removed:
                    message = f'Unable to remove {duty}'
                    break
            if not message:
                message = "Duty removed"
            form = RemoveDivisionForm()
            duties = get('duties')
            if 'Error' not in removed and 'Warning' not in removed:
                form.Name.choices = [(d['Name'],d['Name']) for d in duties]
            return await standardReturn("dutiesRemove.html",
                                        f'Remove {sectionName}',
                                        FORM=form,
                                        MESSAGE=message
                                       )
        else:
            message="Invalid data"
            return await standardReturn("dutiesRemove.html",
                                        f'Remove {sectionName}',
                                        FORM=form,
                                        MESSAGE=message
                                       )
    else:
        return await standardReturn("error.html",
                                    f'Remove {sectionName}',
                                    ERROR="Invalid method"
                                   )
@require_role(DutiesPermissions.Edit)
@duties_blueprint.route("/edit/",methods=["GET","POST"])
async def edit():
    return await standardReturn("error.html",
                                f'Edit {sectionName}',
                                ERROR="No duties provided"
                               )
@require_role(DutiesPermissions.Edit)
@duties_blueprint.route("/edit/<name>",methods=["GET","POST"])
async def editDuty(name):
    global sectionName
    def f(): del session['dutyEdit']
    timer = Timer(current_app.config['EDITING_TIME'],f)
    form = EditDutyForm()
    message = ''
    if request.method == 'GET':
        duty = get('duty',name)
        if 'Error' not in duty and 'Warning' not in duty:
            form.Name.data        = duty.Name
            form.Description.data = duty.Description
        else:
            message = "Invalid name"
        return await standardReturn("dutiesEdit.html",
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
            edited = edit('duty',
                          {
                            'Name'        : name,
                            'Description' : description
                          }
                         )
            if 'Error' not in edited and 'Warning' not in edited:
                message=f'{name} edited'
            else:
                message = 'Edit went wrong'
        return await standardReturn("dutiesEdit.html",
                                    f'Edit {sectionName}',
                                    FORM=form,
                                    MESSAGE="Success"
                                   )
    else:
        return await standardReturn("error.html",
                                    f'Edit {sectionName}',
                                    ERROR="Invalid method"
                                   )
