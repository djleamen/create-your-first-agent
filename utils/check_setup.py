"""
check_setup.py: run this before the workshop starts.

    python utils/check_setup.py

Every line should say [ OK ]. If one says [FAIL], it tells you what to do,
or flag down a volunteer.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
problems = 0


def ok(message):
    print(f"[ OK ] {message}")


def fail(message, fix):
    global problems
    problems += 1
    print(f"[FAIL] {message}\n       -> {fix}")


# 1. Python version
if sys.version_info >= (3, 9):
    ok(f"Python {sys.version.split()[0]}")
else:
    fail(f"Python {sys.version.split()[0]} is too old", "Install Python 3.9 or newer from https://python.org")

# 2. Packages
missing = []
for package in ("openai", "dotenv"):
    try:
        __import__(package)
    except ImportError:
        missing.append(package)
if missing:
    fail(f"Missing packages: {', '.join(missing)}", "Run: pip install -r requirements.txt")
else:
    ok("Packages installed")

# 3. .env file
if (ROOT / ".env").exists():
    ok(".env file found")
else:
    fail("No .env file", "Copy .env.example to a new file named .env, then paste in your key")

if problems:
    print(f"\n{problems} problem(s) to fix before we can talk to the AI.")
    sys.exit(1)

# 4. Provider + key + a real round trip to the model
sys.path.insert(0, str(ROOT))
from utils.llm import PROVIDER, MODEL, get_client  # noqa: E402

ok(f"Provider: {PROVIDER}, model: {MODEL}")
client = get_client()  # exits with instructions if the key is missing

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Reply with exactly: ready"}],
    )
    reply = (response.choices[0].message.content or "").strip()
    ok(f"The model replied: {reply!r}")
except Exception as error:
    fail(
        f"Couldn't reach the model: {error}",
        "Check your key in .env and your Wi-Fi. A 429 error means wait a minute and retry.",
    )

if problems:
    sys.exit(1)
print("\nYou're all set!")
