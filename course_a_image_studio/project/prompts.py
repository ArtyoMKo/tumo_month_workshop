"""
prompts.py - everything to do with the words we send to the model.

Two jobs:

  1. Hold the named style presets, so that every "watercolour" image in your gallery is
     described with exactly the same words and they genuinely look like a set.
  2. Build the final prompt string, and optionally improve it with a text model first.

Deliberately, this file talks to no model directly and touches no files. It only builds
strings. That means you can read it, change a style, and see what will happen without
running anything.
"""

import client

# ---------------------------------------------------------------------------
# Style presets
# ---------------------------------------------------------------------------
# The key is the short name you type; the value is the long description that actually
# gets sent to the model.
#
# ADD YOUR OWN HERE. A good preset names at least four things: the medium, the colours,
# the level of detail, and something about the light.
STYLES = {
    "photo": "photorealistic, natural lighting, shot on 35mm film, shallow depth of field",
    "watercolour": "watercolour painting, soft edges, muted colours, visible paper texture",
    "pixel": "16-bit pixel art, limited colour palette, crisp pixels, retro game sprite",
    "cinematic": "cinematic film still, dramatic lighting, wide aspect, moody atmosphere",
    "sketch": "rough pencil sketch, black and white, visible construction lines",
    "cute": "cute flat vector illustration, bold outlines, bright friendly colours",
}


# ---------------------------------------------------------------------------
# The prompt improver
# ---------------------------------------------------------------------------
# This paragraph of English is, genuinely, part of the program. Changing it changes what
# the studio does, just as much as changing the Python would. It lives up here on its own
# so you can read all of it at once while you're tuning it.
IMPROVER_SYSTEM_PROMPT = """
You are a prompt engineer for an image generation model.
The user gives you a short, plain idea. You rewrite it as one vivid sentence
that an image model can work with.

Include: the subject, what is happening, the lighting, and the mood.
Do NOT add an art style - the studio applies that separately.
Do NOT explain yourself, do not use quotation marks, do not add a preamble.
Reply with the improved prompt and nothing else.
"""


def improve_prompt(rough_prompt):
    """
    Expand a short idea into a detailed image prompt, using a text model.

    "a dragon" becomes something like "an enormous scarred dragon coiled around a ruined
    stone tower at dusk, low red light catching its scales, quiet and watchful".

    This is optional on purpose. It genuinely helps with lazy one-word prompts, and it
    genuinely gets in the way when you already know exactly what you want - it will add
    details you didn't ask for. main.py asks the user which they'd prefer.
    """
    return client.ask_text(IMPROVER_SYSTEM_PROMPT, rough_prompt)


def build_prompt(subject, style_name):
    """
    Join a subject and a named style into the full prompt we send to the image model.

    Looking the style text up here - rather than making the caller paste in a long
    description - is what keeps a set of images consistent with each other.

    Unknown style names fall back to plain text with no style, rather than crashing.
    A typo should give you a slightly disappointing picture, not a stack trace.
    """
    style_text = STYLES.get(style_name, "")
    return f"{subject}. {style_text}".strip().rstrip(".")


def list_styles():
    """Return the style names as a readable comma-separated string, for menus and help text."""
    return ", ".join(STYLES.keys())
