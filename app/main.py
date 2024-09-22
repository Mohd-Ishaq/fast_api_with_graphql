from typing import Union

from fastapi import FastAPI
from app.routers import user,auth

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)







#initial hello world api
@app.get("/")
def read_root():
    
    return {"Hello": "World"}