"""
STEP 4 SOLUTION: The agent loop
===============================
This is my_agent.py with every TODO done: the finished agent!

This is the whole idea of an AI agent:

    while the model keeps asking for tools:
        run the tools
        send back the results
    return the model's final answer

The model decides which tools to use, in what order, and when it's done.
We just keep the loop running. Combined with Step 2's memory, you have an agent.

Try:  "What's the weather in Toronto, and what's that in Fahrenheit?"
      "Is it warmer in Tokyo or London right now, and by how much?"

Fell behind? Copy this whole file into my_agent.py, then try CHALLENGES.md.
Or just run it:  python solutions/step4_agent.py   (type 'quit' to stop)
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
    # Step 4 upgraded this function into the agent loop.
    for _ in range(MAX_STEPS):
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SCHEMAS)
        reply = response.choices[0].message

        # No tool requests means the model is done: that's the final answer.
        if not reply.tool_calls:
            return reply.content

        # Otherwise, save the request exactly as the model sent it (Gemini needs
        # its hidden "thought signature" back), run every tool, and loop again.
        messages.append(reply.model_dump(exclude_none=True))
        for call in reply.tool_calls:
            arguments = json.loads(call.function.arguments or "{}")
            print(f"  [using tool] {call.function.name}({arguments})")
            result = run_tool(call.function.name, arguments)
            print(f"  [tool result] {result}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

    return "Sorry, I hit my step limit before finishing. Try a simpler question?"


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
# Done! ask_agent() at the top of this file now runs this loop. The model
# decides which tools to use, in what order, and when it's finished.
# ===========================================================================


if __name__ == "__main__":
    main()
