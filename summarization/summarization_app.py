from fastapi import APIRouter
from pydantic import BaseModel

from integration.integration import load_integration_data
from integration.integration_endpoint import integrationModel
from summarization.text_summarization import lang_chain_app

summarization_app = APIRouter()




@summarization_app.post("/text_summarization")
def summarization(data:integrationModel):
    text = load_integration_data(data.integration_type,
                                 data.path,
                                data.content)
    return lang_chain_app(text)