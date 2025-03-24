"""Create database queries command"""

from connect import session


def new_object(model, **kwargs):
    """Create new object in db"""
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance
