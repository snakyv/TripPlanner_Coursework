from __future__ import annotations
from pathlib import Path
import json
from typing import Union

from .models import AppState, create_sample_state


def get_default_path() -> Path:
    return Path.cwd() / "travel_data.json"


def load_state(file_path: Union[str, Path, None] = None) -> AppState:
    p = Path(file_path) if file_path else get_default_path()
    if not p.exists():
        return create_sample_state()
    with p.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return AppState.from_dict(raw)


def save_state(state: AppState, file_path: Union[str, Path, None] = None) -> None:
    p = Path(file_path) if file_path else get_default_path()
    with p.open("w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, ensure_ascii=False, indent=4)
