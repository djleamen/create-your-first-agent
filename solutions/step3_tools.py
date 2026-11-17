"""
STEP 3 SOLUTION: Build some tools
=================================
This is my_agent.py with TODOs 1 to 3d done.

A tool is just a Python function. We describe it to the model (name, what it
does, what inputs it takes). The model can't run code itself, so instead it
REPLIES with "please call this tool with these inputs", and we run it.

Try it: ask "what time is it?" The model still can't check, because we only
hand it the tools in Step 4.

Fell behind? Copy this whole file into my_agent.py and carry on from TODO 4.
Or just run it:  python solutions/step3_tools.py   (type 'quit' to stop)
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

def get_current_time():
    """Return the current date and time on this laptop."""
    return datetime.now().strftime("%A, %B %d %Y, %I:%M %p")


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
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g. 'Toronto'"},
                },
                "required": ["city"],
            },
        },
    },
]

# Map each tool's name to the real Python function.
TOOLS = {"calculate": calculate, "get_current_time": get_current_time, "get_weather": get_weather}


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
# TODO 4: Scroll back up to ask_agent() from Step 1 and upgrade it:
#   - add tools=TOOL_SCHEMAS to the create(...) call
#   - wrap the call in:  for _ in range(MAX_STEPS):
#   - reply = response.choices[0].message
#   - if reply.tool_calls is empty -> return reply.content (the final answer)
#   - otherwise save the request with
#       messages.append(reply.model_dump(exclude_none=True)),
#     run each tool with run_tool(...),
#     append each result as {"role": "tool", ...}, and loop again
#   (see solutions/step4_agent.py if you get stuck)
# ===========================================================================


if __name__ == "__main__":
    main()
