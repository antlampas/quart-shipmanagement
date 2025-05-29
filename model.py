#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re

from config                     import BaseConfig as Config
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
                    url=Config.DATABASEURL,
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
    Member: Mapped["CrewMemberTable"] = relationship(cascade='all,delete',back_populates='PersonalBaseInformations')
    Id:         Mapped[int]           = mapped_column(primary_key=True,autoincrement=True)
    Nickname:   Mapped[str]           = mapped_column(unique=True)
    FirstName:  Mapped[int]
    LastName:   Mapped[str]

class CrewMemberTable(db.Model):
    __tablename__ = "CrewMember"
    PersonalBaseInformations:   Mapped["PersonalBaseInformationsTable"] = relationship(cascade='all,delete',back_populates='Member')
    Rank:                       Mapped["CrewMemberRankTable"]           = relationship(cascade='all,delete',back_populates='Member')
    Division:                   Mapped["CrewMemberDivisionTable"]       = relationship(cascade='all,delete',back_populates='Member')
    Duties:                     Mapped[list["CrewMemberDutyTable"]]     = relationship(cascade='all,delete',back_populates='Member')
    SticMembership:             Mapped["STICMembershipTable"]           = relationship(cascade='all,delete',back_populates='Member')
    PersonalBaseInformationsId: Mapped[int]                             = mapped_column(ForeignKey("PersonalBaseInformations.Id"))
    Serial:                     Mapped[int]                             = mapped_column(primary_key=True,autoincrement=True)

class DutyTable(db.Model):
    __tablename__ = "Duty"
    CrewMemberDuty: Mapped["CrewMemberDutyTable"] = relationship(cascade='all,delete',back_populates='Duty')
    Name:           Mapped[str] = mapped_column(primary_key=True)
    Description:    Mapped[str]

class RankTable(db.Model):
    __tablename__ = "Rank"
    CrewMemberRank: Mapped["CrewMemberRankTable"] = relationship(cascade='all,delete',back_populates='Rank')
    Name:           Mapped[str]                   = mapped_column(primary_key=True)
    Description:    Mapped[str]

class DivisionTable(db.Model):
    __tablename__ = "Division"
    CrewMemberDivision:          Mapped["CrewMemberDivisionTable"] = relationship(cascade='all,delete',back_populates='Division')
    Name:                        Mapped[str]                       = mapped_column(primary_key=True)
    Description:                 Mapped[str]

class STICMembershipTable(db.Model):
    __tablename__ = "STICMembership"
    Member:       Mapped["CrewMemberTable"] = relationship(cascade='all,delete',back_populates='SticMembership')
    MemberSerial: Mapped[int]               = mapped_column(ForeignKey("CrewMember.Serial"))
    SticSerial:   Mapped[int]               = mapped_column(primary_key=True)

class CrewMemberRankTable(db.Model):
    __tablename__ = "CrewMemberRank"
    Member:       Mapped["CrewMemberTable"] = relationship(cascade='all,delete',back_populates='Rank')
    Rank:         Mapped["RankTable"]       = relationship(cascade='all,delete',back_populates='CrewMemberRank')
    Id:           Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    RankName:     Mapped[str]               = mapped_column(ForeignKey("Rank.Name"))
    MemberSerial: Mapped[int]               = mapped_column(ForeignKey("CrewMember.Serial"))

class CrewMemberDutyTable(db.Model):
    __tablename__ = "CrewMemberDuty"
    Member:       Mapped["CrewMemberTable"] = relationship(cascade='all,delete',back_populates='Duties')
    Duty:         Mapped["DutyTable"]       = relationship(cascade='all,delete',back_populates='CrewMemberDuty')
    Id:           Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    DutyName:     Mapped[str]               = mapped_column(ForeignKey("Duty.Name"))
    MemberSerial: Mapped[int]               = mapped_column(ForeignKey("CrewMember.Serial"))

