#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from quart import current_app,Blueprint

from model import db
from model import CrewMemberTable
from model import TaskTable
from model import MemberTaskLogEntryTable

from authorization  import require_role
from authorization  import require_login

from permissions    import TasksPermissions

from tasksClasses   import Task
from tasksClasses   import Tasks

from standardReturn import standardReturn

tasks_blueprint = Blueprint("tasks",__name__,url_prefix='/tasks',template_folder='templates/default')

sectionName = "Tasks"

@tasks_blueprint.route("/task/<task>")
@refreshToken
@require_login
async def view(task):
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@tasks_blueprint.route("/add")
@refreshToken
@require_role(TasksPermissions.addTaskRole)
async def add():
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@tasks_blueprint.route("/remove")
@refreshToken
@require_role(TasksPermissions.removeTaskRole)
async def remove():
    return await standardReturn("implement.html",sectionName,implement="Implement!")

@tasks_blueprint.route("/edit")
@refreshToken
@require_role(TasksPermissions.editTaskRole)
async def edit():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
