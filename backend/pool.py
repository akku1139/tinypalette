import uuid

from pipelines.base import Pipeline
from pipelines.stable_diffusion import StableDiffusionPipeline

_pool: dict[str, Pipeline] = {}

def load_model(type: str, path: str) -> str:
  id = str(uuid.uuid4())
  match(type):
    case 'stablediffusion':
      pipe = StableDiffusionPipeline()
    case _:
      raise KeyError(f'unknown pipeline type: {type}')

  pipe.load(path)
  _pool[id] = pipe
  return id

def get_model(id: str) -> Pipeline:
  return _pool[id]
