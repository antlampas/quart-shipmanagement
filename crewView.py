#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re
import requests
import json

from types          import SimpleNamespace
from time           import sleep
from jose           import jwt

from sqlalchemy     import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from quart          import Blueprint
from quart          import current_app
from quart          import request
from quart          import redirect
from quart          import url_for
from quart          import session

from config         import KeycloakConfig

from model          import db
from model          import loadFromDB
from model          import saveToDB

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

from standardReturn import standardReturn

crew_blueprint = Blueprint("crew",
                           __name__,
                           url_prefix='/crew',
                           template_folder='templates/default'
                          )
sectionName    = "Crew"

@require_login
@refreshToken
@crew_blueprint.route("/",methods=["GET"])
async def crew():
    global sectionName
    crewDB = loadFromDB('crew')
    if crewDB:
        return await standardReturn("crew.html",
                                    sectionName,
                                    CREW=crewDB.Crew
                                   )
    else:
        return await standardReturn("error.html",
                                    sectionName,
                                    ERROR="No crew member found"
                                   )

@require_user(groups=['Equipaggio'])
@refreshToken
@crew_blueprint.route("/member/<member>",methods=["GET"])
async def member(member):
    global sectionName
    crewMember = loadFromDB('crewMember',member)
    if crewMember:
        for cm in crewMember.Crew:
            if cm.Nickname == member:
                crewMember = cm
                break
    if crewMember:
        return await standardReturn("crewMember.html",
                                    sectionName,
                                    CREWMEMBER=crewMember
                                   )
    else:
        return await standardReturn("error.html",
                                    sectionName,
                                    ERROR="Crew member not found"
                                   )

@require_role(CrewPermissions.addMemberRole)
@refreshToken
@crew_blueprint.route("/add",methods=["GET","POST"])
async def add():
    # return await standardReturn("implement.html",
    #                             sectionName,
    #                             implement="Implement!"
    #                            )
    #TODO: Make it work with keycloack too
    global sectionName
    form   = AddCrewMemberForm()
    if request.method == 'GET':
        ranks     = []
        duties    = []
        divisions = []
        try:
            with db.bind.Session() as s:
                with s.begin():
                    ranks     = loadFromDB('ranks')
                    duties    = loadFromDB('duties')
                    divisions = loadFromDB('divisions')
        except Exception as e:
                return await standardReturn("error.html",
                                            'Add' + sectionName,
                                            ERROR=str(e)
                                           )
        form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
        form.Duties.choices   = [(d.Name,d.Name) for d in duties]
        form.Division.choices = [(d.Name,d.Name) for d in divisions]
        return await standardReturn("crewMemberAdd.html",sectionName,FORM=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            crewMember = CrewMember(
                                  FirstName = (await request.form)['FirstName'],
                                  LastName  = (await request.form)['LastName'],
                                  Nickname  = (await request.form)['Nickname'],
                                  Rank      = (await request.form)['Rank'],
                                  Division  = (await request.form)['Division'],
                                  Duties    = (await request.form)\
                                                              .getlist('Duties')
                                   )
            # form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
            # form.Duties.choices   = [(d.Name,d.Name) for d in duties]
            # form.Division.choices = [(d.Name,d.Name) for d in divisions]

            if not saveToDB('crewMember',crewMember.__dict__):
                return await standardReturn(
                                         "error.html",
                                         sectionName,
                                         ERROR="Unable to save crew member data"
                                         )
            return await standardReturn("crewMemberAdd.html",
                                         sectionName,
                                         FORM=form,
                                         DUTIES=duties,
                                         MESSAGE='Success')
    else:
        return await standardReturn("error.html",
                                    sectionName,
                                    ERROR="Invalid method"
                                   )

@require_role(CrewPermissions.removeMemberRole)
@refreshToken
@crew_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    global sectionName
    return await standardReturn("implement.html",
                                sectionName,
                                implement="Implement!"
                               )
    #TODO: Make it work with keycloack too
    sectionName = 'Remove ' + sectionName
    form = RemoveCrewMemberForm()
    crew = list()
    if request.method == 'GET':
        crew = loadFromDB('crew')
        if crew:
            form.Nickname.choices = [(c.Nickname,c.Nickname) for c in crew]
        return await standardReturn("crewMemberRemove.html",
                                    sectionName,
                                    FORM=form
                                   )
    elif request.method == 'POST':
        members = (await request.form).getlist('Nickname')
        if form.validate_on_submit():
            for member in members:
                removeFromDB('person',{'nickname':member})
        return redirect(url_for('crew.remove'))
    else:
        return await standardReturn("error.html",
                                    sectionName,
                                    ERROR="Invalid method"
                                   )

@require_role(CrewPermissions.editMemberRole)
@refreshToken
@crew_blueprint.route("/edit/",methods=["GET","POST"])
async def edit():
    global sectionName
    return await standardReturn("error.html",
                                'Edit' + sectionName,
                                ERROR='No member specified'
                               )

@require_role(CrewPermissions.editMemberRole)
@refreshToken
@crew_blueprint.route("/edit/<member>",methods=["GET","POST"])
async def editMember(member):
    global sectionName
    return await standardReturn("implement.html",
                                sectionName,
                                implement="Implement!"
                               )
    #TODO: Make it work with keycloack too, make db managenet code
    #      more clear and check
    sectionName = 'Edit ' + sectionName
    form         = EditCrewMemberForm()
    ranks        = []
    duties       = []
    divisions    = []
    crewMember   = None
    crew         = None
    if request.method == 'GET':
        crewMember = loadFromDB('crewMember',member)
        member = CrewMember(FirstName = crewMember['FirstName'],
                            LastName  = crewMember['LastName'],
                            Nickname  = crewMember['Nickname'],
                            Rank      = crewMember['Rank'],
                            Division  = crewMember['Division'],
                            Duties    = [ d.DutyName for d in crewMemberDuties ]
                           )
        form.FirstName.data   = member.FirstName
        form.LastName.data    = member.LastName
        form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
        form.Rank.default     = member.RankName
        form.Division.choices = [(d.Name,d.Name) for d in divisions]
        form.Division.default = member.DivisionName
        form.Duties.choices   = [(d.Name,d.Name) for d in duties]
        form.Duties.default   = [(d.DutyName,d.DutyName) for d in member.Duties]
        return await standardReturn("crewMemberEdit.html",sectionName,FORM=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            firstname      = (await request.form)['FirstName']
            lastname       = (await request.form)['LastName']
            nickname       = (await request.form)['Nickname']
            rank           = (await request.form)['Rank']
            division       = (await request.form)['Division']
            selectedDuties = (await request.form).getlist('Duties')

            member = CrewMember(FirstName = firstname,
                                LastName  = lastname,
                                Nickname  = nickname,
                                Rank      = rank,
                                Division  = division,
                                Duties    = selectedDuties
                               )
            editDB('crewMember',member.__dict__)
            return redirect(url_for('crew.edit',
                                    member=personalBaseInformations.Nickname
                                   )
                           )
    else:
        return await standardReturn("error.html",
                                    sectionName,
                                    ERROR="Invalid method"
                                   )
