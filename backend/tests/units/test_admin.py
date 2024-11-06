from election.core.contexts.admin import get_admin_context


async def test_admin():
    assert get_admin_context() is None, "Admin not initialized"
