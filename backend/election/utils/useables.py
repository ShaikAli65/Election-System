import uuid


def get_unique_id(typeid: type(int) | type(str) = None):
    _uuid = uuid.uuid4()
    if typeid:
        _uuid = typeid(_uuid)
    return _uuid
