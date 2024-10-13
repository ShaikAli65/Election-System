from . import constants


def get_porfolio_path(poll_id, candidate_id):
    base_path = constants.PORTFOLIOS_PATH
    poll_path = base_path / poll_id
    portfolio_path = poll_path / f"{candidate_id}.pdf"
    portfolio_path.resolve()
    if portfolio_path.is_relative_to(base_path) and portfolio_path.exists():
        return portfolio_path
    else:
        return constants.NA_PORTFOLIO
