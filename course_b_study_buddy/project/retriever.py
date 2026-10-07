"""
retriever.py - finding the pieces of your documents that are relevant to a question.

This file is the search half of the assistant, and it deliberately knows nothing about
language models. You can test everything in here for a tiny fraction of a cent, which is
exactly why it's separate: when an answer comes out wrong, the first question is always
"did the right chunk come back?" - and this file is where you find out.

It reads the index that ingest.py built. It never builds one.
"""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

import config

# The embedding model must be THE SAME ONE ingest.py used. Vectors made by two different
# models are not comparable - the search would still run, and would return nonsense, with
# no error to tell you. Change it in config.py, then always re-run ingest.py.
#
# This half of the project happens to come from the same company as the chat model, but
# it doesn't have to - the two halves never needed to match. To use a different
# company's embeddings - or a free one on your own laptop - replace these two lines (and
# the matching line in ingest.py), then re-run ingest.py. For example, with Ollama:
#
#   from langchain_ollama import OllamaEmbeddings     # pip install langchain-ollama
#   embeddings = OllamaEmbeddings(model="nomic-embed-text")
embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)

# Open the index that ingest.py saved. Built once, when this file is first imported.
#
# Swapping Chroma for a hosted vector database (Pinecone, pgvector, Qdrant) would be a
# change to these lines only - everything below calls .similarity_search(), which they
# all provide.
vectorstore = Chroma(
    persist_directory=str(config.DB_DIR),
    embedding_function=embeddings,
)


def index_exists():
    """
    Has ingest.py been run yet, and did it produce anything?

    Checked before answering, so a student who forgot to run ingest gets one clear
    sentence instead of an assistant that mysteriously knows nothing about anything.
    """
    return config.DB_DIR.exists() and vectorstore._collection.count() > 0


def chunk_count():
    """How many chunks are in the index? Used in main.py's welcome message."""
    return vectorstore._collection.count()


def find_relevant_chunks(question, k=config.RETRIEVE_K):
    """
    Return the k chunks whose meaning is closest to the question.

    This is a similarity search over vectors, not a word search - so a question about
    "the heaviest thing they can fly" can find a note saying "no payload exceeds 2.8 kg",
    even though the two share no words at all.

    Returns a list of Documents. Each one still carries its filename in .metadata.

    IMPORTANT: this always returns k chunks, even when your documents contain nothing
    relevant at all. It hands back the closest things it has, however far away they are.
    Deciding that none of them actually answer the question is the model's job, and it
    only does it because assistant.py explicitly tells it to.
    """
    return vectorstore.similarity_search(question, k=k)


def find_relevant_chunks_with_scores(question, k=config.RETRIEVE_K):
    """
    Same as find_relevant_chunks, but each result comes with a distance score.

    For Chroma the score is a distance, so LOWER means closer. (Other vector stores report
    it the other way round - always check rather than assuming which direction is better.)

    Used by main.py's /sources command, and genuinely useful for debugging: if a question
    is answered badly, look at the scores before you blame the prompt.
    """
    return vectorstore.similarity_search_with_score(question, k=k)


def sources_of(chunks):
    """
    The unique filenames these chunks came from, in a predictable order.

    A set removes duplicates, because four chunks often come from the same two files;
    sorted() turns it back into a list so the output doesn't shuffle between runs.
    """
    return sorted({chunk.metadata["filename"] for chunk in chunks})
