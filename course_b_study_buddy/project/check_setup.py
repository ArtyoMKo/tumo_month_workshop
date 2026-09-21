"""
check_setup.py - run this first, and whenever something stops working.

    python check_setup.py

It checks one thing at a time, in the order things depend on each other, and stops at the
first failure. That order matters: if the embedding model isn't downloaded, there's no
point being told about six other problems that are all caused by it.

Teachers: run this on a lab machine with the real workshop key before Session 1. Step 4
is the one that downloads ~900 MB - get it out of the way the day before.
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
    import langchain_anthropic  # noqa: F401
    import langchain_chroma  # noqa: F401
    import langchain_huggingface  # noqa: F401
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

key = os.getenv("ANTHROPIC_API_KEY")
if not key:
    fail("No ANTHROPIC_API_KEY found", "Create a file called exactly '.env' - see .env.example")
if key.strip() != key:
    fail("Your key has a space or a tab at the start or end", "Edit .env and delete it")
if not key.startswith("sk-ant-"):
    fail("Your key doesn't start with 'sk-ant-'", "Anthropic keys begin sk-ant- - check you pasted the whole thing")
ok(f"API key found, begins {key[:11]}...")

# --- 4. The embedding model ------------------------------------------------
# The slow one. On a fresh machine this downloads about 900 MB.
print("\n  Loading the local embedding model (first run downloads ~900 MB)...")
try:
    from langchain_huggingface import HuggingFaceEmbeddings

    import config

    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    vector = embeddings.embed_query("test")
except Exception as error:
    fail(
        f"Could not load the embedding model: {type(error).__name__}: {error}",
        "Check your internet connection - the model downloads on first use",
    )
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
# Before any paid call, because if search is broken the paid call is wasted money.
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
