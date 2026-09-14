"""
config.py - every setting for the AI Image Studio, in one place.

Why does this file exist at all? Because settings that are scattered through a program are
settings you can't find. When you want to change the model, or the quality, or where images
get saved, you should know exactly which file to open - and it should be this one.

Nothing in here does any work. It just holds decisions.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Read the .env file so that our API key is available to the libraries that need it.
# override=True means "re-read the file even if something was loaded before" - without it,
# editing .env and re-running would quietly keep using the old value.
load_dotenv(override=True)


# ---------------------------------------------------------------------------
# Which AI model to use
# ---------------------------------------------------------------------------
# This one string decides which company's model we talk to. The format is
# "provider:model-name". Change it and the whole program follows - none of the other
# files mention any provider by name.
#
# Other options (each needs its own package installed, and its own key in .env,
# except Ollama which runs on this computer and needs neither):
#
#   CHAT_MODEL = "anthropic:claude-haiku-4-5-20251001"   # pip install langchain-anthropic
#   CHAT_MODEL = "google-genai:gemini-2.5-flash"         # pip install langchain-google-genai
#   CHAT_MODEL = "ollama:llama3.2"                       # pip install langchain-ollama
#
# NOTE: the provider you pick has to be able to *draw*, not just write. Ollama and most
# text-only models can improve prompts perfectly well but cannot generate images - see
# the table at the end of Session 5.
CHAT_MODEL = "openai:gpt-4.1-mini"


# ---------------------------------------------------------------------------
# Image settings
# ---------------------------------------------------------------------------
# "low" is fast and cheap and is the right choice while you're experimenting.
# Switch to "medium" or "high" for images you actually want to keep.
IMAGE_QUALITY = "low"

# The shapes we offer, in words, so that nobody has to remember pixel numbers.
SIZES = {
    "square": "1024x1024",
    "wide": "1536x1024",
    "tall": "1024x1536",
}

DEFAULT_SIZE = "square"
DEFAULT_STYLE = "photo"


# ---------------------------------------------------------------------------
# Where images are saved
# ---------------------------------------------------------------------------
# Path(__file__) is this file. .parent is the folder it lives in. So the gallery is
# always next to the code, no matter which folder you happened to run the program from.
GALLERY_DIR = Path(__file__).parent / "gallery"


# ---------------------------------------------------------------------------
# A friendly check that we have a key at all
# ---------------------------------------------------------------------------
# Every other file imports this one, so this runs before anything else can go wrong.
# Without it, a missing key produces about forty lines of library traceback ending in
# something like "api_key must be set" - technically true, completely unhelpful.
#
# One clear sentence is worth a great deal when you're thirteen and it's 6pm.

# Which environment variable does the provider we chose need?
# Ollama runs on this computer, so it needs nothing.
KEY_FOR_PROVIDER = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google-genai": "GOOGLE_API_KEY",
    "ollama": None,
}

PROVIDER = CHAT_MODEL.split(":")[0]
REQUIRED_KEY = KEY_FOR_PROVIDER.get(PROVIDER, "OPENAI_API_KEY")

if REQUIRED_KEY and not os.getenv(REQUIRED_KEY):
    sys.exit(
        f"\n  ❌ No {REQUIRED_KEY} found.\n"
        f"\n     config.py is set to use '{CHAT_MODEL}', which needs that key."
        f"\n     Create a file called exactly '.env' next to this one, containing:"
        f"\n\n         {REQUIRED_KEY}=your-key-here\n"
        f"\n     See .env.example. No quotes, no spaces around the = sign.\n"
    )
