from fastapi import FastAPI, Response
from PIL import Image
import io

from pool import get_model, load_model

api = FastAPI(root_path='/api')

@api.get('/load')
# @api.post('/load')
def load(type: str, path: str):
  return { "id": load_model(type, path) }

@api.get('/generate', response_class=Response)
# @api.post('/generate', response_class=Response)
def generate(id: str, prompt: str):
  pipe = get_model(id)
  res = pipe.generate(prompt)
  im = Image.fromarray(res.numpy())
  img_io = io.BytesIO()
  im.save(img_io, format="PNG")
  img_io.seek(0)
  return Response(content=img_io.getvalue(), media_type="image/png")

@api.get('/')
async def root():
  return 'Hello world.'
