# Challenges

Finished your agent? Pick any of these. They're roughly in order of difficulty.

## Warm-ups (5–10 minutes)

1. **Give it a personality.** Change `SYSTEM_PROMPT` so your agent is a pirate, a tired grad student, or a hype coach. Does it still use its tools correctly?
2. **Watch it think.** Ask a question that needs two tools, like *"What's the weather in Tokyo, and what's the temperature times 3?"* Count the `[using tool]` lines. Who decided the order?
3. **Break it on purpose.** Set `MAX_STEPS = 1`. What happens to multi-tool questions? Why does the limit exist?

## Build a new tool (15–20 minutes)

Every new tool is the same three moves: **write the function → describe it in `TOOL_SCHEMAS` → add it to `TOOLS`**.

4. **Coin flip / dice roller.** `roll_dice(sides)` using `random.randint`. Ask the agent to settle an argument.
5. **Unit converter.** `convert_km_to_miles(km)`. Then delete it and see if the agent works it out with `calculate` instead.
6. **Notes.** Two tools: `save_note(text)` appends a line to `notes.txt`, and `read_notes()` returns the file. Now your agent remembers things even after you quit!
7. **Course countdown.** `days_until(date)` takes `"2026-12-15"` and returns how many days away it is. Ask *"How many days until my last exam?"* Before you build it, ask your agent *"How many days until December 25?"* and check its answer on a calendar. Using a tool doesn't make every step right, so the agent can still get this wrong!

## Level up (30+ minutes)

8. **Real data.** Find a free API with no key (try [Open Library](https://openlibrary.org/developers/api) for books, or [Frankfurter](https://frankfurter.dev/) for currency rates) and turn it into a tool. `get_weather` in `utils/toolbox.py` shows how to fetch JSON with only the standard library.
9. **Ask before acting.** Make `save_note` ask *"Allow the agent to save this? (y/n)"* with `input()` before it writes. This "human in the loop" check is how real agents stay safe.
10. **Swap the brain.** Change `PROVIDER` in `.env` to `groq`, or install [Ollama](https://ollama.com) to run a model on your own laptop. Your code doesn't change at all. Why not?
11. **A web page.** `pip install gradio`, then wrap `ask_agent` in `gradio.ChatInterface` to get a chat website in about 10 lines.

## Think about it

- The model never runs your code. It only *asks* you to. Why is that design safer?
- What tools would be **dangerous** to give an agent? What rules would you add?
- Where could an agent like this actually help you this semester?
