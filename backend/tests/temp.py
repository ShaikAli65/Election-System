import asyncio

import election.db.schemas  # noqa
from election.main import life_span
from units.test_results import test_results


async def main():
    async with life_span(None) as _:
        # await test_poll_views()
        await test_results('4ac072ed-9778-4569-8a80-5f5eeddb8cde')


if __name__ == '__main__':
    asyncio.run(main())
