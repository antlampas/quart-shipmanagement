#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from threading      import Timer

from quart          import Blueprint
from quart          import current_app
from quart          import request
from quart          import redirect
from quart          import url_for
from quart          import session

from forms          import AddCrewMemberForm
from forms          import RemoveCrewMemberForm
from forms          import EditCrewMemberForm

from authorization  import require_user
from authorization  import require_role
from authorization  import require_login
from authorization  import refreshToken

from permissions    import CrewPermissions

from crewClasses    import CrewMember
from crewClasses    import Crew

from loaders import get
from loaders import remove
from loaders import add
from loaders import edit

from standardReturn import standardReturn

crew_blueprint = Blueprint("crew",
                           __name__,
                           url_prefix='/crew',
                           template_folder='templates/default'
                          )
sectionName    = "Crew"


@require_login
@crew_blueprint.route("/",methods=["GET"])
async def crewView():
    global sectionName
    crew = Crew()
    crewLoaded = get('crew')
    if 'Error' not in crewLoaded and 'Warning' not in crewLoaded:
        crew.deserialize(crewLoaded)
    else:
        crew = None
    if crew:
        return await standardReturn("crew.html",sectionName,CREW=crew)
    else:
        errorMessage = "No crew member found"
        return await standardReturn("crew.html",sectionName,CREW=errorMessage)


@require_role(CrewPermissions.View)
@crew_blueprint.route("/member/<nickname>",methods=["GET"])
async def memberView(nickname):
    global sectionName
    member = CrewMember()
    memberLoaded = get('crewMember',nickname)
    if 'Error' not in memberLoaded and 'Warning' not in memberLoaded:
        member.deserialize(memberLoaded)
    if member:
        return await standardReturn("crewMember.html",sectionName,MEMBER=member)
    else:
        errorMessage = "Crew member not found"
        return await standardReturn("error.html",sectionName,ERROR=errorMessage)


@require_role(CrewPermissions.Add)
@crew_blueprint.route("/add",methods=["GET","POST"])
async def add():
    global sectionName
    member = CrewMember()
    form   = AddCrewMemberForm()
    if request.method == 'GET':
        ranks     = get('rank')
        duties    = get('dutie')
        divisions = get('division')
        if ranks and 'Error' not in ranks and 'Warning' not in ranks:
            form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
        else:
            print(ranks)
        if duties and 'Error' not in duties and 'Warning' not in duties:
            form.Duties.choices   = [(d.Name,d.Name) for d in duties]
        else:
            print(duties)
        if divisions and 'Error' not in divisions and 'Warning' not in divisions:
            form.Division.choices = [(d.Name,d.Name) for d in divisions]
        else:
            print(divisions)
        return await standardReturn("crewMemberAdd.html",
                                    f'Add {sectionName}',
                                    FORM=form
                                   )
    elif request.method == 'POST':
        if await form.validate_on_submit():
            member = CrewMember(
                              FirstName = (await request.form)['FirstName'],
                              LastName  = (await request.form)['LastName'],
                              Nickname  = (await request.form)['Nickname'],
                              Rank      = (await request.form)['Rank'],
                              Division  = (await request.form)['Division'],
                              Duties    = (await request.form).getlist('Duties')
                                   )
            form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
            form.Duties.choices   = [(d.Name,d.Name) for d in duties]
            form.Division.choices = [(d.Name,d.Name) for d in divisions]
            added = add('crewMember',member.serialize())
            if 'Error' in added and 'Warning' in added:
                message = added
                return await standardReturn("crewMemberAdd.html",
                                            sectionName,
                                            FORM=form,
                                            DUTIES=duties,
                                            MESSAGE=message
                                           )
            message = 'Success'
            return await standardReturn("crewMemberAdd.html",
                                         sectionName,
                                         FORM=form,
                                         DUTIES=duties,
                                         MESSAGE=message
                                       )
    else:
        error = "Invalid method"
        return await standardReturn("error.html",sectionName,ERROR=error)


@require_role(CrewPermissions.Remove)
@crew_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    global sectionName
    message = ''
    form    = RemoveCrewMemberForm()
    crew    = list()
    if request.method == 'GET':
        crew = get('crew')
        if crew and 'Error' not in crew and 'Warning' not in crew:
            form.Nickname.choices = [(c.Nickname,c.Nickname) for c in crew]
        return await standardReturn("crewMemberRemove.html",
                                    f'Remove {sectionName}',
                                    FORM=form
                                   )
    elif request.method == 'POST':
        if await form.validate_on_submit():
            crew = (await request.form).getlist('Nickname')
            for member in crew:
                removed = remove('crewMember',member)
                if 'Error' not in removed and 'Warning' not in removed:
                    message = f'Unable to remove {member}'
                    break
            if not message:
                message = 'Members removed'
            form = RemoveCrewMemberForm()
            crew = get('crew')
            if 'Error' not in removed and 'Warning' not in removed:
                form.Nickname.choices = [(d['Nickname'],d['Nickname']) \
                                         for d in crew]
            return await standardReturn("crewMemberRemove.html",
                                        f'Remove {sectionName}',
                                        FORM=form,
                                        MESSAGE=message
                                       )
        else:
            message="Invalid data"
            return await standardReturn("crewMemberRemove.html",
                                        sectionName,
                                        FORM=form,
                                        MESSAGE=message
                                       )
    else:
        return await standardReturn("error.html",
                                    sectionName,
                                    ERROR="Invalid method"
                                   )


