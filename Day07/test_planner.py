from planner import choose_tool
from tools import generate_password, get_current_time, roll_dice

print("AI: Hello, How can I help you?")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("AI: Good Bye, Have a nice day.")
        break

    
    result = choose_tool(user_input.lower())

    print(result)

    if result == "generate_password":
        print("AI:", generate_password())
    elif result == "get_current_time":
        print("AI:", get_current_time())
    elif result == "roll_dice" :
        print("AI:",  roll_dice())
    else:
        print("No tool found!")