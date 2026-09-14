"""
check_setup.py - run this first, and whenever something stops working.

    python check_setup.py

It checks one thing at a time, in the order things depend on each other, and stops at the
first failure. That order matters: if your key is missing, there is no point being told
about six other problems that are all caused by it.

Teachers: run this on a lab machine with the real workshop key before Session 1.
"""

import os
import sys


def ok(message):
    print(f"  ✅ {message}")


def fail(message, fix):
    print(f"  ❌ {message}")
    print(f"     FIX: {fix}")
    sys.exit(1)


print("\nChecking your AI Image Studio setup...\n")

# --- 1. Python version -----------------------------------------------------
# First, because a too-old Python shows up as confusing syntax errors everywhere else.
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
except ImportError as error:
    fail(
        f"A package is missing: {error.name}",
        "Activate your venv, then run:  pip install -r requirements.txt",
    )
ok("All required packages are installed")

# --- 3. The API key --------------------------------------------------------
# Checked before we import our own files, because importing client.py builds a model,
# and building a model without a key fails in a much uglier way than this does.
dotenv.load_dotenv(override=True)

key = os.getenv("OPENAI_API_KEY")
if not key:
    fail("No OPENAI_API_KEY found", "Create a file called exactly '.env' - see .env.example")
if key.strip() != key:
    fail("Your key has a space or a tab at the start or end", "Edit .env and delete it")
if not key.startswith("sk-"):
    fail("Your key doesn't start with 'sk-'", "Check you pasted the whole key")
ok(f"API key found, begins {key[:8]}...")

# --- 4. Our own files ------------------------------------------------------
try:
    import client
    import config  # noqa: F401
    import gallery
    import prompts
except ImportError as error:
    fail(
        f"Could not import one of our own files: {error}",
        "Run this from inside the project folder, the one where main.py lives",
    )
ok("config.py, client.py, prompts.py and gallery.py all import cleanly")

# --- 5. Pure functions, no network ----------------------------------------
# Before any paid call, because if these are broken the paid call is wasted money.
assert gallery.slugify("A ginger cat!!") == "a-ginger-cat"
assert gallery.slugify("!!!") == "image"
assert "watercolour" in prompts.build_prompt("a boat", "watercolour")
ok("slugify() and build_prompt() behave correctly")

# --- 6. One cheap text call ------------------------------------------------
print("\n  Testing a text call (costs a fraction of a cent)...")
try:
    reply = client.ask_text("Reply with exactly one word.", "Say hello")
except Exception as error:
    fail(
        f"The text call failed: {type(error).__name__}: {error}",
        "Check your internet, and check the key in .env is valid and has credit",
    )
ok(f"Text model replied: {reply!r}")

# --- 7. One real image -----------------------------------------------------
# Last, because it's the slowest and the most expensive thing we do.
print("\n  Testing image generation (costs about one cent, takes ~20 seconds)...")
try:
    image_bytes = client.generate_image("a single red apple on a white table")
except Exception as error:
    fail(
        f"Image generation failed: {type(error).__name__}: {error}",
        "The model named in config.py may not offer image generation on this account.\n"
        '          Edit config.py and try:  CHAT_MODEL = "openai:gpt-4.1"',
    )

if not image_bytes.startswith(b"\x89PNG"):
    fail("Got data back, but it isn't a PNG", "Tell your teacher - this one is unusual")

ok(f"Image generated: {len(image_bytes) / 1024:.0f} KB of valid PNG")

print("\n🎉 Everything works. Run:  python main.py\n")
