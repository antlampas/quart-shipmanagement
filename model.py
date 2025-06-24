#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from config                     import DbConfig
from sqlalchemy                 import ForeignKey
from sqlalchemy                 import select
from sqlalchemy                 import text
from sqlalchemy.orm             import Mapped
from sqlalchemy.orm             import mapped_column
from sqlalchemy.orm             import DeclarativeBase
from sqlalchemy.orm             import relationship
from quart_sqlalchemy           import SQLAlchemyConfig
from quart_sqlalchemy.framework import QuartSQLAlchemy

from utilities                  import isAlpha,isNumber,isAlphanumeric

db = QuartSQLAlchemy(
    config=SQLAlchemyConfig(
        binds=dict(
            default=dict(
                engine=dict(
                    url=DbConfig.DATABASEURL,
                    echo=False,
                    connect_args=dict(check_same_thread=False),
                ),
                session=dict(
                    expire_on_commit=False,
                ),
            )
        )
    )
)

class PersonalBaseInformationsTable(db.Model):
    __tablename__ = "PersonalBaseInformations"
    SticMember:    Mapped["STICMembershipTable"] \
                    = relationship(cascade='all,delete',back_populates='Member')
    CrewMember:    Mapped["CrewMemberTable"] \
                    = relationship(cascade='all,delete',back_populates='Member')
    Id:            Mapped[int] \
                    = mapped_column(primary_key=True,autoincrement=True)
    Nickname:      Mapped[str] \
                    = mapped_column(unique=True)
    FirstName:     Mapped[str]
    LastName:      Mapped[str]
class STICMembershipTable(db.Model):
    __tablename__ = "STICMembership"
    Member:     Mapped["PersonalBaseInformationsTable"] \
                = relationship(cascade='all,delete',back_populates='SticMember')
    MemberId:   Mapped[int] \
                = mapped_column(ForeignKey("PersonalBaseInformations.Id"))
    SticSerial: Mapped[int] \
                = mapped_column(primary_key=True)
class CrewMemberTable(db.Model):
    __tablename__ = "CrewMember"
    Member:                     Mapped["PersonalBaseInformationsTable"] \
                = relationship(cascade='all,delete',back_populates='CrewMember')
    Rank:                       Mapped["CrewMemberRankTable"] \
                = relationship(cascade='all,delete',back_populates='Member')
    Division:                   Mapped["CrewMemberDivisionTable"] \
                = relationship(cascade='all,delete',back_populates='Member')
    Duties:                     Mapped[list["CrewMemberDutyTable"]] \
                = relationship(cascade='all,delete',back_populates='Member')
    PersonalBaseInformationsId: Mapped[int] \
                = mapped_column(ForeignKey("PersonalBaseInformations.Id"))
    Serial:                     Mapped[int] \
                = mapped_column(primary_key=True,autoincrement=True)
class DutyTable(db.Model):
    __tablename__ = "Duty"
    CrewMemberDuty: Mapped["CrewMemberDutyTable"] \
                      = relationship(cascade='all,delete',back_populates='Duty')
    Name:           Mapped[str] \
                      = mapped_column(primary_key=True)
    Description:    Mapped[str]
class RankTable(db.Model):
    __tablename__ = "Rank"
    CrewMemberRank: Mapped["CrewMemberRankTable"] \
                      = relationship(cascade='all,delete',back_populates='Rank')
    Name:           Mapped[str] \
                      = mapped_column(primary_key=True)
    Description:    Mapped[str]
class DivisionTable(db.Model):
    __tablename__ = "Division"
    CrewMemberDivision: Mapped["CrewMemberDivisionTable"] \
                  = relationship(cascade='all,delete',back_populates='Division')
    Name:               Mapped[str] \
                  = mapped_column(primary_key=True)
    Description:        Mapped[str]
class CrewMemberRankTable(db.Model):
    __tablename__ = "CrewMemberRank"
    Member:       Mapped["CrewMemberTable"] \
            = relationship(cascade='all,delete',back_populates='Rank')
    Rank:         Mapped["RankTable"] \
            = relationship(cascade='all,delete',back_populates='CrewMemberRank')
    Id:           Mapped[int] \
            = mapped_column(primary_key=True,autoincrement=True)
    RankName:     Mapped[str] \
            = mapped_column(ForeignKey("Rank.Name"))
    MemberSerial: Mapped[int] \
            = mapped_column(ForeignKey("CrewMember.Serial"))
