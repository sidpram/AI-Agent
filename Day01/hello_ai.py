from openai import OpenAI
from dotenv import load_dotenv
import os


#load the configuration 
load_dotenv()


#create a client that communicates with the Ollama 
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key= os.getenv("API_KEY")
)

#Send the request to the model
response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {
            "role":"user",
            "content": "What is Artificial Intelligence?"
        }
    ]
)

# Display the response
print(response.choices[0].message.content)
