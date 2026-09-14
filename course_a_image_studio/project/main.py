"""
main.py - the entry point. This is the file you run.

    python main.py

Its job is to talk to the human and to nobody else. It asks questions, calls the other
modules in the right order, and reports what happened. Every actual piece of work -
talking to the model, building prompts, writing files - happens somewhere else.

Keeping it that way is what makes the rest of the project reusable. You could throw this
file away, write a web page or a Discord bot instead, and every other file would work
unchanged.
"""

import client
import config
import gallery
import prompts


def ask(question, default):
    """
    Ask the user something, and use the default if they just press Enter.

    Pressing Enter to accept a sensible default is the difference between a program
    that's pleasant to use and one you dread starting.
    """
    answer = input(f"{question} [{default}]: ").strip()
    return answer or default


def welcome():
    """Print the header, so the user can see the studio's settings before spending anything."""
    print()
    print("=" * 62)
    print("  AI IMAGE STUDIO")
    print("=" * 62)
    print(f"  Model    : {config.CHAT_MODEL}")
    print(f"  Quality  : {config.IMAGE_QUALITY}")
    print(f"  Gallery  : {config.GALLERY_DIR}  ({gallery.count_images()} images so far)")
    print("=" * 62)
    print()


def create_one_image():
    """
    Run through one full image: ask, build, generate, save, report.

    Returns True if we made an image, False if the user asked to stop.
    """
    subject = input("What would you like to see?  (or 'quit' to stop)\n> ").strip()

    if not subject or subject.lower() in {"quit", "exit", "q"}:
        return False

    style = ask(f"Style?  ({prompts.list_styles()})", config.DEFAULT_STYLE)
    size = ask("Size?  (square, wide, tall)", config.DEFAULT_SIZE)
    improve = ask("Let the AI improve your description first?  (y/n)", "n")

    # Optionally rewrite the user's idea into something more detailed.
    # We print the result so they can see what was actually sent - a program that silently
    # changes your input is a program you stop trusting.
    if improve.lower().startswith("y"):
        print("\n  Improving your description...")
        subject = prompts.improve_prompt(subject)
        print(f"  Using: {subject}")

    full_prompt = prompts.build_prompt(subject, style)

    print("\n  Generating... (this usually takes 10-30 seconds)")
    image_bytes = client.generate_image(full_prompt, size=size)

    path = gallery.save_image(image_bytes, subject, style)

    print(f"\n  ✅ Saved to {path}")
    print(f"     {len(image_bytes) / 1024:.0f} KB, {style} style, {size}\n")
    return True


def main():
    """Run the studio until the user asks to stop."""
    welcome()

    while True:
        try:
            if not create_one_image():
                break

        # One try/except, in one place, at the edge of the program. Everything underneath
        # is allowed to just fail loudly - it's this function's job to turn a failure into
        # a sentence a human can act on, and then carry on rather than dying.
        except ValueError as error:
            # Raised by client.extract_image_bytes when the model didn't draw anything.
            print(f"\n  ⚠️  {error}")
            print("     Try rephrasing - the model sometimes refuses prompts it finds unclear.\n")

        except KeyboardInterrupt:
            # The user pressed Ctrl+C. That's not an error, it's a request.
            print("\n\n  Stopped.\n")
            break

        except Exception as error:
            # Anything else: no internet, bad key, provider outage. Show the type as well
            # as the message, because "AuthenticationError" tells you far more than the
            # sentence that comes with it.
            print(f"\n  ⚠️  Something went wrong: {type(error).__name__}: {error}")
            print("     Check your internet connection and your .env file.\n")

    print(f"Goodbye! Your gallery has {gallery.count_images()} images in it.\n")


# This line means "only run main() if this file was started directly".
# If some other file imports main.py, this block does not run - which is what lets you
# import pieces of a program without accidentally launching it.
if __name__ == "__main__":
    main()
