"""
main.py - the entry point. This is the file you run.

    python ingest.py     (once, and again whenever your documents change)
    python main.py       (as often as you like)

Its job is to talk to the human and nothing else. It asks for a question, calls the other
modules in order, prints the answer and the sources, and repeats.

Every piece of actual work - searching, prompting, answering - happens somewhere else.
That's what would let you replace this file with a web page or a Discord bot without
touching anything underneath it.
"""

import assistant
import config
import retriever


def welcome():
    """Print the header, so the user can see what the assistant actually knows about."""
    print()
    print("=" * 64)
    print("  STUDY BUDDY")
    print("=" * 64)
    print(f"  Model     : {config.CHAT_MODEL}")
    print(f"  Documents : {config.DOCUMENTS_DIR.name}/")
    print(f"  Index     : {retriever.chunk_count()} chunks, retrieving {config.RETRIEVE_K} per question")
    print("=" * 64)
    print("\n  Ask a question, or type:")
    print("    /sources <question>   see which chunks would be retrieved, with scores")
    print("    /forget               start a fresh conversation")
    print("    /quit                 stop")
    print()


def show_sources(question):
    """
    Show the chunks that would be retrieved, and how close each one is.

    This exists because when an answer is wrong there are two completely different
    possible causes, and they have different fixes:

        1. The right chunk never came back  → fix your documents, chunk size, or k
        2. It came back and the model ignored it  → fix the system prompt

    Never debug the second before checking the first. This command is how you check.
    """
    results = retriever.find_relevant_chunks_with_scores(question)

    print("\n  Retrieved chunks (lower score = closer match):\n")
    for i, (chunk, score) in enumerate(results, start=1):
        preview = chunk.page_content[:150].replace("\n", " ")
        print(f"  {i}. [{score:.3f}] {chunk.metadata['filename']}")
        print(f"     {preview}...\n")


def main():
    """Ask questions in a loop until the user stops."""
    # Check the index exists before doing anything else. Forgetting to run ingest.py is
    # the single most common way to end up with an assistant that knows nothing, and the
    # symptom ("it says everything isn't in my documents") points nowhere near the cause.
    if not retriever.index_exists():
        print("\n  ❌ No index found - or it's empty.")
        print("\n     Put your notes in the documents/ folder, then run:")
        print("         python ingest.py\n")
        return

    welcome()

    # The conversation so far, as (question, answer) pairs. This is what lets a
    # follow-up like "which of them is cheaper?" work - see assistant.answer_question.
    history = []

    while True:
        try:
            question = input("> ").strip()

            if not question:
                continue

            if question.lower() in {"/quit", "/exit", "quit", "exit"}:
                break

            if question.lower() == "/forget":
                # Useful when changing subject: old questions in the history drag the
                # search back toward what you were talking about before.
                history = []
                print("\n  Conversation cleared.\n")
                continue

            if question.lower().startswith("/sources"):
                # Everything after the command word is the question
                show_sources(question[len("/sources"):].strip())
                continue

            print("\n  Thinking...")
            answer, sources = assistant.answer_question(question, history)

            print(f"\n  {answer}")
            print(f"\n  Sources: {', '.join(sources)}\n")

            history.append((question, answer))

        # One try/except, in one place, at the edge of the program. Everything underneath
        # is allowed to just fail loudly - it's this loop's job to turn a failure into a
        # sentence a human can act on, and then carry on rather than dying.
        except KeyboardInterrupt:
            # Ctrl+C isn't an error, it's a request.
            print("\n")
            break

        except Exception as error:
            # No internet, bad key, provider outage. Print the type as well as the
            # message - "AuthenticationError" tells you far more than the sentence with it.
            print(f"\n  ⚠️  Something went wrong: {type(error).__name__}: {error}")
            print("     Check your internet connection and your .env file.\n")

    print("  Goodbye!\n")


# Only run main() if this file was started directly. If something imports main.py,
# this block doesn't run - which is what lets you import parts of a program without
# accidentally launching it.
if __name__ == "__main__":
    main()
