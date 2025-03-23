"""Models"""
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, Integer, DateTime,  PrimaryKeyConstraint
from sqlalchemy import func



class Base(DeclarativeBase):
    """Base model class"""


sub_m2m_teach = Table(
    "sub_m2m_teach",
    Base.metadata,
    Column("subject_id", Integer, ForeignKey("subjects.id", ondelete="CASCADE")),
    Column("teacher_id", Integer, ForeignKey("teachers.id", ondelete="CASCADE")),
    PrimaryKeyConstraint("subject_id", "teacher_id"),
)

class Group(Base):
    """Group"""
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    students: Mapped[list["Student"]] = relationship(back_populates="group", cascade="all, delete")

class Student(Base):
    """Studen class"""
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(default="")
    student_card_number = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="students")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="student")


class Teacher(Base):
    """Studen class"""
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name:Mapped[str] = mapped_column(default="")
    department: Mapped[str] = mapped_column(default="")
    subjects: Mapped[list["Subject"]] = relationship(
        secondary=sub_m2m_teach, back_populates="teachers"
    )


class Subject(Base):
    """Subject"""
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    teachers: Mapped[list["Teacher"]] = relationship(
        secondary=sub_m2m_teach, back_populates="subjects"
    )
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="subject")

class Grade(Base):
    """Grade for students and subjects"""
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(primary_key=True)
    value:  Mapped[float] = mapped_column(default=0)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()  # pylint: disable=not-callable
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    student: Mapped["Student"] = relationship(
        "Student", back_populates="grades"
    )
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    subject: Mapped["Subject"] = relationship(
        "Subject", back_populates="grades"
    )
