from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class NLPPreprocessingConfig:
    root_dir: Path
    status_file: Path
