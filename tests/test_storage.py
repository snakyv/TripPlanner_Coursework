from travel_planner.storage import save_state, load_state
from travel_planner.models import AppState
from pathlib import Path


def test_save_and_load_roundtrip(sample_state: AppState, tmp_storage_path: Path):
    save_state(sample_state, tmp_storage_path)
    assert tmp_storage_path.exists()

    loaded = load_state(tmp_storage_path)
    assert isinstance(loaded, AppState)

    assert loaded.to_dict() == sample_state.to_dict()
