from typing import Literal, Union, overload
import uuid
from pipelines.base import Image2ImagePipeline, Model, Pipeline, Text2ImagePipeline
from pipelines.stable_diffusion import StableDiffusion, StableDiffusionText2ImagePipeline

class ModelContainer[M: Model]:
  def __init__(self, model: M):
    self.model: M = model
    self.pipelines: dict[str, Union[
      tuple[Literal['text2image'], Text2ImagePipeline],
      tuple[Literal['image2image'], Image2ImagePipeline],
    ]] = {}

_models: dict[str, ModelContainer] = {}

def load_model(type: str, path: str) -> str:
  id = str(uuid.uuid4())
  match(type):
    case 'stablediffusion':
      _models[id] = ModelContainer(StableDiffusion(path))
    case _:
      raise KeyError(f'unknown model type: {type}')
  return id

def create_pipeline(model_id: str, type: Union[Literal['text2image'], Literal['image2image']]) -> str:
  pipeline_id = str(uuid.uuid4())
  # FIXME
  _models[model_id].pipelines[pipeline_id] = (type, StableDiffusionText2ImagePipeline(_models[model_id].model)) # type: ignore
  return pipeline_id

@overload
def get_pipeline(pipeline_id: str, type: Literal['text2image']) -> Text2ImagePipeline: ...
@overload
def get_pipeline(pipeline_id: str, type: Literal['image2image']) -> Image2ImagePipeline: ...
def get_pipeline(pipeline_id: str, type: str) -> Pipeline:
  pipe = next(
    (container.pipelines[pipeline_id] for container in _models.values() if pipeline_id in container.pipelines),
    None
  )
  if pipe is None:
    raise KeyError(f'non-existent pipeline: {pipeline_id}')
  if pipe[0] != type:
    raise TypeError(f'wrong type ({type}) for pipeline: {pipeline_id}')
  return pipe[1]
