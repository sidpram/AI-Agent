from openai import OpenAI
from dotenv import load_dotenv
import os
from tool_manager import get_user_tool, read_text_file
from retriever import load_documents

def embeddings():

    return ""


documents  = load_documents()

embedded = {}

for fileName, content in documents :
    embedded(fileName) = 


embedded = embeddings()


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

#load the configuration 
load_dotenv()

#create a client that communicates with the Ollama 
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key= os.getenv("API_KEY")
)

print("="*40)
print("                 My Assistance ")
print("="*40)

roles = {
    "1": "You are a friendly school teacher. Explain every concept using simple language and real-life examples.",

    "2": "You are a senior Python developer. Explain programming concepts clearly and always include Python examples.",

    "3": "You are an experienced travel guide. Recommend places, food, transportation and travel tips.",

    "4": "You are a motivational coach. Encourage the user and give practical advice with a positive attitude.",

    "5": "You are a professional interviewer. Ask one interview question at a time and provide feedback after each answer."
}


print("\nChoose Your Assistant\n")

print("1. Teacher")
print("2. Python Expert")
print("3. Travel Guide")
print("4. Motivational Coach")
print("5. Interviewer")

choice = input("\nEnter your choice : ")

messages = [
    {
        "role": "system",
        "content": roles.get(
            choice,
            "You are a helpful AI assistant."
        )
    }
]

#Send the request to the model
while True:

    print()
    user_input = input("You : ")

    text = user_input.lower()

    result = ""

    if result:
        print("AI: ", result)
        continue

    messages.append(
        {
            "role":"user",
            "content": user_input
        }
    )

    if user_input.lower() == "quit":
        print("AI: Good bye!")
        break

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        stream=True
    )

    # ai_reply = response.choices[0].message.content
    # # Display the response
    # print("AI : ", ai_reply)

    ai_reply = show_the_response(response)    
    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    # print("="*40)
    # print("                 Conversation History ")
    # for message in messages:
    #     print(f"{message['role'].title()} : {message['content']}")
    #     print("\n")
    # print("="*40)