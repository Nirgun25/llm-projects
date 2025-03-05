from fastapi import APIRouter
from pydantic import BaseModel

from integration.integration import load_integration_data

integration_app = APIRouter()

class integrationModel(BaseModel):
    integration_type:str
    path:str
    content:str = None


@integration_app.post("/integration")
def integration_endpoint(data:integrationModel):
    return load_integration_data(data)


