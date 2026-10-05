from openai import OpenAI
from dotenv import load_dotenv
import os
from similarity import cosine_similarity

load_dotenv()

client = OpenAI(
        base_url=os.getenv("BASE_URL"),
        api_key= os.getenv("API_KEY")
    )

def create_embedding(text):
    embedding = client.embeddings.create(
        model= os.getenv("E_MODEL"), 
        input=text
    ).data[0].embedding

    return embedding


# response  =  client.embeddings.create(
#     model= os.getenv("E_MODEL"), 
#     input="Python Programing"
# )

# embedding =  response.data[0].embedding
# print(embedding)
# print(len(embedding))
# print(type(embedding))

# text1 = "Python is a programming language."
# #text2 = "Python is used for software development."
# text2 = "This is my school."

# embedding1 = client.embeddings.create(
#     model= os.getenv("E_MODEL"), 
#     input=text1
# ).data[0].embedding

# embedding2 = client.embeddings.create(
#     model= os.getenv("E_MODEL"), 
#     input=text2
# ).data[0].embedding


# print(len(embedding1))
# print(len(embedding2))

# score =  cosine_similarity(embedding1, embedding2)
# print(score)