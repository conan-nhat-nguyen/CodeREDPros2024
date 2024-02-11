import json
from openai import OpenAI
from typing import Optional, List
from pydantic import Field
from langchain_core.pydantic_v1 import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain

def extract_to_json(userInput) -> dict:
    client = OpenAI(api_key='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')


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


    llm = ChatOpenAI(openai_api_key="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")

    chain = create_extraction_chain(schema, llm)
    res = chain.run(userInput)


    return res