class CrewMemberDivisionTable(db.Model):
    __tablename__ = "CrewMemberDivision"
    Division:     Mapped["DivisionTable"]   = relationship(cascade='all,delete',back_populates='CrewMemberDivision')
    Member:       Mapped["CrewMemberTable"] = relationship(cascade='all,delete',back_populates='Division')
    Id:           Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    DivisionName: Mapped[str]               = mapped_column(ForeignKey("Division.Name"))
    MemberSerial: Mapped[int]               = mapped_column(ForeignKey("CrewMember.Serial"))

class TaskTable(db.Model):
    __tablename__ = "Task"
    Mission:          Mapped["MissionTable"] = relationship(cascade='all,delete',back_populates='Tasks')
    Name:             Mapped[str]            = mapped_column(primary_key=True)
    Description:      Mapped[str]
    Objective:        Mapped[str]
    RequiredDuration: Mapped[str]
    StartedAt:        Mapped[int]
    EndedAt:          Mapped[int]
    Status:           Mapped[str]

class MissionBaseInformationsTable(db.Model):
    __tablename__ = "MissionBaseInformations"
    Mission:          Mapped["MissionTable"] = relationship(cascade='all,delete',back_populates='MissionBaseInformations')
    Name:             Mapped[str]            = mapped_column(primary_key=True)
    Description:      Mapped[str]
    RequiredDuration: Mapped[str]
    StartedAt:        Mapped[int]
    EndedAt:          Mapped[int]
    Status:           Mapped[str]

class MissionTable(db.Model):
    __tablename__ = "Mission"
    MissionBaseInformations: Mapped["MissionBaseInformationsTable"] = relationship(cascade='all,delete',back_populates='Mission')
    Tasks:    Mapped[list["TaskTable"]] = relationship(cascade='all,delete',back_populates='Mission')
    Id:       Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    Name:     Mapped[str] = mapped_column(ForeignKey("MissionBaseInformations.Name"))
    TaskName: Mapped[str] = mapped_column(ForeignKey("Task.Name"))

class MemberDutyLogEntryTable(db.Model):
    __tablename__ = "MemberDutyLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Serial"))
    Duty:       Mapped[str] = mapped_column(ForeignKey("Duty.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberOnboardLogEntryTable(db.Model):
    __tablename__ = "MemberOnboardLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Serial"))
    Period:     Mapped[int]

