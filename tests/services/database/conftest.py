import shutil

import pytest

from dune_tournament_scoreboard.services.database.tournament import DATA_ROOT


@pytest.fixture
def clean_data():
    shutil.rmtree(DATA_ROOT)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
