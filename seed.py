"""Create fake data in db"""

from datetime import datetime, timedelta
from faker import Faker
from connect import session
from models import Group, Student, Teacher, Subject, Grade
from helpers import call

fake = Faker()


def make_fake_group() -> Group:
    """
    name
    """
    group_name = fake.company()
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
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    teachers: Mapped[list["Teacher"]] = relationship(
        secondary=sub_m2m_teach, back_populates="subjects"
    )

    """
    fake_subject = f"{fake.word().capitalize()} {fake.word().capitalize()}"
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
    std1, std2, std3 = make_fake_student(), make_fake_student(), make_fake_student()
    group = make_fake_group()
    teacher = make_fake_teacher()
    sub1, sub2 = make_fake_subject(), make_fake_subject()
    group.students = [std1, std2, std3]

    session.add(group)
    teacher.subjects = [sub1, sub2]
    session.add(teacher)
    session.add_all([sub1, sub2])
    session.commit()
    session.add_all(
        [
            make_fake_grade(std1, sub1),
            make_fake_grade(std2, sub1),
            make_fake_grade(std3, sub1),
            make_fake_grade(std1, sub2),
            make_fake_grade(std2, sub2),
            make_fake_grade(std3, sub2),
        ]
    )


if __name__ == "__main__":
    call(fake_all, 100)
    session.commit()
    session.close()
