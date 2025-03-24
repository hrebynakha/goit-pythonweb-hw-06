"""Create fake data in db"""

from datetime import datetime, timedelta
import random
from faker import Faker
from connect import session
from models import Group, Student, Teacher, Subject, Grade
from helpers import call

fake = Faker()


def make_fake_group() -> Group:
    """
    name
    """
    group_name = f"Group: {fake.company()}"
    group = Group(name=group_name)

    return group


def make_fake_student() -> Student:
    """

    first_name
    last_name
    student_card_number

    """

    student = Student(first_name=fake.first_name(), last_name=fake.last_name())
    return student


def make_fake_teacher() -> Teacher:
    """
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name:Mapped[str] = mapped_column(default="")
    department: Mapped[str] = mapped_column(default="")

    """
    fake_company_department = f"{fake.company()} - {fake.word().capitalize()}"
    teacher = Teacher(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        department=fake_company_department,
    )
    return teacher


def make_fake_subject() -> Subject:
    """
    name:
    teachers: Mapped[list["Teacher"]] = relationship(
        secondary=sub_m2m_teach, back_populates="subjects"
    )

    """
    fake_subject = f"Subject: {fake.word().capitalize()} {fake.word().capitalize()}"
    subject = Subject(name=fake_subject)
    return subject


def make_fake_grade(std, sub) -> Grade:
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    value:  Mapped[float] = mapped_column(default=0)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()  # pylint: disable=not-callable
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))


    """
    default_range = datetime.now() - timedelta(days=2 * 365)  # 2 years ago
    fake_date = fake.date_between(start_date=default_range, end_date="today")
    fake_grade = fake.pyfloat(
        left_digits=2, right_digits=2, positive=True, min_value=60, max_value=100
    )
    return Grade(value=fake_grade, created_date=fake_date, student=std, subject=sub)


def fake_all():
    """Make fake case"""
    students = call(make_fake_student, 15)
    group = make_fake_group()
    group.students = students
    session.add(group)
    teacher = call(make_fake_teacher, 2)
    session.add_all(teacher)
    subjects = call(make_fake_subject, 3)
    session.add_all(subjects)
    session.commit()


def add_fake_grades():
    """Adding random fake grades"""
    students = session.query(Student).all()
    subjects = session.query(Subject).all()

    for student in students:
        for subject in subjects:
            if random.choices([True, False]):
                session.add(make_fake_grade(student, subject))
    session.commit()


def add_fake_rel_sub_teacher():
    """Add fake rel with subjects for teacher"""
    teachers = session.query(Teacher).all()
    subjects = session.query(Subject).all()

    for subject in subjects:
        if random.choices([True, False]):
            teachers_list = [teachers[random.randint(0, len(teachers) - 1)]]
            subject.teachers = teachers_list
    session.commit()


if __name__ == "__main__":
    call(fake_all, 3)
    call(add_fake_grades, 10)
    call(add_fake_rel_sub_teacher, 2)
    session.close()
