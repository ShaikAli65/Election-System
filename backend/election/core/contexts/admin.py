from core.models.user import CandidateFromAdmin


class AdminContext:

    def __init__(self):
        ...

    async def add_candidate(self, candidate:CandidateFromAdmin):
        ...


def get_admin_context() -> AdminContext:
    ...
