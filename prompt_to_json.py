import json
from openai import OpenAI
from typing import Optional, List
from pydantic import Field
from langchain_core.pydantic_v1 import BaseModel
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from dotenv import dotenv_values

config = dotenv_values(".env")

def extract_to_json(userInput) -> dict[str, any]:


    # class Properties(BaseModel):

    #     departure_name: str
    #     destination_name: str
    #     departure_date: Optional[str]
    #     return_date: Optional[str]

    schema = {
        "properties": {
            "departure": {"type": "string"},
            "destination": {"type": "string"},
            "departure_date": {"type": "string"},
            "return_date": {"type": "string"}
        },
        "required": ["departure", "destination", "departure_date"]
    }


    llm = ChatOpenAI(openai_api_key=config['OPEN_API'], model="gpt-3.5-turbo")

    chain = create_extraction_chain(schema, llm)
    res = chain.invoke(userInput)

    if (type(res['text']) == list) : return res['text'][0]

    return res['text']