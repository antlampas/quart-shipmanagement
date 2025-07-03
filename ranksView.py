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

from   permissions   import RanksPermissions

from   loaders       import get
from   loaders       import remove
from   loaders       import add
from   loaders       import edit

from   ranksClasses  import Rank
from   ranksClasses  import Ranks

from   forms         import AddRankForm
from   forms         import RemoveRankForm
from   forms         import EditRankForm

from standardReturn import standardReturn

ranks_blueprint = Blueprint("ranks",__name__,url_prefix='/ranks',template_folder='templates/default')

sectionName = "Ranks"

@require_role(RanksPermissions.View)
@ranks_blueprint.route("/",methods=["GET"])
async def ranks():
    global sectionName
    d = get('ranks')
    if 'Error' not in d and 'Warning' not in d:
        return await standardReturn("ranks.html",
                                    sectionName,
                                    RANKS=d
                                   )
    else:
        message="No rank found"
        return await standardReturn("ranks.html",
                                    sectionName,
                                    RANKS=message
                                   )
@require_role(RanksPermissions.View)
@ranks_blueprint.route("/rank/<name>",methods=["GET"])
async def view(name):
    global sectionName
    r = get('rank',{'name' : name})
    if 'Error' not in r and 'Warning' not in r:
        return await standardReturn("rank.html",
                                    sectionName,
                                    RANK=r
                                   )
    else:
        message = "Rank not found"
        return await standardReturn("rank.html",
                                    sectionName,
                                    RANK=message
                                   )
@require_role(RanksPermissions.Add)
@ranks_blueprint.route("/add",methods=["GET","POST"])
async def addRank():
    global sectionName
    rank = Rank()
    form = AddRankForm()
    if request.method == 'GET':
        return await standardReturn("ranksAdd.html",
                                    f'Add {sectionName}',
                                    FORM=form
                                   )
    elif request.method == 'POST':
        if await form.validate_on_submit():
            message = ""
            name        = (await request.form)['Name']
            description = (await request.form)['Description']
            rank = Rank(name,description)
            r = rank.serialize()
            added = add('rank',r)
            if 'Error' in added or 'Warning' in added:
                message = added
            else:
                message = "Rank added"
        else:
            message = "Invalid data"
        return await standardReturn("ranksAdd.html",
                                    f'Add {sectionName}',
                                    FORM=form,
                                    MESSAGE=message
                                   )
    else:
        return await standardReturn("error.html",
                                    f'Add {sectionName}',
                                    ERROR="Invalid method"
                                   )

@require_role(RanksPermissions.Remove)
@ranks_blueprint.route("/remove",methods=["GET","POST"])
async def removeRank():
    global sectionName
    message   = ''
    form      = RemoveRankForm()
    divisions = list()
    if request.method == 'GET':
        ranks = get('ranks')
        if 'Error' not in ranks and 'Warning' not in ranks:
            form.Name.choices = [(d['Name'],d['Name']) for d in divisions]
        return await standardReturn("ranksRemove.html",
                                    f'Remove {sectionName}',
                                    FORM=form,
                                    MESSAGE=message
                                   )
    elif request.method == 'POST':
        if await form.validate_on_submit():
            ranks = (await request.form).getlist('Name')
            for rank in ranks:
                removed = remove('rank',rank)
                if 'Error' in removed and 'Warning' in removed:
                    message = f'Unable to remove {rank}'
                    break
            if not message:
                message = "Rank removed"
            form = RemoveDivisionForm()
            ranks = get('ranks')
            if 'Error' not in ranks and 'Warning' not in ranks:
                form.Name.choices = [(r['Name'],r['Name']) for r in ranks]
            return await standardReturn("ranksRemove.html",
                                        f'Remove {sectionName}',
                                        FORM=form,
                                        MESSAGE=message
                                       )
        else:
            message="Invalid data"
            return await standardReturn("ranksRemove.html",
                                        f'Remove {sectionName}',
                                        FORM=form,
                                        MESSAGE=message
                                       )
    else:
        return await standardReturn("error.html",
                                    f'Remove {sectionName}',
                                    ERROR="Invalid method"
                                   )
@require_role(RanksPermissions.Edit)
@ranks_blueprint.route("/edit/",methods=["GET","POST"])
async def edit():
    return await standardReturn("error.html",
                                f'Edit {sectionName}',
                                ERROR="No rank provided"
                               )

@require_role(RanksPermissions.Edit)
@ranks_blueprint.route("/edit/<name>",methods=["GET","POST"])
async def editRank(name):
    global sectionName
    def f(): del session['rankEdit']
    timer = Timer(current_app.config['EDITING_TIME'],f)
    form = EditRankForm()
    message = ''
    if request.method == 'GET':
        rank = get('rank',name)
        if 'Error' not in rank and 'Warning' not in rank:
            form.Name.data        = rank.Name
            form.Description.data = rank.Description
        else:
            message = "Invalid name"
        return await standardReturn("rankEdit.html",
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
            edited = edit('rank',
                          {
                            'name'        : name,
                            'description' : description
                          }
                         )
            if 'Error' not in edited and 'Warning' not in edited:
                message=f'{name} edited'
            else:
                message = 'Edit went wrong'
        return await standardReturn("ranksEdit.html",
                                    f'Edit {sectionName}',
                                    FORM=form,
                                    MESSAGE="Success"
                                   )
    else:
        return await standardReturn("error.html",
                                    f'Edit {sectionName}',
                                    ERROR="Invalid method"
                                   )
