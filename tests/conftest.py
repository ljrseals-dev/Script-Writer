from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
@pytest.fixture(scope="session")
def sample_scene():return (ROOT/"examples"/"sample_scene.txt").read_text(encoding="utf-8")
