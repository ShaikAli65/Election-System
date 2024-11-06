import asyncio
from datetime import datetime
from functools import partial

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from election.core.contexts.admin import get_admin_context
from election.db.database import AsyncDB, db_session_factory
from election.db.schemas import ElectionSchema, ElectionStatusEnum
from election.repository.poll import PollRepository

_trigger_tasks = []


async def activate_db_timed_triggers():
    global _trigger_tasks
    async_db = AsyncDB(db_session_factory)
    poll_repo = PollRepository(async_db)
    print("activating timed triggers on election polls")

    async with poll_repo.database() as async_session:
        async_session: AsyncSession
        stmt = select(ElectionSchema).where(ElectionSchema.election_status == ElectionStatusEnum.UPCOMING)
        result = await async_session.execute(stmt)
        for poll in result.scalars():
            time_delta = datetime.now() - poll.start_date
            time_to_trigger = time_delta.seconds
            state_ongoing = asyncio.create_task(
                _state_trigger_to_ongoing(
                    time_to_trigger,
                    poll.election_id,
                )
            )
            state_ongoing.add_done_callback(
                # registering a callback (after the poll state is set to ongoing) to finalize poll
                partial(
                    _spawn_election_finalizer,
                    poll.end_date,
                    poll.election_id,
                    _trigger_tasks,
                )
            )

            _trigger_tasks.append(state_ongoing)


async def _state_trigger_to_ongoing(trigger_time_in_secs, election_id):
    await asyncio.sleep(trigger_time_in_secs)

    async_db = AsyncDB(db_session_factory)
    poll_repo = PollRepository(async_db)
    async with poll_repo.database() as async_session:
        async_session: AsyncSession
        await _state_triggerer(async_session, election_id, ElectionStatusEnum.ONGOING)
    print(f"changed state to 'ongoing' for poll : {election_id}")


async def _state_triggerer(async_session, election_id, set_status_to):

    stmt = select(ElectionSchema).where(ElectionSchema.election_id == election_id)
    result = await async_session.execute(stmt)
    a_poll = result.scalar_one()  # no need to catch any errors if poll not found
    a_poll.election_status = set_status_to


def _spawn_election_finalizer(end_datetime, election_id, task_add_list, *_):
    task = asyncio.create_task(
        _state_trigger_to_completed(
            (datetime.now() - end_datetime).seconds,
            election_id
        )
    )
    task_add_list.append(task)


async def _state_trigger_to_completed(trigger_time_in_secs, election_id):
    await asyncio.sleep(trigger_time_in_secs)

    async_db = AsyncDB(db_session_factory)
    poll_repo = PollRepository(async_db)
    async with poll_repo.database() as async_session:
        async_session: AsyncSession
        await _state_triggerer(async_session, election_id, ElectionStatusEnum.COMPLETED)

    print(f"changed state to 'completed' for poll : {election_id}")
    print("preparing results")
    await get_admin_context().prepare_results(election_id)


async def finalize():
    global _trigger_tasks
    for t in _trigger_tasks.copy():
        if t.done():
            continue
        t.cancel("finalizing")
