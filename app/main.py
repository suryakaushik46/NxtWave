from fastapi import FastAPI
from .routers import rider,user,requester
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from app import models
from fastapi_pagination import  add_pagination

app=FastAPI()

#list of urls that can talk to our api if * every thing can talk to our domain
origins=["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#including all the routers
app.include_router(rider.router)
app.include_router(user.router)
app.include_router(requester.router)
#adding the ablity to create tables if not present in db
models.Base.metadata.create_all(bind=engine)
#adding pagination
add_pagination(app)

 # path operation
@app.get("/")
async def root():
    return {"message":"Hello world !!"}