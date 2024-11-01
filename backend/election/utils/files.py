import shutil

from backend.election.core.constants import get_config


def get_porfolio_path(poll_id, candidate_id):
    base_path = get_config().portfolios_path
    poll_path = base_path / poll_id
    portfolio_path = poll_path / f"{candidate_id}.pdf"
    portfolio_path.resolve()
    if portfolio_path.is_relative_to(base_path) and portfolio_path.exists():
        return portfolio_path
    else:
        return get_config().na_portfolio_path


def generate_portfolio_path(poll_id, candidate_id):
    base_path = get_config().portfolios_path
    poll_path = base_path / poll_id
    portfolio_path = poll_path / f"{candidate_id}.pdf"
    portfolio_path.resolve()
    poll_path.mkdir(parents=True, exist_ok=True)
    print("generated path", type(portfolio_path), portfolio_path, "for", poll_id, candidate_id)
    return portfolio_path


async def save_porfolio(file_path, file_object):
    # file_path
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file_object.file, buffer)

