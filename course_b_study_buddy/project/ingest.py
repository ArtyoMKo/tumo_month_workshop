"""
ingest.py - read your documents, cut them up, and build the search index.

    python ingest.py

This is the SLOW half of the project, and you only run it when your documents change.
It reads everything in documents/, splits it into chunks, turns every chunk into a vector,
and saves the result into vector_db/.

main.py then reads that saved index instantly, instead of rebuilding it every time you
want to ask a question. Separating the two is the difference between a program that starts
in half a second and one that makes you wait thirty seconds before every conversation.

Run this again whenever you add, remove or edit a file in documents/ - otherwise you'll be
searching yesterday's notes.
"""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config


def load_documents():
    """
    Read every .md and .txt file in documents/ and return them as LangChain Documents.

    A Document is text plus a metadata dictionary. We put the filename in the metadata
    here, at the very start, and it survives every later step - splitting, embedding,
    retrieval - which is what lets the assistant tell you where an answer came from.

    sorted() so the order is identical on every run and every machine. Without it the
    order depends on the filesystem, and results that change for no visible reason are
    the most miserable kind of bug to chase.

    encoding="utf-8" is not optional: without it, Windows sometimes guesses a different
    encoding and mangles every non-English character in your notes.
    """
    documents = []

    for path in sorted(config.DOCUMENTS_DIR.glob("**/*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue

        text = path.read_text(encoding="utf-8")

        # Skip empty files. An empty chunk embeds to a meaningless vector that can show
        # up in search results for any question at all, which is baffling to debug.
        if not text.strip():
            print(f"  (skipping {path.name} - it's empty)")
            continue

        documents.append(Document(page_content=text, metadata={"filename": path.name}))

    return documents


def split_into_chunks(documents):
    """
    Cut documents into chunks small enough to retrieve usefully.

    RecursiveCharacterTextSplitter breaks at the most natural place available: paragraph
    breaks first, then line breaks, then sentences, then words. So chunks tend to end
    somewhere sensible rather than halfway through a thought.

    The overlap means each chunk repeats a little of the previous one, so a sentence that
    lands exactly on a boundary still appears whole somewhere.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def build_index(chunks):
    """
    Turn every chunk into a vector and save the whole lot into vector_db/.

    Chroma writes to disk, so this survives closing your laptop - that's the entire point
    of doing it as a separate step.

    Returns the vector store, so this function is also usable from a notebook.
    """
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

    # If an index already exists, delete it first. Otherwise we'd add a second copy of
    # every chunk on top of the old one, and searches would return duplicates - or worse,
    # chunks from documents you deleted weeks ago.
    if config.DB_DIR.exists():
        Chroma(
            persist_directory=str(config.DB_DIR), embedding_function=embeddings
        ).delete_collection()

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(config.DB_DIR),
    )


def main():
    """Run the whole ingest: load, split, embed, save - printing progress at each stage."""
    print("\nBuilding your Study Buddy's index...\n")

    if not config.DOCUMENTS_DIR.exists():
        print(f"  ❌ There's no documents folder at {config.DOCUMENTS_DIR}")
        print("     Create it and put some .md or .txt files in it.\n")
        return

    print(f"  Reading {config.DOCUMENTS_DIR}...")
    documents = load_documents()

    if not documents:
        print("  ❌ No .md or .txt files found. Put your notes in the documents folder.\n")
        return

    for doc in documents:
        print(f"    {doc.metadata['filename']:30} {len(doc.page_content):>7,} characters")

    print(f"\n  Splitting into chunks (size {config.CHUNK_SIZE}, overlap {config.CHUNK_OVERLAP})...")
    chunks = split_into_chunks(documents)
    average = sum(len(c.page_content) for c in chunks) / len(chunks)
    print(f"    {len(documents)} documents → {len(chunks)} chunks, average {average:.0f} characters")

    print("\n  Creating embeddings... (the first run downloads the model - be patient)")
    build_index(chunks)

    print(f"\n  ✅ Index built and saved to {config.DB_DIR}")
    print("\n  Now run:  python main.py\n")


# Only run main() if this file was started directly. If something imports ingest.py,
# this block doesn't run - which is what lets you reuse load_documents() elsewhere
# without accidentally rebuilding the entire index.
if __name__ == "__main__":
    main()
