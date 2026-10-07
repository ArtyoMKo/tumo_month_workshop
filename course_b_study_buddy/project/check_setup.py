"""
check_setup.py - run this first, and whenever something stops working.

    python check_setup.py

It checks one thing at a time, in the order things depend on each other, and stops at the
first failure. That order matters: if the embedding model isn't downloaded, there's no
point being told about six other problems that are all caused by it.

Teachers: run this on a lab machine with the real workshop key before Lesson 1. Step 4
is the first call that proves the key works.
"""

import os
import sys


def ok(message):
    print(f"  ✅ {message}")


def fail(message, fix):
    print(f"  ❌ {message}")
    print(f"     FIX: {fix}")
    sys.exit(1)


print("\nChecking your Study Buddy setup...\n")

# --- 1. Python version -----------------------------------------------------
if sys.version_info < (3, 10):
    fail(
        f"Python {sys.version_info.major}.{sys.version_info.minor} is too old",
        "Install Python 3.12 from python.org, then re-create your venv",
    )
ok(f"Python {sys.version_info.major}.{sys.version_info.minor}")

# --- 2. Packages -----------------------------------------------------------
try:
    import dotenv
    import langchain  # noqa: F401
    import langchain_openai  # noqa: F401
    import langchain_chroma  # noqa: F401
    import langchain_text_splitters  # noqa: F401
except ImportError as error:
    fail(
        f"A package is missing: {error.name}",
        "Activate your venv, then run:  pip install -r requirements.txt",
    )
ok("All required packages are installed")

# --- 3. The API key --------------------------------------------------------
# Before importing our own files, because importing assistant.py builds a model, and
# building one without a key fails in a much uglier way than this does.
dotenv.load_dotenv(override=True)

key = os.getenv("OPENAI_API_KEY")
if not key:
    fail("No OPENAI_API_KEY found", "Create a file called exactly '.env' - see .env.example")
if key.strip() != key:
    fail("Your key has a space or a tab at the start or end", "Edit .env and delete it")
if key.startswith("sk-ant-"):
    fail("That is an Anthropic key, not an OpenAI one", "Ask your teacher for the OpenAI key - it begins sk-proj-")
if not key.startswith("sk-"):
    fail("Your key doesn't start with 'sk-'", "OpenAI keys begin sk-proj- - check you pasted the whole thing")
ok(f"API key found, begins {key[:11]}...")

# --- 4. The embedding model ------------------------------------------------
# It runs on OpenAI's servers, so this is a network call, not a download - and the first
# check that the key actually works. It costs a tiny fraction of a cent.
print("\n  Asking OpenAI to turn a sentence into numbers...")
try:
    from langchain_openai import OpenAIEmbeddings

    import config

    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
    vector = embeddings.embed_query("test")
except Exception as error:
    fail(
        f"The embedding model failed: {type(error).__name__}: {error}",
        "Check your internet connection, and check the key in .env is valid and has credit",
    )
if len(vector) != 1536:
    fail(f"Got {len(vector)} numbers back, expected 1536", "Tell your teacher - this is unusual")
ok(f"Embedding model works ({len(vector)} numbers per piece of text)")

# --- 5. Documents ----------------------------------------------------------
if not config.DOCUMENTS_DIR.exists():
    fail(f"No documents folder at {config.DOCUMENTS_DIR}", "Create it and put your notes in it")

files = [p for p in config.DOCUMENTS_DIR.glob("**/*") if p.suffix.lower() in {".md", ".txt"}]
if not files:
    fail("The documents folder is empty", "Put some .md or .txt files in it")
ok(f"{len(files)} document(s) found")

# --- 6. The index ----------------------------------------------------------
import retriever

if not retriever.index_exists():
    fail("No index has been built yet", "Run:  python ingest.py")
ok(f"Index found: {retriever.chunk_count()} chunks")

# --- 7. Retrieval, no model involved --------------------------------------
# Before the chat model call, because if search is broken that call is wasted money.
chunks = retriever.find_relevant_chunks("What is this about?")
if not chunks:
    fail("Search returned nothing at all", "Re-run:  python ingest.py")
ok(f"Search works ({len(chunks)} chunks returned, from {', '.join(retriever.sources_of(chunks))})")

# --- 8. One real answer ----------------------------------------------------
print("\n  Testing a full answer (costs a fraction of a cent)...")
try:
    import assistant

    answer, sources = assistant.answer_question("What is this collection of documents about?")
except Exception as error:
    fail(
        f"The model call failed: {type(error).__name__}: {error}",
        "Check your internet, and check the key in .env is valid and has credit",
    )
ok(f"Got an answer, citing: {', '.join(sources)}")

print(f"\n  It said: {answer[:200]}")
print("\n🎉 Everything works. Run:  python main.py\n")
