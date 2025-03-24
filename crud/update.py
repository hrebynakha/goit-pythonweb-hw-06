"""Updating instance in DB"""

from connect import session


def update_object(model, object_id, **new_values):
    """Update object in DB"""

    instance = session.query(model).filter_by(id=object_id).first()
    if not instance:
        raise KeyError("Not found object in DB.")

    for key, value in new_values.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
        else:
            raise AttributeError(f"'{model.__name__}' not has key'{key}'")
    session.commit()
    return instance
