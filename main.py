from fastapi import FastAPI

from handlers import routers


app = FastAPI()

[app.include_router(router) for router in routers]

