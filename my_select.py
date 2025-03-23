"""All select functions"""

from helpers import call
from connect import session
from models import Group, Student, Teacher, Subject, Grade
from sqlalchemy import select


def select_1():
    q = (
        session.execute(
            select(
                Student.id,
                Student.first_name,
                Student.last_name,
                Student.student_card_number,
                Grade.value
            ).join(Grade).order_by(Grade.value.desc())
            .limit(5)
        ).mappings().all()
    )
    print(q)
    return q


def select_2(subject_name = "In Answer"):
    q = (
        session.execute(
            select(
                Student.id,
                Student.first_name,
                Student.last_name,
                Student.student_card_number,
                Grade.value,
                Subject.name
            ).join(Grade).join(Subject)
            .filter(Subject.name == subject_name)
        ).mappings().all()
    )
    print(q)
    return q


def select_3():
    pass


def select_all():
    for i in range(1, 3):
        func_name = f"select_{i}"
        print(("#"* 25)," " ,func_name, " ",  ("#" * 25))
        globals()[func_name]()


if __name__ == "__main__":
    select_all()
    session.close()