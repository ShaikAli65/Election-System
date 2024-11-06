from election.core.contexts.admin import get_admin_context


async def test_results(election_id):
    admin_context = get_admin_context()
    await admin_context.prepare_results(election_id)
