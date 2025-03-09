from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from integration.integration import load_integration_data
from vault_local import  *


def lang_chain_app(text):
    model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)
    parser = StrOutputParser()
    generic_tempt = "behave like a text summarization tool:"
    prompt = ChatPromptTemplate.from_messages([("system", generic_tempt), ("user", "{text}")])
    chain = prompt | model | parser
    message=chain.invoke({"text": text})
    return message


