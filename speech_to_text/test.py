from openai import OpenAI
import langchain_openai
import langchain
import faiss
from llama_index import LlamaIndex
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
import os
import json
from llama_index.indices.service_context import ServiceContext
from llama_index.llms import OpenAI
from llama_index.indices.struct_store import JSONQueryEngine

f = open(r"C:\Users\LENOVO\Desktop\VS Projects\New folder\g.json")
 
# returns JSON object as 
# a dictionary
json_schema = json.load(f)

os.environ["OPENAI_API_KEY"] = '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'

import requests

# Define the API endpoint URL
departure_id = "IAH"
destination_id = "JFK"
departure_id = "2024-05-02"
endpoint_url = "https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={departure_id}&destinationLocationCode={destination_id}&departureDate={departure_date}&adults=1&max=2"
token_flight = "uc1w8WOBh3A2l9AKo8F6IsoPAX8n"

headers_flight = {"Authorization" : "Bearer " + token_flight}

# Make a GET request to the API endpoint
response = requests.get(endpoint_url, headers=headers_flight)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Extract and process the relevant data
    # (e.g., access 'data' field in the JSON response)
    print(data['data'])
else:
    # Handle errors or non-200 status codes
    print("Error:", response.status_code)

# llm = OpenAI(model="gpt-3.5-turbo")
# service_context = ServiceContext.from_defaults(llm=llm)
# nl_query_engine = JSONQueryEngine(
#     json_value=data,
#     json_schema=json_schema,
#     service_context=service_context,
# )

# Chat Bot

class Chatbot:
    def __init__(self, api_key, index):
        self.index = index
        OpenAI.api_key = api_key
        self.chat_history = []

    def generate_response(self, user_input):
        prompt = "\n".join([f"{message['role']}: {message['content']}" 
                           for message in self.chat_history[-5:]])
        prompt += f"\nUser: {user_input}"
        query_engine = self.index.as_query_engine()
        response = query_engine.query(user_input)

        message = {"role": "assistant", "content": response.response}
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append(message)
        return message

    def load_chat_history(self, filename):
        try:
            with open(filename, 'r') as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            pass

    def save_chat_history(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.chat_history, f)

bot = Chatbot("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", index=index)
bot.load_chat_history("chat_history.json")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "goodbye"]:
        print("Bot: Goodbye!")
        bot.save_chat_history("chat_history.json")
        break
    response = bot.generate_response(user_input)
    print(f"Bot: {response['content']}")