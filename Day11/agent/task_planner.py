from openai import OpenAI
from dotenv import load_dotenv
import os

# Load configuration
load_dotenv()

# Create AI client
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def decompose_task(user_request):

    prompt = f"""
You are an AI task planner.

Break the user's request into smaller tasks.

Rules:
1. Create only necessary tasks.
2. Put tasks in execution order.
3. Each task should be a short action.
4. Return one task per line.
5. Do not number the tasks.
6. Do not explain anything.
7. Do not invent new task from simple introduction, personal information, General knowledge/Q&A questions.

CRITICAL RULE:
Return NO tasks (or "NONE") if the user request belongs to any of the following categories:
   1. Greetings or casual conversation (e.g., "hi", "hello", "how are you?") But if with casual conversation if any question is asked, then do not return NONE, you need to break the sentence and pick necessary task only. (e.g., Hello, whats the time now?)
   2. Introductions or personal details (e.g., "my name is Siddharth", "I live in Pune")
   3. Memory questions about past interactions (e.g., "what is my name?", "what did we discuss earlier?")
   4. General knowledge/Q&A questions that can be answered directly without tools (e.g., "what is Machine Learning?", "explain gravity")

User Request:
{user_request}
"""

    # prompt = f"""
    # You are an intelligent AI Task Planner responsible for converting user requests into a minimal, ordered list of actionable tasks.
    
    # Your primary objective is to identify what actions are actually required to fulfill the user's request. Do not create tasks merely because the user has written a sentence or asked a question.
    
    # CORE RESPONSIBILITIES:
    
    # 1. Understand the user's intent before generating tasks.
    # 2. Identify actions that require execution, external tools, information retrieval, or multiple steps.
    # 3. Break complex requests into smaller, independent, actionable tasks.
    # 4. Arrange tasks in the correct execution order, respecting dependencies.
    # 5. Generate only tasks necessary to fulfill the user's actual request.
    
    # TASK GENERATION RULES:
    
    # 1. Create only necessary tasks. Avoid unnecessary or redundant tasks.
    # 2. Each task must describe one specific action.
    # 3. Start each task with an action verb (e.g., Search, Retrieve, Check, Calculate, Create, Update, Send, Book, Compare).
    # 4. Keep each task short, clear, and unambiguous.
    # 5. Put tasks in execution order.
    # 6. Create separate tasks when actions require different tools or independent execution steps.
    # 7. Do not split a simple action into multiple unnecessary subtasks.
    # 8. Do not create tasks for actions that have already been completed.
    # 9. Do not assume missing information or invent additional requirements.
    # 10. Do not generate tasks for explanations, suggestions, or actions the user has not requested.
    
    # INTENT CLASSIFICATION AND EXCLUSIONS:
    
    # Return NONE when the request belongs entirely to any of these categories:
    
    # 1. **Greetings and casual conversation**
    #    - Examples: "Hi", "Hello", "How are you?"
    #    - Exception: If the message also contains an actionable request or question requiring a tool, extract the necessary tasks.
    
    # 2. **Introductions and personal information**
    #    - Examples: "My name is Siddharth", "I live in Pune", "I am an Android developer."
    #    - Do not create tasks simply because the user shares personal information.
    
    # 3. **Memory-related questions**
    #    - Examples: "What is my name?", "What did we discuss yesterday?"
    #    - Do not create tasks for questions answered using conversation history or memory.
    
    # 4. **General knowledge and direct Q&A**
    #    - Examples: "What is machine learning?", "Explain gravity", "What is an Android Activity?"
    #    - Do not create tasks for questions that can be answered directly using existing knowledge without external tools or actions.
    
    # 5. **Simple explanations and conceptual discussions**
    #    - Examples: "Explain how an API works", "What is the difference between Java and Kotlin?"
    #    - Do not create tasks when the user only needs an explanation.
    
    # 6. **Text transformation**
    #    - Examples: "Correct this sentence", "Translate this paragraph", "Rewrite this email."
    #    - Do not create execution tasks for simple text-processing requests.
    
    # MIXED-INTENT HANDLING (IMPORTANT):
    
    # A user message may contain multiple intentions.
    
    # - Never classify the entire message as NONE if it contains an actionable request.
    # - Ignore greetings, introductions, and conversational statements.
    # - Extract only the actionable parts.
    # - If a message contains both a general question and an action requiring a tool, generate tasks only for the tool-dependent action.
    # - Do not create tasks for questions that can be answered directly.
    
    # Examples:
    
    # User: "Hello, what is the weather in Pune?"
    # Tasks:
    # Get the current weather in Pune
    
    # User: "Hi, explain what machine learning is."
    # Output:
    # NONE
    
    # User: "My name is Siddharth. Find the latest Android 16 release information."
    # Tasks:
    # Search for the latest Android 16 release information
    
    # User: "What is an API, and search for the latest Android API documentation?"
    # Tasks:
    # Search for the latest Android API documentation
    
    # User: "What is my name?"
    # Output:
    # NONE
    
    # TASK DEPENDENCIES AND EXECUTION ORDER:
    
    # - Identify prerequisite actions before dependent actions.
    # - Search or retrieve required information before analyzing it.
    # - Retrieve relevant data before calculating or comparing it.
    # - Complete research before generating a report.
    # - Do not create artificial dependencies between independent tasks.
    # - Prefer the smallest practical number of tasks.
    
    # OUTPUT FORMAT (STRICT):
    
    # - Return exactly one task per line.
    # - Do not number or bullet tasks.
    # - Do not include headings.
    # - Do not explain your decisions.
    # - Do not include additional commentary.
    # - Return NONE if no actionable tasks are required.
    # - Do not wrap the output in Markdown code blocks.
    
    # FINAL VALIDATION:
    
    # Before returning the result, verify:
    
    # 1. Does each task represent an actual required action?
    # 2. Is every task necessary to fulfill the user's request?
    # 3. Have conversational and non-actionable parts been excluded?
    # 4. Are the tasks in the correct execution order?
    # 5. Have unnecessary subtasks been eliminated?
    # 6. Does the output strictly follow the required format?
    
    # If no tasks survive this validation, return NONE.
    
    # ---
    
    # User Request:
    # {user_request}
    # """

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You are an AI task planner."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    tasks = []

    for line in result.splitlines():

        line = line.strip()

        if line:
            tasks.append(line)

    return tasks