import uuid


def get_unique_id(typeid: type(int) | type(str)):
    return typeid(uuid.uuid4())
