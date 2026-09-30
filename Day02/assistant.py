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

print("="*40)
print("                 My Assistance ")
print("="*40)

messages = []
#Send the request to the model
while True:

    user_input = input("\n You : ")

    messages.append(
        {
            "role":"user",
            "content": user_input
        }
    )

    if user_input.lower() == "quit":
        print("\n AI: Good bye!")
        break

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )

    ai_reply = response.choices[0].message.content

    # Display the response
    print("AI : ", ai_reply)

    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    print("="*40)
    print("                 Conversation History ")
    for message in messages:
        print(f"{message['role'].title()} : {message['content']}")
        print("\n")
    print("="*40)