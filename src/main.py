from fastapi import FastAPI

from src.api.api import api_router
from src.routes import redirect_router


app = FastAPI()
app.include_router(router=redirect_router)
app.include_router(router=api_router, prefix='/api')