class CrewMemberDutyTable(db.Model):
    __tablename__ = "CrewMemberDuty"
    Member:       Mapped["CrewMemberTable"] \
            = relationship(cascade='all,delete',back_populates='Duties')
    Duty:         Mapped["DutyTable"] \
            = relationship(cascade='all,delete',back_populates='CrewMemberDuty')
    Id:           Mapped[int] \
            = mapped_column(primary_key=True,autoincrement=True)
    DutyName:     Mapped[str] \
            = mapped_column(ForeignKey("Duty.Name"))
    MemberSerial: Mapped[int] \
            = mapped_column(ForeignKey("CrewMember.Serial"))
class CrewMemberDivisionTable(db.Model):
    __tablename__ = "CrewMemberDivision"
    Division:     Mapped["DivisionTable"] \
        = relationship(cascade='all,delete',back_populates='CrewMemberDivision')
    Member:       Mapped["CrewMemberTable"] \
        = relationship(cascade='all,delete',back_populates='Division')
    Id:           Mapped[int] \
        = mapped_column(primary_key=True,autoincrement=True)
    DivisionName: Mapped[str] \
        = mapped_column(ForeignKey("Division.Name"))
    MemberSerial: Mapped[int] \
        = mapped_column(ForeignKey("CrewMember.Serial"))
class TaskTable(db.Model):
    __tablename__    = "Task"
    Mission:          Mapped["MissionTable"] \
                     = relationship(cascade='all,delete',back_populates='Tasks')
    Name:             Mapped[str] \
                     = mapped_column(primary_key=True)
    Description:      Mapped[str]
    Objective:        Mapped[str]
    RequiredDuration: Mapped[str]
    StartedAt:        Mapped[int]
    EndedAt:          Mapped[int]
    Status:           Mapped[str]
class MissionBaseInformationsTable(db.Model):
    __tablename__ = "MissionBaseInformations"
    Mission:          Mapped["MissionTable"] \
   = relationship(cascade='all,delete',back_populates='MissionBaseInformations')
    Name:             Mapped[str] \
   = mapped_column(primary_key=True)
    Description:      Mapped[str]
    RequiredDuration: Mapped[str]
    StartedAt:        Mapped[int]
    EndedAt:          Mapped[int]
    Status:           Mapped[str]
class MissionTable(db.Model):
    __tablename__ = "Mission"
    MissionBaseInformations: Mapped["MissionBaseInformationsTable"] \
                   = relationship(cascade='all,delete',back_populates='Mission')
    Tasks:                   Mapped[list["TaskTable"]]\
                   = relationship(cascade='all,delete',back_populates='Mission')
    Id:                      Mapped[int] \
                   = mapped_column(primary_key=True,autoincrement=True)
    Name:                    Mapped[str] \
                   = mapped_column(ForeignKey("MissionBaseInformations.Name"))
    TaskName:                Mapped[str] \
                   = mapped_column(ForeignKey("Task.Name"))
