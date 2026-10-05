from openai import OpenAI
from dotenv import load_dotenv
import os
from retriever import load_documents
from test_embedding import create_embedding
from similarity import cosine_similarity

#load the configuration 
load_dotenv()


# 1. First load all the documents
documents  = load_documents()

# 2. Generate embedding for all the documents
document_embedding = {}

for fileName, content in documents.items(         ) :
    document_embedding[fileName] = create_embedding(content)

# Prints the AI output
def show_the_response(response):
    ai_reply = ""    
    print("AI: ", end="", flush=True)

    for chunk in response:

        content = chunk.choices[0].delta.content

        if content:
            print(content, end="", flush=True)
            ai_reply += content

    print()
    return ai_reply

#create a client that communicates with the Ollama 
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key= os.getenv("API_KEY")
)

print("="*40)
print("                 My Assistance ")
print("="*40)

while True:

    print()
    user_input = input("You : ")

    text = user_input.lower()
    if text == "quit":
        print("AI: Good bye!")
        break

    # Generate embedded vector for user question

    question_embedding  = create_embedding(text)

    # Now loop each document embedding to search the similarity 

    best_file = ""
    best_score = -1

    for fileName, embedding in document_embedding.items():

        score = cosine_similarity( embedding, question_embedding)

        if score > best_score:
            best_score = score
            best_file = fileName


    # now we know the content:
    context  = documents[best_file]

    prompt = f"""
        Answer the question using only
        the following information.
        Context:
        {context}
        Question:
        {user_input}
    """

    messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        stream=True
    )

    ai_reply = show_the_response(response)    
    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )