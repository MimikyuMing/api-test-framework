from pathlib import Path
import yaml

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_yaml(filename):
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
