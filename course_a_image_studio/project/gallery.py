"""
gallery.py - saving images to disk with filenames you can actually read.

The whole file exists to answer one question well: given some image bytes and the prompt
that produced them, where should the file go and what should it be called?

Nothing in here talks to a model. It's pure file handling, which means you can test it
without spending a penny - just hand it any bytes you like.
"""

import re
from datetime import date

import config


def slugify(text, max_words=5):
    """
    Turn a prompt into something safe to use inside a filename.

    "A ginger cat asleep on a radiator!!" -> "a-ginger-cat-asleep-on"

    We strip punctuation because several characters are illegal in filenames on Windows,
    and we cut the length because a 200-character filename is unusable.

    Falls back to "image" when nothing usable is left - an empty slug would produce a
    file called just ".png", which is hidden by default on Mac and Linux and would look
    to the student like the program silently did nothing.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", "", text)          # keep only letters, digits and spaces
    words = text.split()[:max_words]                 # first few words only
    return "-".join(words) or "image"


def unique_path(path):
    """
    Return a path that doesn't exist yet, by adding -2, -3, ... if it has to.

    Without this, generating the same prompt in the same style twice on the same day
    would silently overwrite the first image. Silently destroying someone's work is
    about the rudest thing a program can do.
    """
    if not path.exists():
        return path

    counter = 2
    while True:
        candidate = path.with_name(f"{path.stem}-{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def save_image(image_bytes, subject, style_name):
    """
    Save image bytes into the gallery folder and return the path they were written to.

    Filenames look like:  2026-03-14_a-paper-boat-floating_cinematic.png

    The date comes first so that sorting the folder alphabetically also sorts it by
    time - that only works because ISO dates (YYYY-MM-DD) happen to sort correctly as
    plain text, which is exactly why that format is an international standard.
    """
    # exist_ok=True means "fine if it's already there" - so this is safe to call every time
    config.GALLERY_DIR.mkdir(exist_ok=True)

    filename = f"{date.today()}_{slugify(subject)}_{style_name}.png"
    path = unique_path(config.GALLERY_DIR / filename)

    # "write_bytes" and not "write_text": this is a picture, not words. Writing it as
    # text would mangle it and produce a file that no image viewer can open.
    path.write_bytes(image_bytes)
    return path


def count_images():
    """How many images are in the gallery? Used for the welcome message in main.py."""
    if not config.GALLERY_DIR.exists():
        return 0
    return len(list(config.GALLERY_DIR.glob("*.png")))
