# Build Your First AI Agent

**ACM-W hands-on workshop** · Friday, November 20, 11 AM to 2 PM · SHA024

In one session you'll build a working AI agent from scratch in Python. It can hold a conversation, do maths, tell the time and check the live weather, and it decides on its own which tool to use.

No AI experience needed. If you've written a `for` loop in any language, you're ready.

---

## What's an AI agent?

A normal chatbot can only *talk*. An **agent** can also *do things*: it calls tools (Python functions) to get information or take actions, looks at the results, and decides what to do next, all in a loop until the job is done.

```
You ask a question
      │
      ▼
 ┌──────────┐   "call get_weather('Toronto')"   ┌────────────┐
 │  AI model │ ────────────────────────────────► │ Your Python │
 │  (thinks) │ ◄──────────────────────────────── │  (does)     │
 └──────────┘        "4°C, light rain"           └────────────┘
      │   ...repeats until the model has enough to answer
      ▼
 Final answer
```

---

## Setup (about 10 minutes, ideally before the workshop)

### 1. Install the basics

- **Python 3.9 or newer.** Check by running `python3 --version` (Mac) or `py --version` (Windows). Get it at [python.org/downloads](https://www.python.org/downloads/). On Windows, **tick "Add Python to PATH"** in the installer.
- **A code editor.** [VS Code](https://code.visualstudio.com/) is a good choice.
- **Git** (optional). Without it, use the green **Code → Download ZIP** button on this page instead of `git clone`.

> **Laptop trouble?** Click **Code → Codespaces → Create codespace** on this page. You get a ready-to-go editor in your browser with everything installed (free with a GitHub account). Then skip to step 4.

### 2. Get the code

```bash
git clone <THIS-REPO-URL>
cd create-your-first-agent
```

### 3. Install the packages

**Mac / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

You'll see `(.venv)` at the start of your terminal prompt when it's working. If you open a new terminal later, run the `activate` line again.

> Windows says "running scripts is disabled"? Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer `Y`, and try again.

### 4. Get a free AI key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey) and sign in with a **personal** Google account (school accounts sometimes block it).
2. Click **Create API key** and copy it.
3. Make a copy of `.env.example` and name it `.env`. Paste your key after `GEMINI_API_KEY=`.

```
PROVIDER=gemini
GEMINI_API_KEY=AIza...your-key...
```

> Your key is like a password. `.env` is already ignored by git, so it won't be uploaded. Don't paste your key anywhere else.
>
> Can't use Google? See the backup options inside `.env.example` (Groq is also free).

### 5. Check everything works

```bash
python utils/check_setup.py
```

Every line should say `[ OK ]`. If you're stuck, bring your laptop to the workshop early and a volunteer will help.

---

## Code along

You'll write your agent in **`my_agent.py`**. It runs right now (try `python my_agent.py`), but it can't think yet. The steps run top to bottom through the file, and we'll fill in the TODOs together:

| Step | You'll learn | TODOs in `my_agent.py` | Finished version |
|---|---|---|---|
| 1 | Send a message to an AI model | TODO 1 | `solutions/step1_first_call.py` |
| 2 | Give it memory so it can hold a conversation | TODO 2a, 2b | `solutions/step2_chat_loop.py` |
| 3 | Write tools and describe them to the model | TODO 3a–3d | `solutions/step3_tools.py` |
| 4 | The agent loop: let the model use tools on its own | TODO 4 | `solutions/step4_agent.py` |

**Fell behind? No problem.** Each solution file is `my_agent.py` with every TODO up to that step already done (the later TODOs are still there for you). Copy the matching one over your `my_agent.py` and keep going, or just run it:

```bash
python solutions/step4_agent.py
```

Things to ask your finished agent:
- *What's the weather in Toronto, and what's that in Fahrenheit?*
- *Is it warmer in Tokyo or London right now, and by how much?*
- *If I save $37.50 a week, how much will I have in a year?*

---

## Files

| File | What it is | Edit it? |
|---|---|---|
| `my_agent.py` | **Your agent.** Where you code along | Yes! |
| `solutions/` | `my_agent.py` as it looks after each step | Copy from it |
| `utils/toolbox.py` | Ready-made calculator and weather tools | Peek if curious |
| `utils/llm.py` | Connects to the AI provider | No |
| `utils/check_setup.py` | Checks your setup | No |
| `CHALLENGES.md` | Ideas for after you finish | Yes! |

---

## Troubleshooting

| You see | Try |
|---|---|
| `python: command not found` | Use `python3` (Mac) or `py` (Windows) |
| `No module named 'openai'` | Activate your venv (step 3), then `pip install -r requirements.txt` |
| `No API key found` | Is your file named exactly `.env` (not `.env.txt`)? Is it in the main project folder? |
| `401` or `API key not valid` | Re-copy the key from AI Studio with no spaces or quotes around it |
| `429` or `RESOURCE_EXHAUSTED` | Free tier limit. Wait a minute and try again. Still happening? You've used today's requests for that model (they reset at midnight Pacific): set `MODEL=gemini-3.1-flash-lite` in `.env` |
| Hangs, `503`, or `Request timed out` | That model is overloaded. Set `MODEL=gemini-3.1-flash-lite` in `.env` (or try again later) |
| `404` model not found | Models get renamed. Ask a volunteer, or set `MODEL=` in `.env` to a current one |

---

## Keep going

Finished early, or want more at home? Open **[CHALLENGES.md](CHALLENGES.md)**.

