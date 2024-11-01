# import datetime
# from pathlib import Path
#
# from fastapi import FastAPI
#
# from backend.core.models.poll import CandidateInPoll, PollId, PortFolio, Poll
# from backend.core.models.person import PersonId
#
# p = Path("C:\\Users\\7862s\\Desktop\\Election-System\\database\\portfolios\\notavailable.pdf")
#
# poll_id = PollId(1)
#
# poll = Poll(
#     title="test",
#     type="normal",
#     start_date=datetime.date(2024,12,4),
#     end_date=datetime.date(2024,12,4),
#     candidates=[
#         CandidateInPoll(
#             candidate_id=PersonId("1"),
#             # portfolio=PortFolio(
#             #     portfolio_path=p,
#             #     poll_id=poll_id,
#             #     candidate_id=PersonId("1"),
#             # ),
#         ),
#         CandidateInPoll(
#             candidate_id=PersonId("1"),
#             portfolio=PortFolio(
#                 portfolio_path=p,
#                 poll_id=poll_id,
#                 candidate_id=PersonId("1"),
#             ),
#         ),
#     ]
# )
#
# app = FastAPI()
#
