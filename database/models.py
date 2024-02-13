from datetime import time
from enum import Enum
from typing import Annotated

from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class Studio(Base):
    __tablename__ = 'studios'

    id: Mapped[intpk]
    name: Mapped[str]

    groups: Mapped[list['Group']] = relationship(back_populates='studio')
    individual_lesson: Mapped['IndividualLesson'] = relationship(
        back_populates='studio'
    )


class WeekDays(Enum):
    monday = 'Понедельник'
    tuesday = 'Вторник'
    wednesday = 'Среда'
    thursday = 'Четверг'
    friday = 'Пятница'
    saturday = 'Суббота'
    sunday = 'Воскресенье'


class Schedule(Base):
    __tablename__ = 'schedules'

    id: Mapped[intpk]
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    start_time: Mapped[time]
    start_date: Mapped[WeekDays]

    group: Mapped['Group'] = relationship(back_populates='schedules')


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[intpk]
    name: Mapped[str]
    studio_id: Mapped[int] = mapped_column(ForeignKey('studios.id'))

    studio: Mapped['Studio'] = relationship(back_populates='groups')
    schedules: Mapped[list['Schedule']] = relationship(back_populates='group')
    students: Mapped[list['Student']] = relationship(
        secondary='student_group_association',
        back_populates='groups'
    )


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[intpk]
    name: Mapped[str]
    age: Mapped[int]
    individual_lesson_id: Mapped[int | None] = mapped_column(
        ForeignKey('individual_lessons.id')
    )

    individual_lesson: Mapped['IndividualLesson'] = relationship(
        back_populates='students'
    )
    groups: Mapped[list['Group']] = relationship(
        secondary='student_group_association',
        back_populates='students'
    )


class IndividualLesson(Base):
    __tablename__ = 'individual_lessons'

    id: Mapped[intpk]
    start_time: Mapped[time]
    start_date: Mapped[WeekDays]
    studio_id: Mapped[int] = mapped_column(ForeignKey('studios.id'))

    students: Mapped[list['Student']] = relationship(
        back_populates='individual_lesson'
    )
    studio: Mapped['Studio'] = relationship(back_populates='individual_lesson')


student_group_association = Table(
    'student_group_association',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('group_id', ForeignKey('groups.id'), nullable=False),
    Column('student_id', ForeignKey('students.id'), nullable=False),
    UniqueConstraint('group_id', 'student_id', name='idx_unique_group_student')
)