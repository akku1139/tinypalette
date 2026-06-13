from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import api

app = FastAPI()
app.mount('/api', api.api)
app.mount('/', StaticFiles(directory='../frontend/dist', html=True), name='frontend')
