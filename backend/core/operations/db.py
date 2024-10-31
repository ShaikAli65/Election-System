# Description: This file contains the database operations for the application.
from itertools import islice

from backend.core.models.poll import Poll, PollStatus

candidates = {
    'candidate_Alice': {
        'id': 'candidate_Alice',
        'name': 'Alice',
        'email': 'alice@gmail.com',
        'age': 30,
        'gender': 'F',
        'port_folio': 'C:\\Users\\7862s\\Desktop\\Election-System\\backend\\database\\alice_portfolio.txt',
        'poll_id': 'P1',
        'vote_count': 100,
    },
    'candidate_Bob': {
        'id': 'candidate_Bob',
        'name': 'Bob',
        'email': 'temp@mail.com',
        'age': 25,
        'gender': 'M',
        'port_folio': 'C:\\Users\\7862s\\Desktop\\Election-System\\backend\\database\\alice_portfolio.txt',
        'poll_id': 'P2',
        'vote_count': 150,
    },
    'candidate_Charlie': {
        'id': 'candidate_Charlie',
        'name': 'Charlie',
        'email': 'charlie@gmail.com',
        'age': 35,
        'gender': 'M',
        'port_folio': 'C:\\Users\\7862s\\Desktop\\Election-System\\backend\\database\\alice_portfolio.txt',
        'poll_id': 'P3',
        'vote_count': 200,
    },
    'candidate_Diana': {
        'id': 'candidate_Diana',
        'name': 'Diana',
        'email': 'diana@gmail.com',
        'age': 28,
        'gender': 'F',
        'port_folio': 'C:\\Users\\7862s\\Desktop\\Election-System\\backend\\database\\alice_portfolio.txt',
        'poll_id': 'P4',
        'vote_count': 250,
    },
    'candidate_Eve': {
        'id': 'candidate_Eve',
        'name': 'Eve',
        'email': 'eve@gmail.com',
        'age': 22,
        'gender': 'F',
        'port_folio': 'C:\\Users\\7862s\\Desktop\\Election-System\\backend\\database\\alice_portfolio.txt',
        'poll_id': 'P5',
        'vote_count': 300,
    },
    'candidate_Frank': {
        'id': 'candidate_Frank',
        'name': 'Frank',
        'email': 'frank@gmail.com',
        'age': 40,
        'gender': 'M',
        'port_folio': 'C:\\Users\\7862s\\Desktop\\Election-System\\backend\\database\\alice_portfolio.txt',
        'poll_id': 'P6',
        'vote_count': 350,
    },
    'candidate_Grace': {
        'id': 'candidate_Grace',
        'name': 'Grace',
        'email': 'grace@gmail.com',
        'age': 27,
        'gender': 'F',
        'port_folio': 'C:\\Users\\7862s\\Desktop\\Election-System\\backend\\database\\alice_portfolio.txt',
        'poll_id': 'P7',
        'vote_count': 400,
    },
    'candidate_Hank': {
        'id': 'candidate_Hank',
        'name': 'Hank',
        'email': 'hank@gmail.com',
        'age': 33,
        'gender': 'M',
        'port_folio': 'C:\\Users\\7862s\\Desktop\\Election-System\\backend\\database\\alice_portfolio.txt',
        'poll_id': 'P8',
        'vote_count': 450,
    },
}

voters = {
    'voter_Alice': {
        'id': 'voter_Alice',
        'name': 'Alice',
        'email': 'alice_voter@gmail.com',
        'age': 30,
        'gender': 'F',
    },
    'voter_Bob': {
        'id': 'voter_Bob',
        'name': 'Bob',
        'email': 'bob_voter@gmail.com',
        'age': 25,
        'gender': 'M',
    },
    'voter_Charlie': {
        'id': 'voter_Charlie',
        'name': 'Charlie',
        'email': 'charlie_voter@gmail.com',
        'age': 35,
        'gender': 'M',
    },
    'voter_Diana': {
        'id': 'voter_Diana',
        'name': 'Diana',
        'email': 'diana_voter@gmail.com',
        'age': 28,
        'gender': 'F',
    },
    'voter_Eve': {
        'id': 'voter_Eve',
        'name': 'Eve',
        'email': 'eve_voter@gmail.com',
        'age': 22,
        'gender': 'F',
    },
    'voter_Frank': {
        'id': 'voter_Frank',
        'name': 'Frank',
        'email': 'frank_voter@gmail.com',
        'age': 40,
        'gender': 'M',
    },
    'voter_Grace': {
        'id': 'voter_Grace',
        'name': 'Grace',
        'email': 'grace_voter@gmail.com',
        'age': 27,
        'gender': 'F',
    },
    'voter_Hank': {
        'id': 'voter_Hank',
        'name': 'Hank',
        'email': 'hank_voter@gmail.com',
        'age': 33,
        'gender': 'M',
    },
    'voter_Ivy': {
        'id': 'voter_Ivy',
        'name': 'Ivy',
        'email': 'ivy_voter@gmail.com',
        'age': 29,
        'gender': 'F',
    },
    'voter_Jack': {
        'id': 'voter_Jack',
        'name': 'Jack',
        'email': 'jack_voter@gmail.com',
        'age': 31,
        'gender': 'M',
    },
}

polls = {
    'P1': {
        'id': 'P1',
        'title': 'Presidential Election',
        'start_time': '2023-01-01T00:00:00Z',
        'end_time': '2023-01-01T23:59:59Z',
        'status': PollStatus.SCHEDULED,
        'candidates': [*islice(candidates.items(), 0, 3)],
        'result': {
            'poll_id': 'P1',
            'result_id': 'R1',
            'winner': candidates['candidate_Alice'],
            'total_votes': 1000,
        },
    },
    'P2': {
        'id': 'P2',
        'title': 'City Mayor Election',
        'start_time': '2023-02-01T00:00:00Z',
        'end_time': '2023-02-01T23:59:59Z',
        'status': PollStatus.ACTIVE,
        'candidates': [*islice(candidates.items(), 3, 5)],
        'result': {
            'poll_id': 'P2',
            'result_id': 'R2',
            'winner': candidates['candidate_Bob'],
            'total_votes': 1500,
        },
    },
    'P3': {
        'id': 'P3',
        'title': 'School Board Election',
        'start_time': '2023-03-01T00:00:00Z',
        'end_time': '2023-03-01T23:59:59Z',
        'status': PollStatus.EXPIRED,
        'candidates': [*islice(candidates.values(), 5, 7)],
        'result': {
            'poll_id': 'P3',
            'result_id': 'R3',
            'winner': candidates['candidate_Charlie'],
            'total_votes': 2000,
        },
    },
}


def create_poll(poll: Poll):
    dumped = poll.model_dump_json()
    polls.update({poll.id: dumped})


def get_candidate(c_id) -> dict:
    candidate = candidates[c_id]

    return candidate.model_dump(exclude=['vote_count', 'port_folio'])

