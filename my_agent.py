"""
MY FIRST AI AGENT
=================
This is YOUR file. We'll fill in the TODOs together, top to bottom:

    STEP 1  Talk to an AI model        TODO 1
    STEP 2  Give it a memory           TODO 2a, 2b
    STEP 3  Build some tools           TODO 3a, 3b, 3c, 3d, 3e
    STEP 4  The agent loop             TODO 4

    Run it:   python my_agent.py      (type 'quit' to stop)

It runs right now, even before you change anything. It just can't think yet.
Fell behind? Each step's finished code is in the solutions/ folder:
copy it in here, or just run that file to catch up.
"""

import json
from datetime import datetime

from utils.llm import get_client, MODEL
from utils.toolbox import calculate, get_weather

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
    # TODO 1: Send the messages to the model and return its reply. Replace
    #         the return line at the bottom of this function with:
    #
    #   response = client.chat.completions.create(model=MODEL, messages=messages)
    #   return response.choices[0].message.content
    #
    # (You'll come back to this function in Step 4.)

    return "(I can't think yet. Finish TODO 1!)"


# ===========================================================================
# STEP 2: GIVE IT A MEMORY
# The model forgets everything between calls. To hold a conversation, WE keep
# a list of every message and send the whole list each time.
# ===========================================================================

def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # TODO 2a: Right now you only get one question. Wrap the lines below in
    #          a `while True:` loop, and `break` when the user types 'quit'.
    user_input = input("You: ").strip()
    messages.append({"role": "user", "content": user_input})
    try:
        reply = ask_agent(messages)
        print("Agent:", reply, "\n")
        # TODO 2b: Remember the reply by adding it to the list:
        #          messages.append({"role": "assistant", "content": reply})
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
