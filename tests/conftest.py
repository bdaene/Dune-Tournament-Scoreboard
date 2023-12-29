import pytest

from dune_tournament_scoreboard.services import database


@pytest.fixture
def temporary_data_root(tmp_path):
    old_data_root = database.tournament.DATA_ROOT
    try:
        database.tournament.DATA_ROOT = tmp_path
        yield
    finally:
        database.tournament.DATA_ROOT = old_data_root
