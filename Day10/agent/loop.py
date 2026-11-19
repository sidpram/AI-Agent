from state import (
    create_state,
    add_task,
    add_action,
    record_observation,
    add_result,
    complete_task, 
    next_step,
    can_continue,
    finish
)

from task_planner import decompose_task

async def run_agent_loop(
    user_request,
    planner,
    execute_action,
    format_answer,
    tools,
    client
):

    state = create_state(user_request)

    # break the user request to smaller task
    planned_tasks = decompose_task(user_request)

    # Now add these planned task 

    for task in planned_tasks:
        add_task(state, task)

    print("\nTask Planned")
    for item in state["tasks"]:
        print("-", item["task"], "- status", item["status"])

# While can_continue: "This is the heart of our agent."

    while can_continue(state):
#The planner decides what to do next.

        action = planner(state, tools)

        print("Planner Selected:", action)

        if action == "FINISH":
            answer = format_answer(state)
            finish(state, answer)
            break
# We execute that action.

        observation = await execute_action(
            action,
            client
        )
# We add that action in state

        add_action(
            state,
            action
        )
#    	We remember what happened.

        record_observation(
            state,
            action,
            observation
        )
#	We move to the next iteration.
     

        next_step(state)

    return state
