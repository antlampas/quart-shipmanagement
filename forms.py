#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from quart_wtf          import QuartForm
from wtforms            import StringField
from wtforms            import PasswordField
from wtforms            import SelectField
from wtforms            import SelectMultipleField
from wtforms            import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.widgets    import PasswordInput

class AddCrewMemberForm(QuartForm):
    FirstName        = StringField('First name')
    LastName         = StringField('Last Name')
    Nickname         = StringField('Nickname')
    Rank             = SelectField('Rank')
    Division         = SelectField('Division')
    Duties           = SelectMultipleField('Duties')

class RemoveCrewMemberForm(QuartForm):
    Nickname         = SelectMultipleField('Member')

class EditCrewMemberForm(QuartForm):
    FirstName        = StringField('First name')
    LastName         = StringField('Last Name')
    Rank             = SelectField('Rank')
    Division         = SelectField('Division')
    Duties           = SelectMultipleField('Duties')

class AddTaskForm(QuartForm):
    Name             = StringField('Task')
    Description      = StringField('Description')
    Objective        = StringField('Objective')
    RequiredDuration = StringField('Required Duration')
    StartedAt        = StringField('Started At')
    EndedAt          = StringField('Ended At')
    Status           = StringField('Status')

class RemoveTaskForm(QuartForm):
    Name             = SelectMultipleField('Task')

class EditTaskForm(QuartForm):
    Name             = StringField('Task')
    Description      = StringField('Description')
    Objective        = StringField('Objective')
    RequiredDuration = StringField('Required Duration')
    StartedAt        = StringField('Started At')
    EndedAt          = StringField('Ended At')
    Status           = StringField('Status')

class AddMissionForm(QuartForm):
    Name             = StringField('Mission')
    Description      = StringField('Description')
    RequiredDuration = StringField('Required Duration')
    StartedAt        = StringField('Started At')
    EndedAt          = StringField('Ended At')
    Tasks            = SelectMultipleField('Tasks')
    Status           = StringField('Status')

class RemoveMissionForm(QuartForm):
    Name             = SelectMultipleField('Mission')

class EditMissionForm(QuartForm):
    Name             = StringField('Mission')
    Description      = StringField('Description')
    RequiredDuration = StringField('Required Duration')
    StartedAt        = StringField('Started At')
    EndedAt          = StringField('Ended At')
    Tasks            = SelectMultipleField('Tasks')
    Status           = StringField('Status')

class AddRankForm(QuartForm):
    Name        = StringField('Name')
    Description = StringField('Description')

class EditRankForm(QuartForm):
    Name        = StringField('Name')
    Description = StringField('Description')

class RemoveRankForm(QuartForm):
    Name = SelectMultipleField('Name')

class AddDutyForm(QuartForm):
    Name        = StringField('Name')
    Description = StringField('Description')

class EditDutyForm(QuartForm):
    Name        = StringField('Name')
    Description = StringField('Description')

class RemoveDutyForm(QuartForm):
    Name = SelectMultipleField('Name')

class AddDivisionForm(QuartForm):
    Name        = StringField('Name')
    Description = StringField('Description')

class EditDivisionForm(QuartForm):
    Name        = StringField('Name')
    Description = StringField('Description')

class RemoveDivisionForm(QuartForm):
    Name = SelectMultipleField('Name')
