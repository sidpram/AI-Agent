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

#Send the request to the model
while True:

    user_input = input("\n You : ")

    if user_input.lower() == "quit":
        print("\n AI: Good bye!")
        break

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role":"user",
                "content": user_input
            }
        ]
    )

    # Display the response
    print("AI : ", response.choices[0].message.content)
