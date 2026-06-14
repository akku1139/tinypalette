import os
from pathlib import Path
from pydantic import BaseModel

CONFIG_DIR = Path.home() / ".config" / "tinypalette"
CONFIG_FILE_PATH = CONFIG_DIR / "config.json"

class Config(BaseModel):
  class PathConfig(BaseModel):
    class ModelsConfig(BaseModel):
      stablediffusion: Path
    models: ModelsConfig

    class OutputsConfig(BaseModel):
      image: Path
    outputs: OutputsConfig

  path: PathConfig

config = Config.model_validate_json(CONFIG_FILE_PATH.read_text(encoding="utf-8"))

os.makedirs(config.path.models.stablediffusion, exist_ok=True)
os.makedirs(config.path.outputs.image, exist_ok=True)
