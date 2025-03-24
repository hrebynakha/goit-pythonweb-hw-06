"""Delete object in database"""

from connect import session


def delete_object(
    model,
    object_id,
) -> None:
    """Delete object in DB"""

    instance = session.query(model).filter_by(id=object_id).first()
    if not instance:
        raise KeyError("Not found object in DB.")

    session.delete(instance)
    session.commit()
