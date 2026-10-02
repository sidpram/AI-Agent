from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key= os.getenv("API_KEY")
)

response  =  client.embeddings.create(
    model= os.getenv("E_MODEL"), 
    input="Python Programing"
)

embedding =  response.data[0].embedding
print(embedding)
print(len(embedding))
print(type(embedding))