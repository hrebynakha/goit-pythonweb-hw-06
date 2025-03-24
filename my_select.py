"""All select functions"""

from connect import session
from models import Group, Student, Teacher, Subject, Grade, sub_m2m_teach
from sqlalchemy.sql import func
from sqlalchemy import select
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()],
)
logging.getLogger().setLevel(logging.INFO)
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def select_1():
    """Query 1"""
    q = (
        session.query(Student.first_name, Student.last_name, func.avg(Grade.value))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .limit(5)
        .all()
    )
    logging.info("Query 1 result:%s", q)
    return q


def select_2(subject_id=1):
    """Query 2"""
    q = (
        session.query(Student.first_name, Student.last_name, func.avg(Grade.value))
        .join(Grade)
        .join(Subject)
        .filter(Subject.id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .first()
    )
    logging.info("Query 2 result:%s", q)
    return q


def select_3(subject_id=1):
    """Query 3"""
    q = (
        session.query(Group.name, func.avg(Grade.value))
        .select_from(Student)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Subject.id == subject_id)
        .group_by(Group.id)
        .order_by(func.avg(Grade.value).desc())
        .all()
    )
    logging.info("Query 3 result:%s", q)
    return q


def select_4():
    """Query 4"""
    q = session.query(func.avg(Grade.value)).first()
    logging.info("Query 4 result:%s", q)
    return q


def select_5(teacher_id=1):
    """Query 5"""
    q = (
        session.query(Subject.id, Subject.name)
        .select_from(sub_m2m_teach)
        .join(Teacher)
        .join(
            Subject,
        )
        .filter(Teacher.id == teacher_id)
        .order_by(Subject.id)
        .all()
    )
    logging.info("Query 5 result:%s", q)
    return q


def select_6(group_id=1):
    """Query 6"""
    q = (
        session.query(Student.id, Student.first_name, Student.last_name)
        .join(Group)
        .filter(Group.id == group_id)
        .order_by(Student.id)
        .limit(10)
        .all()
    )
    logging.info("Query 6 result:%s", q)
    return q


def select_7(group_id=1, subject_id=1):
    """Query 7"""
    q = (
        session.query(
            Student.id, Student.first_name, Student.last_name, Grade.value, Subject.name
        )
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.id == group_id)
        .filter(Subject.id == subject_id)
        .order_by(Student.id)
        .limit(10)
        .all()
    )
    logging.info("Query 7 result:%s", q)
    return q


def select_8(teacher_id=1):
    """Query 8"""
    q = (
        session.query(Subject.id, Subject.name, func.avg(Grade.value))
        .select_from(sub_m2m_teach)
        .join(Teacher)
        .join(Subject)
        .join(Grade)
        .filter(Teacher.id == teacher_id)
        .group_by(Subject.id)
        .order_by(func.avg(Grade.value).desc())
        .all()
    )
    logging.info("Query 8 result:%s", q)
    return q


def select_9(student_id=1):
    """Query 9"""
    q = (
        session.query(Subject.id, Subject.name)
        .select_from(Grade)
        .distinct(Subject.id)
        .join(Subject)
        .join(Student)
        .filter(Student.id == student_id)
        .all()
    )
    logging.info("Query 9 result:%s", q)
    return q


def select_10(student_id=1, teacher_id=1):
    """Query 10"""
    q = (
        session.query(Subject.id, Subject.name, Student.id, Teacher.id)
        .select_from(Grade)
        .distinct(Subject.id)
        .join(Subject)
        .join(Student)
        .join(sub_m2m_teach)
        .join(Teacher)
        .filter(Student.id == student_id)
        .filter(Teacher.id == teacher_id)
        .all()
    )
    logging.info("Query 10 result:%s", q)
    return q


def select_11(student_id=1, teacher_id=1):
    """Query 11"""
    q = (
        session.query(func.avg(Grade.value))
        .select_from(Grade)
        .join(Subject)
        .join(Student)
        .join(sub_m2m_teach)
        .join(Teacher)
        .filter(Student.id == student_id)
        .filter(Teacher.id == teacher_id)
        .first()
    )
    logging.info("Query 11 result:%s", q)
    return q


def select_12(group_id=1, subject_id=1):
    """Query 12"""
    lates_lesson = (
        select(func.max(Grade.created_date))
        .select_from(Grade)
        .join(Subject)
        .join(Student)
        .join(Group)
        .filter(Subject.id == subject_id)
        .filter(Group.id == group_id)
        .scalar_subquery()
    )
    q = (
        session.query(
            Grade.value,
            Grade.created_date,
            Group.id,
            Group.name,
            Student.first_name,
            Student.last_name,
        )
        .select_from(Grade)
        .join(Subject)
        .join(Student)
        .join(Group)
        .filter(Subject.id == subject_id)
        .filter(Group.id == group_id)
        .filter(Grade.created_date == lates_lesson)
        .all()
    )
    logging.info("Query 12 result:%s", q)
    return q


def select_all():
    """Main select function"""
    for i in range(1, 13):
        func_name = f"select_{i}"
        print(("#" * 25), " ", func_name, " ", ("#" * 25))
        globals()[func_name]()


if __name__ == "__main__":
    select_all()
    session.close()
