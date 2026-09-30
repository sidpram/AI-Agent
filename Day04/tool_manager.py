from tools import (
    get_current_time, 
    roll_dice, 
    generate_password
)


def get_user_tool(user_text):

    user_text = user_text.lower()
    if "date" in user_text or "time" in user_text or "clock" in user_text:
            return get_current_time()
    
    elif "password" in user_text or "passcode" in user_text or "key" in user_text:
        return generate_password()
    
    elif "dice" in user_text or "die" in user_text:
        return f"you rolled  {roll_dice()}"

    else:
         None