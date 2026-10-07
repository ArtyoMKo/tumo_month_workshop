"""
config.py - every setting for the Study Buddy, in one place.

Settings scattered through a program are settings you can't find. When you want to change
the model, the chunk size, or how many chunks get retrieved, you should know exactly which
file to open - and it should be this one.

Nothing in here does any work. It only holds decisions.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Read the .env file so our API key is available to the libraries that need it.
# override=True means "re-read even if something was loaded before" - without it, editing
# .env and re-running would quietly keep using the old value.
load_dotenv(override=True)


# ---------------------------------------------------------------------------
# Where things live
# ---------------------------------------------------------------------------
# Path(__file__).parent is the folder this file is in, so these work no matter which
# directory you happened to run the program from.
PROJECT_DIR = Path(__file__).parent
DOCUMENTS_DIR = PROJECT_DIR / "documents"     # your own notes go here
DB_DIR = PROJECT_DIR / "vector_db"            # built by ingest.py - don't edit by hand


# ---------------------------------------------------------------------------
# Which AI model answers the questions
# ---------------------------------------------------------------------------
# "provider:model-name". Change this one string and the whole program follows -
# no other file mentions any provider by name.
#
# We use GPT-5.4 mini: it is OpenAI's fast, cheap current model, and for RAG that is
# exactly the right trade. The hard thinking in this project is done by the retriever,
# not the model - by the time the model sees the question, the answer is already sitting
# in front of it. You are paying it to read four paragraphs and write four sentences,
# and the mini model does that very well.
#
#   CHAT_MODEL = "openai:gpt-5.4"                # smarter, ~3x the price - try it in Lesson 8
#   CHAT_MODEL = "anthropic:claude-haiku-4-5"    # pip install langchain-anthropic
#   CHAT_MODEL = "google-genai:gemini-2.5-flash" # pip install langchain-google-genai
#   CHAT_MODEL = "ollama:llama3.2"               # runs HERE - no key, no internet
#
# Switch this to Ollama AND the embeddings to a local model (see retriever.py), and the
# entire system runs offline. Nothing you own ever leaves the laptop.
CHAT_MODEL = "openai:gpt-5.4-mini"

# temperature controls how varied the model's wording is. 0 means "always pick the most
# likely next word", which is what you want for factual answers - we are not looking for
# creativity here, we're looking for the same answer to the same question.
TEMPERATURE = 0

# Everything the model is built with, gathered in one dictionary for assistant.py.
#
# OpenAI's GPT-5 models can "reason" - think privately before answering. We don't need
# that here (the answer is already in the retrieved chunks), and while it's switched on,
# LangChain quietly ignores TEMPERATURE. So for OpenAI we switch it off. Other providers
# don't have this setting, which is why it's only added for "openai:".
MODEL_SETTINGS = {"temperature": TEMPERATURE}
if CHAT_MODEL.startswith("openai:"):
    MODEL_SETTINGS["reasoning_effort"] = "none"


# ---------------------------------------------------------------------------
# Which model turns text into vectors
# ---------------------------------------------------------------------------
# This model runs on OpenAI's servers, not on your laptop, and uses the same key as
# CHAT_MODEL. We send it a piece of text, it sends back the numbers. That means nothing
# to download and nothing to install.
#
# It costs $0.02 per million tokens - fifty times cheaper than the chat model. Embedding
# every note you own and every question you ask all workshop costs less than a cent.
#
# KNOW ITS LIMIT: it is very good in English and much weaker in Armenian. On our test
# questions it found the right English chunk 7 times out of 8, but the right Armenian one
# only 1 time in 4. If your notes are in Armenian, test retrieval before trusting answers.
#
#   EMBEDDING_MODEL = "text-embedding-3-large"   # slightly sharper, ~6x the price
#
# Note this has nothing to do with CHAT_MODEL above - the two are set separately, and
# could even come from different companies. That's why they live in separate files.
#
# If you change this, you MUST re-run ingest.py. Vectors made by two different models are
# not comparable, and searching one with the other returns nonsense without any error.
EMBEDDING_MODEL = "text-embedding-3-small"


# ---------------------------------------------------------------------------
# The dials
# ---------------------------------------------------------------------------
# How big each piece of your documents is when we cut them up.
# Too small and a chunk stops mid-thought; too large and it's mostly irrelevant text.
# 500-1000 is where you start. Changing these means re-running ingest.py.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# How many chunks to retrieve for each question.
# Too few and you miss answers that were there; too many and the answers get vague.
# 4-6 is the usual range.
RETRIEVE_K = 4


# ---------------------------------------------------------------------------
# A friendly check that we have a key at all
# ---------------------------------------------------------------------------
# Every other file imports this one, so this runs before anything else can go wrong.
# Without it, a missing key produces about forty lines of library traceback ending in
# "api_key must be set" - technically true, completely unhelpful.


KEY_FOR_PROVIDER = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google-genai": "GOOGLE_API_KEY",
    "ollama": None,          # runs on this computer, needs no key
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
