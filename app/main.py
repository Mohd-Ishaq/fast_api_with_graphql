from typing import Union

from fastapi import FastAPI
from app.routers import user,auth,task


app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(task.graphql_app)









#initial hello world api
@app.get("/")
def read_root():
    
    return {"Hello": "World"}