#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from threading      import Timer

from quart          import current_app
from quart          import Blueprint

from model          import db
from model          import CrewMemberTable
from model          import TaskTable
from model          import MemberTaskLogEntryTable

from authorization  import require_role
from authorization  import require_login
from authorization  import refreshToken

from permissions    import TasksPermissions

from tasksClasses   import Task
from tasksClasses   import Tasks

from standardReturn import standardReturn

tasks_blueprint = Blueprint("tasks",__name__,url_prefix='/tasks',template_folder='templates/default')

sectionName = "Tasks"


@require_role(TasksPermissions.View)
@tasks_blueprint.route("/")
async def tasks():
    return await standardReturn("implement.html",sectionName,implement="Implement!")


@require_role(TasksPermissions.View)
@tasks_blueprint.route("/task/<task>")
async def view(task):
    return await standardReturn("implement.html",sectionName,implement="Implement!")


@require_role(TasksPermissions.Add)
@tasks_blueprint.route("/add")
async def add():
    return await standardReturn("implement.html",sectionName,implement="Implement!")


@require_role(TasksPermissions.Remove)
@tasks_blueprint.route("/remove")
async def remove():
    return await standardReturn("implement.html",sectionName,implement="Implement!")


@require_role(TasksPermissions.Edit)
@tasks_blueprint.route("/edit")
async def edit():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
