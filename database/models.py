from datetime import time
from enum import Enum
from typing import Annotated, Type, TypeVar
from pydantic import BaseModel

from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base


intpk = Annotated[int, mapped_column(primary_key=True)]
NameStr = Annotated[str, mapped_column(String(50))]
SchemaResponse = TypeVar('SchemaResponse', bound=BaseModel)


class WeekDays(Enum):
    monday = 'Понедельник'
    tuesday = 'Вторник'
    wednesday = 'Среда'
    thursday = 'Четверг'
    friday = 'Пятница'
    saturday = 'Суббота'
    sunday = 'Воскресенье'


class UserRoles(Enum):
    VISITOR = 'visitor'
    STUDENT = 'student'
    TEACHER = 'teacher'
    OWNER = 'owner'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        autoincrement=False
    )
    username: Mapped[str] = mapped_column(String(50), unique=True)
    role: Mapped[UserRoles]

    def to_read_model(self, schema: Type[SchemaResponse]) -> SchemaResponse:
        return schema(
            id=self.id,
            username=self.username,
            role=self.role
        )


class Studio(Base):
    __tablename__ = 'studios'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50), unique=True)

    groups: Mapped[list['Group']] = relationship(
        back_populates='studio',
        lazy='selectin',
        cascade='all, delete'
    )

    def to_read_model(self, schema: Type[SchemaResponse]) -> SchemaResponse:
        return schema(
            id=self.id,
            name=self.name
        )


class Schedule(Base):
    __tablename__ = 'schedules'

    id: Mapped[intpk]
    group_id: Mapped[int] = mapped_column(
        ForeignKey('groups.id')
    )
    start_time: Mapped[time]
    start_date: Mapped[WeekDays]

    group: Mapped['Group'] = relationship(back_populates='schedules')

    def to_read_model(self, schema: Type[SchemaResponse]) -> SchemaResponse:
        return schema(
            id=self.id,
            group_id=self.group_id,
            start_time=self.start_time,
            start_date=self.start_date
        )


class Group(Base):
    __tablename__ = 'groups'
    __table_args__ = (
        UniqueConstraint('name', 'studio_id', 'is_individual'),
    )

    id: Mapped[intpk]
    is_individual: Mapped[bool]
    name: Mapped[NameStr]
    notes: Mapped[str | None]
    studio_id: Mapped[int] = mapped_column(
        ForeignKey('studios.id')
    )

    studio: Mapped['Studio'] = relationship(back_populates='groups')
    schedules: Mapped[list['Schedule']] = relationship(
        back_populates='group',
        cascade='all, delete'
    )
    students: Mapped[list['Student']] = relationship(
        secondary='student_group_association',
        back_populates='groups'
    )

    def to_read_model(self, schema: Type[SchemaResponse]) -> SchemaResponse:
        return schema(
            id=self.id,
            name=self.name,
            notes=self.notes,
            studio_id=self.studio_id,
            is_individual=self.is_individual
        )


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[intpk]
    name: Mapped[NameStr]
    notes: Mapped[str | None]

    groups: Mapped[list['Group']] = relationship(
        secondary='student_group_association',
        back_populates='students'
    )

    def to_read_model(self, schema: Type[SchemaResponse]) -> SchemaResponse:
        return schema(
            id=self.id,
            name=self.name,
            notes=self.notes
        )


student_group_association = Table(
    'student_group_association',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column(
        'group_id',
        ForeignKey('groups.id', ondelete='CASCADE'),
        nullable=False
    ),
    Column(
        'student_id',
        ForeignKey('students.id', ondelete='CASCADE'),
        nullable=False
    ),
    UniqueConstraint('group_id', 'student_id')
)