@require_role(CrewPermissions.Edit)
@crew_blueprint.route("/edit/",methods=["GET","POST"])
async def edit():
    global sectionName
    return await standardReturn("error.html",
                                f'Edit {sectionName}',
                                ERROR='No member specified'
                               )


@require_role(CrewPermissions.Edit)
@crew_blueprint.route("/edit/<member>",methods=["GET","POST"])
async def editMember(member):
    global sectionName
    # def f(): del session['memberEdit']
    # timer = Timer(current_app.config['EDITING_TIME'],f)
    form         = EditCrewMemberForm()
    ranks        = []
    duties       = []
    divisions    = []
    crewMember   = None
    crew         = None
    if request.method == 'GET':
        if re.match(isAlpha,member):
            message = ""
            memberLoaded = get('crewMember',member)
            if 'Error' not in memberLoaded and 'Warning' not in memberLoaded:
                member = CrewMember(
                                FirstName = memberLoaded['FirstName'],
                                LastName  = memberLoaded['LastName'],
                                Nickname  = memberLoaded['Nickname'],
                                Rank      = memberLoaded['Rank'],
                                Division  = memberLoaded['Division'],
                                Duties    = [d.DutyName \
                                             for d in memberLoaded['Duties']]
                                )
                form.FirstName.data   = member.FirstName
                form.LastName.data    = member.LastName
                form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
                form.Rank.default     = member.RankName
                form.Division.choices = [(d.Name,d.Name) for d in divisions]
                form.Division.default = member.DivisionName
                form.Duties.choices   = [(d.Name,d.Name) for d in duties]
                form.Duties.default   = [(d.DutyName,d.DutyName) \
                                         for d in member.Duties]
            else:
                message = "Invalid member"
            return await standardReturn("crewMemberEdit.html",
                                        f'Edit {sectionName}',
                                        FORM=form,
                                        MESSAGE=message
                                       )
        else:
            return await standardReturn("error.html",
                                        f'Edit {sectionName}',
                                        ERROR="Invalid member nickname"
                                       )
    elif request.method == 'POST':
        if 'memberEdit' in session:
            if await form.validate_on_submit():
                firstname      = (await request.form)['FirstName']
                lastname       = (await request.form)['LastName']
                nickname       = (await request.form)['Nickname']
                rank           = (await request.form)['Rank']
                division       = (await request.form)['Division']
                selectedDuties = (await request.form).getlist('Duties')

                member = CrewMember(FirstName = firstname,
                                    LastName  = lastname,
                                    Nickname  = session['memberEdit'],
                                    Rank      = rank,
                                    Division  = division,
                                    Duties    = selectedDuties
                                )
                edited = edit('crewMember',member.__dict__)
                if 'Error' not in memberLoaded and 'Warning' not in memberLoaded:
                    del session['memberEdit']
                    return redirect(url_for('crew.edit',member=member.Nickname))
                else:
                    form.FirstName.data   = member.FirstName
                    form.LastName.data    = member.LastName
                    form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
                    form.Rank.default     = member.RankName
                    form.Division.choices = [(d.Name,d.Name) for d in divisions]
                    form.Division.default = member.DivisionName
                    form.Duties.choices   = [(d.Name,d.Name) for d in duties]
                    form.Duties.default   = [(d.DutyName,d.DutyName) \
                                             for d in member.Duties]
                    message = "Edit went wrong"
                    return await standardReturn("crewMemberEdit.html",
                                                f'Edit {sectionName}',
                                                FORM=form,
                                                MESSAGE=message
                                               )
            else:
                message = "Invalid data"
                return await standardReturn("crewMemberEdit.html",
                                            f'Edit {sectionName}',
                                            FORM=form,
                                            MESSAGE=message
                                           )
        else:
            return await standardReturn("error.html",
                                        f'Edit {sectionName}',
                                        ERROR="Session expired"
                                       )
    else:
        return await standardReturn("error.html",
                                    f'Edit {sectionName}',
                                    ERROR="Invalid method"
                                   )