class MemberDutyLogEntryTable(db.Model):
    __tablename__ = "MemberDutyLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[int] = mapped_column(ForeignKey("CrewMember.Serial"))
    Duty:       Mapped[str] = mapped_column(ForeignKey("Duty.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]
class MemberOnboardLogEntryTable(db.Model):
    __tablename__ = "MemberOnboardLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[int] = mapped_column(ForeignKey("CrewMember.Serial"))
    Period:     Mapped[int]
class MemberRankLogEntryTable(db.Model):
    __tablename__ = "MemberRankLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[int] = mapped_column(ForeignKey("CrewMember.Serial"))
    Rank:       Mapped[str] = mapped_column(ForeignKey("Rank.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]
class MemberDivisionLogEntryTable(db.Model):
    __tablename__ = "MemberDivisionLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[int] = mapped_column(ForeignKey("CrewMember.Serial"))
    Division:   Mapped[str] = mapped_column(ForeignKey("Division.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]
class MemberTaskLogEntryTable(db.Model):
    __tablename__ = "MemberTaskLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[int] = mapped_column(ForeignKey("CrewMember.Serial"))
    Task:       Mapped[str] = mapped_column(ForeignKey("Task.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]
class MemberMissionLogEntryTable(db.Model):
    __tablename__ = "MemberMissionLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[int] = mapped_column(ForeignKey("CrewMember.Serial"))
    Mission:    Mapped[str] = mapped_column(ForeignKey("Mission.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

#### Queries ####
def selectPerson(attribute='',search='',stic=False):
    if attribute                       and \
       search                          and \
       not re.match(isAlpha,attribute) and \
       not re.match(isAlpha,search):
        return None
    elif not attribute or not search:
        if stic:
            return select(
                         PersonalBaseInformationsTable.FirstName.label(
                                                                     'FirstName'
                                                                      ),
                         PersonalBaseInformationsTable.LastName.label(
                                                                      'LastName'
                                                                     ),
                         PersonalBaseInformationsTable.Nickname.label(
                                                                      'Nickname'
                                                                     ),
                         STICMembershipTable.SticSerial.label('STIC')
                         ).join(
                             STICMembershipTable,
                             PersonalBaseInformationsTable.Id == \
                                                    STICMembershipTable.MemberId
                         )
        else:
            return select(
                         PersonalBaseInformationsTable.FirstName.label(
                                                                     'FirstName'
                                                                      ),
                         PersonalBaseInformationsTable.LastName.label(
                                                                      'LastName'
                                                                     ),
                         PersonalBaseInformationsTable.Nickname.label(
                                                                      'Nickname'
                                                                     )
                         )
    else:
        where_clause = f"PersonalBaseInformations.{attribute}='{person}'"
        if stic:
            return select(
                         PersonalBaseInformationsTable.FirstName.label(
                                                                     'FirstName'
                                                                      ),
                         PersonalBaseInformationsTable.LastName.label(
                                                                      'LastName'
                                                                     ),
                         PersonalBaseInformationsTable.Nickname.label(
                                                                      'Nickname'
                                                                     ),
                         STICMembershipTable.SticSerial.label('STIC')
                         ).join(
                             STICMembershipTable,
                             PersonalBaseInformationsTable.Id == \
                                                    STICMembershipTable.MemberId
                         ).where(text(where_clause))
        else:
            return select(
                         PersonalBaseInformationsTable.FirstName.label(
                                                                     'FirstName'
                                                                      ),
                         PersonalBaseInformationsTable.LastName.label(
                                                                      'LastName'
                                                                     ),
                         PersonalBaseInformationsTable.Nickname.label(
                                                                      'Nickname'
                                                                     )
                         ).where(text(where_clause))
def selectCrew(member='',stic=False):
    if not member:
        return select(PersonalBaseInformationsTable)
    else:
        if re.match(isAlpha,member):
            where_clause = f"PersonalBaseInformations.Nickname='{member}'"
            if stic:
                return select(
                         PersonalBaseInformationsTable.FirstName.label(
                                                                     'FirstName'
                                                                      ),
                         PersonalBaseInformationsTable.LastName.label(
                                                                      'LastName'
                                                                     ),
                         PersonalBaseInformationsTable.Nickname.label(
                                                                      'Nickname'
                                                                     ),
                         CrewMemberTable.Serial.label('Serial'),
                         STICMembershipTable.SticSerial.label('STIC'),
                         CrewMemberRankTable.RankName.label('Rank'),
                         CrewMemberDutyTable.DutyName.label('Duties'),
                         CrewMemberDivisionTable.DivisionName.label('Division')
                         ).select_from(PersonalBaseInformationsTable). \
                         join(PersonalBaseInformationsTable.CrewMember). \
                         join(PersonalBaseInformationsTable.SticMember). \
                         join(CrewMemberTable.Rank). \
                         join(CrewMemberTable.Duties). \
                         join(CrewMemberTable.Division). \
                         where(where_clause)
            else:
                return select(
                         PersonalBaseInformationsTable.FirstName.label(
                                                                     'FirstName'
                                                                      ),
                         PersonalBaseInformationsTable.LastName.label(
                                                                      'LastName'
                                                                     ),
                         PersonalBaseInformationsTable.Nickname.label(
                                                                      'Nickname'
                                                                     ),
                         CrewMemberTable.Serial.label('Serial'),
                         CrewMemberRankTable.RankName.label('Rank'),
                         CrewMemberDutyTable.DutyName.label('Duties'),
                         CrewMemberDivisionTable.DivisionName.label('Division')
                         ).select_from(PersonalBaseInformationsTable). \
                         join(PersonalBaseInformationsTable.CrewMember). \
                         join(PersonalBaseInformationsTable.SticMember). \
                         join(CrewMemberTable.Rank). \
                         join(CrewMemberTable.Duties). \
                         join(CrewMemberTable.Division). \
                         where(text(where_clause))
        else:
            return None
def selectRank(rank=''):
    if not rank:
        return select(RankTable)
    else:
        if re.match(isAlpha,rank):
            where_clause = f"Rank.Name='{rank}'"
            return select(RankTable).where(text(where_clause))
        else:
            return None
def selectDuty(duty=''):
    if not duty:
        return select(DutyTable)
    else:
        if re.match(isAlpha,duty):
            where_clause = f"Duty.Name='{duty}'"
            return select(DutyTable).where(text(where_clause))
        else:
            return None
def selectDivision(division=''):
    if not division:
        return select(DivisionTable)
    else:
        if re.match(isAlpha,division):
            where_clause = f"Division.Name='{division}''"
            return select(DivisionTable).where(text(where_clause))
        else:
            return None
def selectMission(mission=''):
    if not mission:
        return select(MissionTable)
    else:
        if re.match(isAlpha,mission):
            where_clause = f"Mission.Name='{mission}''"
            return select(MissionTable).where(text(where_clause))
        else:
            return None
def selectTask(task=''):
    if not task:
        return select(TaskTable)
    else:
        if re.match(isAlpha,task):
            where_clause = f"Task.Name='{task}''"
            return select(TaskTable).where(text(where_clause))
        else:
            return None
#### End queries ####

#### Helper functions ####
def loadFromDB(what='',pattern=''):
    if what == 'person':
        if pattern:
            person           = None
            personDictionary = dict()
            if re.match(isAlpha,pattern):
                with db.bind.Session() as s:
                    with s.begin():
                        person = s.scalar(selectPerson(attribute='nickname',
                                                       search=pattern
                                                      )
                                         )
                personDictionary['FirstName'] = person.FirstName
                personDictionary['LastName']  = person.LastName
                personDictionary['Nickname']  = person.Nickname

                return personDictionary
            else:
                return None
        else:
            return None
    elif what == 'people':
        people           = None
        peopleDictionary = dict()
        if not pattern:
            with db.bind.Session() as s:
                with s.begin():
                    people = s.scalars(selectPerson()).all()
            if people:
                for person in people:
                    peopleDictionary[person.Nickname] = {
                                                 'FirstName' : person.FirstName,
                                                 'LastName'  : person.LastName,
                                                 'Nickname'  : person.Nickname
                                                  }
                return people
            else:
                return None
        else:
            pass
    elif what == 'crewMember':
        if pattern:
            crewMember           = None
            crewMemberDictionary = dict()
            if re.match(isAlpha,pattern):
                with db.bind.Session() as s:
                    with s.begin():
                        crewMember = s.scalar(selectCrew(pattern))
                if crewMember:
                    crewMemberDictionary["FirstName"] = crewMember.FirstName
                    crewMemberDictionary["LastName"]  = crewMember.LastName
                    crewMemberDictionary["Nickname"]  = crewMember.Nickname
                    crewMemberDictionary["Rank"]      = crewMember.Rank
                    crewMemberDictionary["Divison"]   = crewMember.Division
                    crewMemberDictionary["Duties"]    = crewMember.Duties
                    crewMemberDictionary["Serial"]    = crewMember.Serial
                    crewMemberDictionary["Stic"]      = crewMember.Stic

                    return crewMemberDictionary
            else:
                return None
        else:
            return None
    elif what == 'crew':
        crewList       = None
        crewDictionary = dict()
        if not pattern:
            with db.bind.Session() as s:
                with s.begin():
                    crewList = s.scalars(selectCrew()).all()
            if crewList:
                for member in crewList:
                    crewDictionary[member.Nickname] = {
                                                 "FirstName" : member.FirstName,
                                                 "LastName"  : member.LastName,
                                                 "Nickname"  : member.Nickname,
                                                 "Rank"      : member.Rank,
                                                 "Division"  : member.Division,
                                                 "Duties"    : member.Duties,
                                                 "Serial"    : member.Serial,
                                                 "Stic"      : member.Stic,
                                                  }
                return crewDictionary
            else:
                return None
        else:
            pass
    elif what == 'rank':
        if pattern:
            rank           = None
            rankDictionary = dict()
            if re.match(isAlpha,pattern):
                with db.bind.Session() as s:
                    with s.begin():
                        rank = s.scalar(selectRank(pattern))
            if rank:
                rankDictionary['Name']        = rank.Name
                rankDictionary['Description'] = rank.Description

                return rankDictionary
            else:
                return None
        else:
            return None
    elif what == 'ranks':
        ranks           = None
        ranksDictionary = dict()
        if not pattern:
            with db.bind.Session() as s:
                with s.begin():
                    ranks = s.scalars(selectRank()).all()
            if ranks:
                for rank in ranks:
                    ranksDictionary[rank.Name] = {
                                                'Name'        : rank.Name,
                                                'Description' : rank.Description
                                                }
                return ranksDictionary
            else:
                return None
        else:
            pass
    elif what == 'division':
        if pattern:
            division           = None
            divisionDictionary = dict()
            if re.match(isAlpha,pattern):
                with db.bind.Session() as s:
                    with s.begin():
                        division = s.scalar(selectDivision(pattern))
            if division:
                divisionDictionary['Name']        = division.Name
                divisionDictionary['Description'] = division.Description

                return divisionDictionary
            else:
                return None
        else:
            return None
    elif what == 'divisions':
        divisions           = None
        divisionsDictionary = dict()
        with db.bind.Session() as s:
            with s.begin():
                divisions = s.scalars(selectDivision()).all()
        if divisions:
            for division in divisions:
                divisionsDictionary[division.Name] = {
                                              'Name'        : division.Name,
                                              'Description' : division.Name
                                               }
            return divisions
        else:
            return None
    elif what == 'task':
        if pattern:
            task           = None
            taskDictionary = dict()
            if re.match(isAlpha,pattern):
                with db.bind.Session() as s:
                    with s.begin():
                        task = s.scalar(selectTask(pattern))
            if task:
                taskDictionary['Name']        = task.Name
                taskDictionary['Description'] = task.Description

                return taskDictionary
            else:
                return None
        else:
            return None
    elif what == 'tasks':
        tasks           = None
        tasksDictionary = dict()
        with db.bind.Session() as s:
            with s.begin():
                tasks = s.scalars(selectTask()).all()
        if tasks:
            for task in tasks:
                tasksDictionary[task.Name] = {
                                                  'Name'        : task.Name,
                                                  'Description' : task.Name
                                             }
            return tasksDictionary
        else:
            return None
    elif what == 'duty':
        if pattern:
            duty           = None
            dutyDictionary = dict()
            if re.match(isAlpha,pattern):
                with db.bind.Session() as s:
                    with s.begin():
                        duty = s.scalar(selectDuty(pattern))
            if duty:
                dutyDictionary["Name"]        = duty.Name
                dutyDictionary["Description"] = duty.Description

                return dutyDictionary
            else:
                return None
        else:
            return None
    elif what == 'duties':
        duties           = None
        dutiesDictionary = dict()
        if re.match(isAlpha,pattern):
            with db.bind.Session() as s:
                with s.begin():
                    duties = s.scalars(selectDuty()).all()
        if duties:
            for duty in duties:
                dutiesDictionary['Name'] = {
                                            'Name'        : duty.Name,
                                            'Description' : duty.Description
                                           }
            return dutiesDictionary
        else:
            return None
    elif what == 'mission':
        #TODO: implement missing records
        if pattern:
            mission           = None
            missionDictionary = dict()
            if re.match(isAlpha,pattern):
                with db.bind.Session() as s:
                    with s.begin():
                        mission = s.scalar(selectMission(pattern))
            if mission:
                missionDictionary['Name']        = mission.Name
                missionDictionary['Description'] = mission.Description

                return missionDictionary
            else:
                return None
        else:
            return None
    elif what == 'missions':
        #TODO: implement missing records
        missions           = None
        missionsDictionary = dict()
        with db.bind.Session() as s:
            with s.begin():
                missions = s.scalars(selectMission()).all()
        if missions:
            for mission in missions:
                missionsDictionary[mission.Name] = {
                                         'Name'        : mission.Name,
                                         'Description' : mission.Description
                                         }
            return missionsDictionary
        else:
            return None
    else:
        return None
def removeFromDB(what='',pattern=''):
    if what == 'person':
        if 'nickname' in pattern:
            personDB = db.session.scalar(selectPerson(pattern))
            with db.bind.Session() as s:
                with s.begin():
                    s.delete(personDB)
                    s.commit()
            return True
        else:
            return False
    elif what == 'crewMember':
        if 'nickname' in pattern:
            crewMemberDB = db.session.scalar(selectCrew(pattern))
            with db.bind.Session() as s:
                with s.begin():
                    s.delete(crewMemberDB)
                    s.commit()
            return True
        else:
            return False
    elif what == 'task':
        if 'name' in pattern:
            taskDB = db.session.scalar(selectTask(pattern))
            with db.bind.Session() as s:
                with s.begin():
                    s.delete(taskDB)
                    s.commit()
            return True
        else:
            return False
    elif what == 'duty':
        if 'name' in pattern:
            dutyDB = db.session.scalar(selectDuty(pattern))
            with db.bind.Session() as s:
                with s.begin():
                    s.delete(dutyDB)
                    s.commit()
            return True
        else:
            return False
    elif what == 'rank':
        if 'name' in pattern:
            rankDB = db.session.scalar(selectRank(pattern))
            with db.bind.Session() as s:
                with s.begin():
                    s.delete(rankDB)
                    s.commit()
            return True
        else:
            return False
    elif what == 'division':
        if 'name' in pattern:
            divisionDB = db.session.scalar(selectDivision(pattern))
            with db.bind.Session() as s:
                with s.begin():
                    s.delete(divisionDB)
                    s.commit()
            return True
        else:
            return False
def saveToDB(what='',data=dict()):
    #TODO: Check and complete this
    if what == 'crewMember':
        personDB = loadFromDB()
        person   = PersonalBaseInformationsTable(FirstName=data['FirstName'],
                                                 LastName=data['LastName'],
                                                 Nickname=data['Nickname']
                                                )
        with db.bind.Session() as s:
            with s.begin():
                s.add(person)
                s.commit()
        personDB   = db.session.scalar(selectPerson(data['Nickname']))
        crewMember = CrewMemberTable(PersonalBaseInformationsId=personDB.Id,
                                     Serial=data['Serial'])
        with db.bind.Session() as s:
            with s.begin():
                s.add(crewMember)
                s.commit()
        sticMembership = STICMembershipTable(MemberSerial = data['Serial'],
                                             SticSerial   = data['Stic']
                                            )
        memberRank     = CrewMemberRankTable(MemberSerial = ['Serial'],
                                             RankName     = data['Rank']
                                            )
        memberDuty     = CrewMemberDutyTable(MemberSerial = ['Serial'],
                                             DutyName     = data['Duty']
                                            )
        memberDivision = CrewMemberDivisionTable(
                                                MemberSerial = ['Serial'],
                                                DivisionName = data['Division']
                                                )
        with db.bind.Session() as s:
            with s.begin():
                s.add(sticMembership)
                s.add(memberRank)
                s.add(memberDuty)
                s.add(memberDivision)
                s.commit()
        return True
    else:
        return False
def editDB(what='',pattern=dict()):
    if what == 'person':
        if pattern and 'Nickname' in pattern:
            person = db.session.scalar(selectPerson(pattern['Nickname']))
            if person:
                with db.bind.Session() as s:
                    with s.begin():
                        s.commit()
                    return True
            else:
                return False
        else:
            return False
    elif what == 'crewMember':
        if pattern and 'Nickname' in pattern:
            crewMember = db.session.scalar(selectCrew(pattern['Nickname']))
            if crewMember and (pattern.keys() >= {'FirstName',
                                                  'LastName',
                                                  'Rank',
                                                  'Duties',
                                                  'Division',
                                                  'Stic'
                                                  }
                              ):
                crewMember.FirstName = data['FirstName']
                crewMember.LastName  = data['LastName']
                crewMember.Rank      = data['Rank']
                crewMember.Duties    = data['Duties']
                crewMember.Division  = data['Division']
                crewMember.STIC      = data['Stic']
                with db.bind.Session() as s:
                    with s.begin():
                        s.commit()
                return True
            else:
                return False
        else:
            return False
    elif what == 'rank':
        if pattern and 'Name' in pattern:
            rank = db.session.scalar(selectRank(pattern['Name']))
            if rank and 'Description' in pattern:
                rank.Description = pattern['Description']
                with db.bind.Session() as s:
                    with s.begin():
                        s.commit()
                return True
            else:
                return False
        else:
            return False
    elif what == 'division':
        if pattern and 'Name' in pattern:
            division = db.session.scalar(selectDivision(pattern['Name']))
            if division and 'Description' in pattern:
                division.Description = pattern['Description']
                with db.bind.Session() as s:
                    with s.begin():
                        s.commit()
                return True
            else:
                return False
        else:
            return False
    elif what == 'duty':
        if pattern and 'Name' in pattern:
            duty = db.session.scalar(selectDuty(pattern['Name']))
            if duty and 'Description' in pattern:
                duty.Description = pattern['Description']
                with db.bind.Session() as s:
                    with s.begin():
                        s.commit()
                return True
            else:
                return False
        else:
            return False
    elif what == 'mission':
        if pattern and 'Name' in pattern:
            pass
    elif what == 'task':
        if pattern and 'Name' in pattern:
            pass
#### End helper functions ####
