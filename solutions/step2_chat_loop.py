"""
STEP 2 SOLUTION: Give it a memory
=================================
This is my_agent.py with TODOs 1, 2a and 2b done.

Models don't remember anything between calls. To have a conversation,
WE keep a list of every message and send the whole list each time.

Try it: tell it your name, then ask "what's my name?"

Fell behind? Copy this whole file into my_agent.py and carry on from TODO 3a.
Or just run it:  python solutions/step2_chat_loop.py   (type 'quit' to stop)
"""

import json  # used in Step 4
import os
import sys
from datetime import datetime  # used in Step 3

# Lets this file find the utils/ folder when it's run from inside solutions/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm import get_client, MODEL  # noqa: E402
from utils.toolbox import calculate, get_weather  # noqa: E402

client = get_client()

# Change this to give your agent its own personality!
SYSTEM_PROMPT = (
    "You are a friendly helper at a student coding workshop. Keep answers short. "
    "Use your tools whenever they help, and never guess at maths, times or weather."
)

MAX_STEPS = 5  # Step 4: safety limit so a confused model can't loop forever


# ===========================================================================
# STEP 1: TALK TO AN AI MODEL
# An AI model is like a function: messages in, reply out.
# ===========================================================================

def ask_agent(messages):
    # (You'll come back to this function in Step 4.)
    response = client.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content


# ===========================================================================
# STEP 2: GIVE IT A MEMORY
# The model forgets everything between calls. To hold a conversation, WE keep
# a list of every message and send the whole list each time.
# ===========================================================================

def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Your agent is ready! Type 'quit' to stop.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        try:
            reply = ask_agent(messages)
            print("Agent:", reply, "\n")
            messages.append({"role": "assistant", "content": reply})  # remember what it said
        except Exception as error:  # e.g. no Wi-Fi, or "429" = too many requests
            print(f"(Couldn't reach the model: {error}\n Wait a few seconds and try again.)\n")


# ===========================================================================
# STEP 3: BUILD SOME TOOLS
# A tool is just a Python function. We describe it to the model so it knows
# the tool exists and what inputs it takes.
# ===========================================================================

# TODO 3a: Write a tool called get_current_time() that returns the current date
#          and time as text. Hint: datetime.now().strftime("%A, %B %d %Y, %I:%M %p")


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a maths expression. Use this for ANY arithmetic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "e.g. '(12 * 4) / 3'"},
                },
                "required": ["expression"],
            },
        },
    },
    # TODO 3b: Describe get_current_time here so the model knows it exists.
    #          Copy the block above, change the name and description, and
    #          give it empty parameters: {"type": "object", "properties": {}}
    #
    # TODO 3c (bonus): describe get_weather too. It takes one input: "city".
]

# TODO 3d: Add your new tools to this dictionary: "tool_name": function_name
TOOLS = {"calculate": calculate}

# TODO 3e: The model still can't SEE your tools: you have to send them with
#          every request. Scroll up to ask_agent() and replace its last two
#          lines with:
#
#   response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SCHEMAS)
#   reply = response.choices[0].message
#   if reply.tool_calls:  # the model is asking US to run a tool
#       call = reply.tool_calls[0]
#       return f"(I want to call {call.function.name}({call.function.arguments}), but I can't run tools until Step 4!)"
#   return reply.content
#
#   Then ask "what time is it?" and watch the model ask for your tool.


def run_tool(name, arguments):
    """Run one tool and always return text, even if something goes wrong."""
    if name not in TOOLS:
        return f"Error: there is no tool called {name!r}"
    try:
        return str(TOOLS[name](**arguments))
    except Exception as error:  # send the error back so the model can recover
        return f"Error: {error}"


# ===========================================================================
# STEP 4: THE AGENT LOOP
# This is what turns a chatbot into an agent:
#
#     while the model keeps asking for tools:
#         run the tools
#         send back the results
#     return the model's final answer
#
# TODO 4: Scroll back up to ask_agent() and upgrade it into a loop:
#   - wrap the create(...) call in:  for _ in range(MAX_STEPS):
#   - if reply.tool_calls is empty -> return reply.content (the final answer)
#   - otherwise, instead of returning, save the request with
#       messages.append(reply.model_dump(exclude_none=True)),
#     run each tool with run_tool(...),
#     append each result as {"role": "tool", ...}, and loop again
#   (see solutions/step4_agent.py if you get stuck)
# ===========================================================================


if __name__ == "__main__":
    main()
