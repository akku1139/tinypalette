import uuid
from pipelines.base import Model, Pipeline
from pipelines.stable_diffusion import StableDiffusion, StableDiffusionText2ImagePipeline

class ModelContainer[M: Model]:
  def __init__(self, model: M):
    self.model: M = model
    self.pipelines: dict[str, Pipeline[M]] = {}

_models: dict[str, ModelContainer] = {}

def load_model(type: str, path: str) -> str:
  id = str(uuid.uuid4())
  match(type):
    case 'stablediffusion':
      _models[id] = ModelContainer(StableDiffusion(path))
    case _:
      raise KeyError(f'unknown model type: {type}')
  return id

def create_pipeline(model_id: str) -> str:
  pipeline_id = str(uuid.uuid4())
  # FIXME
  _models[model_id].pipelines[pipeline_id] = StableDiffusionText2ImagePipeline(_models[model_id].model)
  return pipeline_id

def get_pipeline(pipeline_id: str) -> Pipeline:
  return _models[pipeline_id].pipelines[pipeline_id]
