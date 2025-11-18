import sys
from pathlib import Path
import copy
import pytest

CURRENT_FILE = Path(__file__).resolve()

candidate_roots = [
    CURRENT_FILE.parents[0],
    CURRENT_FILE.parents[1],
    CURRENT_FILE.parents[2] if len(CURRENT_FILE.parents) > 2 else None,
]

for cand in candidate_roots:
    if cand and (cand / "travel_planner").exists():
        if str(cand) not in sys.path:
            sys.path.insert(0, str(cand))
        break

from travel_planner.models import create_sample_state, AppState


@pytest.fixture
def sample_state() -> AppState:
    state = create_sample_state()
    return copy.deepcopy(state)


@pytest.fixture
def tmp_storage_path(tmp_path: Path) -> Path:
    return tmp_path / "test_travel_data.json"
