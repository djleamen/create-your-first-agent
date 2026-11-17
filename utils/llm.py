"""
utils/llm.py: connects your code to an AI model.

You do NOT need to edit this file during the workshop. It reads your .env
file, picks a provider, and hands back a `client` you can send messages to.

Every provider below speaks the same "OpenAI-compatible" format, so the rest
of the workshop code works no matter which one you choose.
"""

import os
import sys

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv not installed yet; utils/check_setup.py will say so
    pass


PROVIDERS = {
    # Free tier, just needs a Google account. Recommended for the workshop.
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "model": "gemini-3.5-flash-lite",  # free tier: ~500 requests/day (Flash gets only 20)
        "key_env": "GEMINI_API_KEY",
        "get_key": "https://aistudio.google.com/apikey",
    },
    # Free tier, sign up with email or GitHub. Good backup if Gemini is down.
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.3-70b-versatile",
        "key_env": "GROQ_API_KEY",
        "get_key": "https://console.groq.com/keys",
    },
    # Runs on your own laptop, no key or internet needed after the download.
    # Install from https://ollama.com, then run: ollama pull llama3.2
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "model": "llama3.2",
        "key_env": None,
        "get_key": None,
    },
}

PROVIDER = os.getenv("PROVIDER", "gemini").strip().lower()
if PROVIDER not in PROVIDERS:
    sys.exit(
        f"PROVIDER={PROVIDER!r} in your .env is not one of: {', '.join(PROVIDERS)}"
    )

MODEL = os.getenv("MODEL", "").strip() or PROVIDERS[PROVIDER]["model"]


def get_client():
    """Return a client with a `.chat.completions.create(...)` method."""
    settings = PROVIDERS[PROVIDER]

    api_key = "not-needed"
    if settings["key_env"]:
        api_key = os.getenv(settings["key_env"], "").strip()
        if not api_key or api_key.startswith("paste-"):
            sys.exit(
                f"\nNo API key found for {PROVIDER}.\n"
                f"  1. Get a free key at {settings['get_key']}\n"
                f"  2. Paste it into your .env file as {settings['key_env']}=...\n"
                f"  3. Run this again.\n"
            )

    try:
        from openai import OpenAI
    except ImportError:
        sys.exit(
            "\nThe 'openai' package isn't installed.\n"
            "Run:  pip install -r requirements.txt\n"
        )

    # Give up after a minute (with one retry) instead of silently hanging
    # for ~30 minutes when the model is overloaded.
    return OpenAI(api_key=api_key, base_url=settings["base_url"], timeout=60, max_retries=1)
