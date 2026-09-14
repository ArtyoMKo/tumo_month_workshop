"""
client.py - the provider-agnostic layer.

This is the only file in the project that knows how to talk to an AI model. Everything
else asks *this* file for an image and gets back bytes, without knowing or caring which
company produced them.

That separation is the whole point of the architecture. Swapping providers means editing
config.py, and at most this file - never main.py, prompts.py or gallery.py.
"""

import base64

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

import config

# Build the model once, when this file is first imported, rather than on every call.
# Creating it is cheap but not free, and there's no reason to do it repeatedly.
#
# Note that this line does not mention OpenAI, or any other company. All it knows is
# the string it was handed from config.py.
BASE_MODEL = init_chat_model(config.CHAT_MODEL)


def extract_image_bytes(response):
    """
    Pull the image out of a model's response and return it as raw bytes.

    Models reply with a list of 'content blocks'. Some blocks are text ("Here's your
    picture!"), some are images. We want the first image block, and we want its base64
    text decoded back into the real bytes of a PNG file.

    Raises ValueError if the model replied without drawing anything - which does happen,
    usually when it decided the request needed clarification instead of a picture.
    """
    for block in response.content_blocks:
        if block["type"] == "image":
            return base64.b64decode(block["base64"])

    # No image block. Include what the model *did* say, because that's almost always
    # the explanation - a refusal, or a question.
    raise ValueError(f"The model returned no image. It said: {response.text!r}")


def generate_image(prompt, size=config.DEFAULT_SIZE):
    """
    Generate one image from a full text prompt, and return it as bytes.

    prompt - the complete description to send. Build it with prompts.build_prompt()
             rather than assembling it here; this file's job is talking to the model,
             not deciding what to say.
    size   - "square", "wide" or "tall" (see config.SIZES)

    Returns the image as bytes, ready to write to a file.
    """
    # Ask the model for permission to draw, and set the picture's shape and quality
    # while we're at it. bind_tools returns a *new* model object with the tool attached -
    # BASE_MODEL itself is left untouched, so we can bind different settings per call.
    #
    # (In the Session 3 notebook we asked for the size inside the prompt text, which
    # mostly worked. Setting it as a real parameter here is the proper way: the model
    # is told the size rather than asked for it.)
    image_tool = {
        "type": "image_generation",
        "quality": config.IMAGE_QUALITY,
        "size": config.SIZES.get(size, config.SIZES[config.DEFAULT_SIZE]),
    }

    drawing_model = BASE_MODEL.bind_tools([image_tool])
    response = drawing_model.invoke(prompt)
    return extract_image_bytes(response)


def ask_text(system_prompt, user_message):
    """
    Ask the model a plain text question and return its reply as a string.

    Used by prompts.improve_prompt(). It lives here rather than there because this file
    owns every conversation with a model - so if you ever change providers, there is
    exactly one file to check.

    system_prompt - who the model is and what its job is
    user_message  - what we actually want it to work on
    """
    response = BASE_MODEL.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message),
    ])
    return response.text.strip()
