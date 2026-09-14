"""
assistant.py - turning retrieved chunks into a grounded answer.

This file owns the one thing that makes the whole project trustworthy: the system prompt.
That paragraph of English does more work than any line of Python here. It is what stops
the assistant answering questions your documents don't cover.

It is also the only file that talks to a language model.
"""

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

import config
import retriever

# Build the model once, when this file is first imported.
#
# Note that this line names no company. It only knows the string from config.py - which
# is exactly why changing providers is a one-line change and not a rewrite.
model = init_chat_model(config.CHAT_MODEL, temperature=config.TEMPERATURE)


# ---------------------------------------------------------------------------
# The system prompt
# ---------------------------------------------------------------------------
# Read this as carefully as you'd read code, because it behaves like code.
#
# Every sentence is here for a reason:
#   - "ONLY the notes"          stops it answering from general knowledge
#   - the exact refusal wording gives it something specific to say instead of guessing
#   - "Do not guess"            the same instruction again, plainly, because repetition
#                               measurably helps
#   - "short and correct beats  removes the pressure to pad an answer out, which is where
#      long and maybe"          a lot of invented detail creeps in
#
# Try deleting any one of those lines and asking a question your notes don't cover. The
# difference is not subtle.
SYSTEM_PROMPT = """
You are a study assistant. You answer questions about the user's own notes.

Use ONLY the notes below. Do not use anything you know from anywhere else.
If the notes do not contain the answer, say exactly: "That isn't in your documents."
Do not guess. Do not fill in gaps from general knowledge.
A short answer that is definitely correct is much better than a long one that might not be.

When the notes do answer the question, answer in a few clear sentences.

NOTES:
{context}
"""


def build_context(chunks):
    """
    Join retrieved chunks into a single block of text for the prompt.

    The "---" separator matters more than it looks. Without a clear break, the model can
    read the end of one chunk and the start of the next as a single sentence, and invent
    a connection between two unrelated notes.
    """
    return "\n\n---\n\n".join(chunk.page_content for chunk in chunks)


def answer_question(question, k=config.RETRIEVE_K):
    """
    Answer a question using only the user's documents.

    The whole pipeline, in four steps:
        1. find the chunks closest in meaning to the question   (retriever.py)
        2. join them into one block of context                  (build_context)
        3. paste that into the system prompt                    (SYSTEM_PROMPT)
        4. ask the model                                        (model.invoke)

    Returns a tuple: (answer, sources) where sources is a list of filenames.

    We return the sources alongside the answer, always, so the user can go and check.
    An answer nobody can trace back to a document is exactly the thing this whole project
    exists to avoid - even on the occasions when it happens to be right.
    """
    chunks = retriever.find_relevant_chunks(question, k=k)
    context = build_context(chunks)

    response = model.invoke([
        SystemMessage(content=SYSTEM_PROMPT.format(context=context)),
        HumanMessage(content=question),
    ])

    return response.text, retriever.sources_of(chunks)
