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
# We use Claude Haiku 4.5: it is Anthropic's fastest and cheapest current model, and for
# RAG that is exactly the right trade. The hard thinking in this project is done by the
# retriever, not the model - by the time the model sees the question, the answer is
# already sitting in front of it. You are paying it to read four paragraphs and write
# four sentences, and Haiku does that very well.
#
#   CHAT_MODEL = "anthropic:claude-sonnet-5"     # smarter, ~2x the price - try it in Session 8
#   CHAT_MODEL = "openai:gpt-4.1-mini"           # pip install langchain-openai
#   CHAT_MODEL = "google-genai:gemini-2.5-flash" # pip install langchain-google-genai
#   CHAT_MODEL = "ollama:llama3.2"               # runs HERE - no key, no internet
#
# Note that embeddings already run locally, so switching this to Ollama makes the entire
# system offline. Nothing you own ever leaves the laptop.
CHAT_MODEL = "anthropic:claude-haiku-4-5"

# temperature controls how varied the model's wording is. 0 means "always pick the most
# likely next word", which is what you want for factual answers - we are not looking for
# creativity here, we're looking for the same answer to the same question.
TEMPERATURE = 0


# ---------------------------------------------------------------------------
# Which model turns text into vectors
# ---------------------------------------------------------------------------
# This model runs on Hugging Face's servers, not on your laptop. We send it a piece of
# text, it sends back the numbers. That means nothing to download and nothing to install:
# running it locally would need PyTorch, which is well over a gigabyte.
#
# WHY THE MULTILINGUAL ONE: it understands Armenian, Russian and about fifty other
# languages as well as English. The obvious alternative, "all-MiniLM-L6-v2", is slightly
# sharper on English but is ENGLISH ONLY - on Armenian it scores a correct answer and a
# completely unrelated sentence within 0.004 of each other, so retrieval becomes random
# and nothing tells you it has. Since you choose your own notes, multilingual is the safe
# default.
#
# Note this has nothing to do with CHAT_MODEL above. Anthropic does not make an embedding
# model at all, so the two halves of this project come from different companies - a neat
# illustration of why we kept them in separate files.
#
# If you change this, you MUST re-run ingest.py. Vectors made by two different models are
# not comparable, and searching one with the other returns nonsense without any error.
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


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

# Hugging Face works without a token, but an anonymous request shares a rate limit with
# everyone else on your network - and sixteen students in one room look like one very
# busy user. A free token from huggingface.co/settings/tokens raises that limit and is
# strongly recommended. Nothing breaks without it; you may just get asked to slow down.
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Hand it to the library under the name it looks for, so the rest of the code doesn't
# have to think about it.
if HF_TOKEN:
    os.environ.setdefault("HUGGINGFACEHUB_API_TOKEN", HF_TOKEN)


KEY_FOR_PROVIDER = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google-genai": "GOOGLE_API_KEY",
    "ollama": None,          # runs on this computer, needs no key
}

PROVIDER = CHAT_MODEL.split(":")[0]
REQUIRED_KEY = KEY_FOR_PROVIDER.get(PROVIDER, "ANTHROPIC_API_KEY")

if REQUIRED_KEY and not os.getenv(REQUIRED_KEY):
    sys.exit(
        f"\n  ❌ No {REQUIRED_KEY} found.\n"
        f"\n     config.py is set to use '{CHAT_MODEL}', which needs that key."
        f"\n     Create a file called exactly '.env' next to this one, containing:"
        f"\n\n         {REQUIRED_KEY}=your-key-here\n"
        f"\n     See .env.example. No quotes, no spaces around the = sign.\n"
    )
