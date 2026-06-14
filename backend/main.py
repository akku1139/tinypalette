from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import api
from config import config

app = FastAPI()
app.mount('/api', api.api)
app.mount('/data/outputs/images', StaticFiles(directory=config.path.outputs.images), name='output_images')
# It's also mounted on the development server, but never accessed so no problem
app.mount('/', StaticFiles(directory='../frontend/dist', html=True), name='frontend')
