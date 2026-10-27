from openai import OpenAI
from dotenv import load_dotenv
import os

from planner import choose_tool

from tools import (
    get_current_time,
    roll_dice,
    generate_password
)

# Load configuration
load_dotenv()

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


# Create AI client
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

print("=" * 40)
print("      My AI Assistant")
print("=" * 40)

print("AI: Hello, How can I help you?")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("AI: Good Bye, Have a nice day.")
        break

    
    tool = choose_tool(user_input.lower())

    print(tool)
    result = ""
    if tool == "generate_password":
        result = (generate_password())
    elif tool == "get_current_time":
        result = (get_current_time())
    elif tool == "roll_dice" :
        result =  (roll_dice())
    else:
        result = None

    if result != None :
        # create prompt
        prompt = f"""
        The user asked:
        {user_input}
        The tool returned:
        {result}
        Answer the user naturally.don't add anything from your side in the answer. if tool is none, then answer it from LLM model.
        """

        response = client.chat.completions.create(
        
                model=os.getenv("MODEL"),
        
                messages=[
                    {
                    "role":"user",
                    "content":prompt
                    }
                    ], 
                    stream=True
                    )
        #print("\nAI :", response.choices[0].message.content) 
        show_the_response(response)


