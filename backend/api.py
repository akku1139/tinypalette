from fastapi import FastAPI, Response
from PIL import Image
import io
from pydantic import BaseModel

from config import config
from pool import create_pipeline, get_pipeline, load_model

api = FastAPI(root_path='/api')

@api.get('/list_models/stablediffusion')
def list_models_stablediffusion():
  return list(config.path.models.stablediffusion.rglob("*.safetensors"))

class LoadData(BaseModel):
  type: str
  path: str

@api.post('/load')
def load(data: LoadData):
  return { "model_id": load_model(data.type, data.path) }

class CreatePipelineData(BaseModel):
  model_id: str
  type: str

@api.post('/create_pipeline')
def cp(data: CreatePipelineData):
  return { "pipeline_id": create_pipeline(data.model_id) }

class GenerateData(BaseModel):
  pipeline_id: str
  prompt: str

@api.post('/generate', response_class=Response)
def generate(data: GenerateData):
  pipe = get_pipeline(data.pipeline_id)
  res = pipe.generate(data.prompt)
  im = Image.fromarray(res.numpy())
  img_io = io.BytesIO()
  im.save(img_io, format="PNG")
  img_io.seek(0)
  return Response(content=img_io.getvalue(), media_type="image/png")

@api.get('/')
async def root():
  return 'Hello world.'
