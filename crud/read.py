"""Filtering and list db records"""

from connect import session


def list_objects(model, columns_name, **filters):
    """List object in DB"""
    columns = [getattr(model, col_name, None) for col_name in columns_name]
    q = session.query(*columns).filter_by(**filters).all()
    return q
