from election.core.contexts.admin import get_admin_context


async def test_poll_views():
    _admin_context = get_admin_context()
    list_of_polls = []

    async for poll_view in _admin_context.get_poll_views():
        list_of_polls.append(poll_view)
        print(poll_view)

    return list_of_polls