class MemberRankLogEntryTable(db.Model):
    __tablename__ = "MemberRankLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Serial"))
    Rank:       Mapped[str] = mapped_column(ForeignKey("Rank.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberDivisionLogEntryTable(db.Model):
    __tablename__ = "MemberDivisionLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Serial"))
    Division:   Mapped[str] = mapped_column(ForeignKey("Division.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberTaskLogEntryTable(db.Model):
    __tablename__ = "MemberTaskLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Serial"))
    Task:       Mapped[str] = mapped_column(ForeignKey("Task.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberMissionLogEntryTable(db.Model):
    __tablename__ = "MemberMissionLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Serial"))
    Mission:    Mapped[str] = mapped_column(ForeignKey("Mission.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

db.create_all()

#### Queries ####
def selectCrew(member=""):
    if member == "":
        return select(PersonalBaseInformationsTable)
    else:
        where_clause = f"PersonalBaseInformations.Nickname='{member}'"
        return select(
            PersonalBaseInformationsTable.FirstName.label('FirstName'),
            PersonalBaseInformationsTable.LastName.label('LastName'),
            PersonalBaseInformationsTable.Nickname.label('Nickname'),
            CrewMemberTable.Serial.label('Serial'),
            STICMembershipTable.SticSerial.label('STIC'),
            CrewMemberRankTable.RankName.label('Rank'),
            CrewMemberDutyTable.DutyName.label('Duties'),
            CrewMemberDivisionTable.DivisionName.label('Division')
        ).join(
            CrewMemberTable,
            PersonalBaseInformationsTable.Id == CrewMemberTable.PersonalBaseInformationsId
        ).join(
            CrewMemberRankTable,
            CrewMemberTable.Serial == CrewMemberRankTable.MemberSerial
        ).join(
            CrewMemberDutyTable,
            CrewMemberTable.Serial == CrewMemberDutyTable.MemberSerial
        ).join(
            CrewMemberDivisionTable,
            CrewMemberTable.Serial == CrewMemberDivisionTable.MemberSerial
        ).join(
            STICMembershipTable,
            CrewMemberTable.Serial == STICMembershipTable.MemberSerial
        ).where(text(where_clause))

def selectPerson(person=""):
    if person == "":
        return None
    else:
        where_clause = f"PersonalBaseInformations.Nickname='{person}'"
        return select(PersonalBaseInformationsTable).where(text(where_clause))

def selectPeople(attribute="",search=""):
    if not attribute or not search:
        return None
    else:
        return select(
            PersonalBaseInformationsTable.FirstName.label('FirstName'),
            PersonalBaseInformationsTable.LastName.label('LastName'),
            PersonalBaseInformationsTable.Nickname.label('Nickname'),
            CrewMemberTable.Serial.label('Serial'),
            STICMembershipTable.SticSerial.label('STIC'),
            CrewMemberRankTable.RankName.label('Rank'),
            CrewMemberDutyTable.DutyName.label('Duties'),
            CrewMemberDivisionTable.DivisionName.label('Division')
        ).join(
            CrewMemberTable,
            PersonalBaseInformationsTable.Id == CrewMemberTable.PersonalBaseInformationsId
        ).join(
            CrewMemberRankTable,
            CrewMemberTable.Serial == CrewMemberRankTable.MemberSerial
        ).join(
            CrewMemberDutyTable,
            CrewMemberTable.Serial == CrewMemberDutyTable.MemberSerial
        ).join(
            CrewMemberDivisionTable,
            CrewMemberTable.Serial == CrewMemberDivisionTable.MemberSerial
        ).join(
            STICMembershipTable,
            CrewMemberTable.Serial == STICMembershipTable.MemberSerial
        ).where(text(f'{attribute}={search}'))

def selectRank(rank=""):
    if rank == "":
        return select(RankTable)
    else:
        where_clause = f"Rank.Name='{rank}'"
        return select(RankTable).where(text(where_clause))

def selectDuty(duty=""):
    if duty == "":
        return select(DutyTable)
    else:
        where_clause = f"Duty.Name='{duty}'"
        return select(DutyTable).where(text(where_clause))

def selectDivision(division=""):
    if division == "":
        return select(DivisionTable)
    else:
        where_clause = f"Division.Name='{division}''"
        return select(DivisionTable).where(text(where_clause))

def selectMission(mission=""):
    if mission == "":
        return select(MissionTable)
    else:
        where_clause = f"Mission.Name='{mission}''"
        return select(MissionTable).where(text(where_clause))

def selectTask(task=""):
    if task == "":
        return select(TaskTable)
    else:
        where_clause = f"Task.Name='{task}''"
        return select(TaskTable).where(text(where_clause))
#### End queries ####

#### Helper functions ####
def loadFromDB(what="",pattern=""):
    if what == "crewMember":
        crewMember = None
        if re.match(isAlpha,pattern):
            with db.bind.Session() as s:
                with s.begin():
                    crewMember = s.scalar(selectCrew(pattern))
        else:
            return crewMember
    elif what == "crew":
        crew = list()
        with db.bind.Session() as s:
            with s.begin():
                crewDB = s.scalars(selectCrew())
                if crewDB:
                    for member in crewDB:
                        DBmember = CreMember(FirstName = crewDB.FirstName
                                             LastName  = crewDB.LastName
                                             Rank      = crewDB.Rank
                                             Division  = crewDB.Division
                                             Duties    = crewDB.Duties
                                             Serial    = crewDB.Serial
                                             Stic      = crewDB.Stic
                                            )
                        crew.append(DBmember)
        return crew
    else:
        return None
def saveToDB():
    pass
#### End helper functions ####
