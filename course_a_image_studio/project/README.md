# AI Image Studio

Type a description. Get a picture that has never existed before.

Built at TUMO over 16 hours, starting from a single API call in a notebook.

```
$ python main.py

==============================================================
  AI IMAGE STUDIO
==============================================================
  Model    : openai:gpt-4.1-mini
  Quality  : low
  Gallery  : /home/you/image_studio/gallery  (12 images so far)
==============================================================

What would you like to see?  (or 'quit' to stop)
> a lighthouse in a storm
Style?  (photo, watercolour, pixel, cinematic, sketch, cute) [photo]: cinematic
Size?  (square, wide, tall) [square]: wide
Let the AI improve your description first?  (y/n) [n]: y

  Improving your description...
  Using: a solitary lighthouse battered by enormous waves under a bruised
         sky, its beam cutting through sheets of rain, tense and lonely

  Generating... (this usually takes 10-30 seconds)

  ✅ Saved to gallery/2026-03-14_a-solitary-lighthouse-battered-by_cinematic.png
     412 KB, cinematic style, wide
```

---

## Install

You need **Python 3.12** and about 200 MB of disk.

```bash
# 1. Get into the project folder
cd image_studio

# 2. Make a virtual environment - a private box of packages for this project only
python -m venv .venv

# 3. Activate it
source .venv/bin/activate        # Mac / Linux
.venv\Scripts\activate           # Windows

# 4. Install what it needs
pip install -r requirements.txt

# 5. Add your API key
cp .env.example .env             # then open .env and paste your real key in

# 6. Check everything works before you start
python check_setup.py
```

`check_setup.py` tests seven things in order and stops at the first failure, telling you
how to fix it. If it ends with 🎉 you're ready.

## Run

```bash
python main.py
```

Type a description, pick a style and a size, and the image lands in `gallery/`.
Type `quit` (or press Ctrl+C) to stop.

---

## How it's put together

Five files. Each one is explainable in a single sentence — that was the design rule.

| File | What it's responsible for |
|---|---|
| `main.py` | Talking to the human. Asks questions, calls the others in order, reports what happened. |
| `config.py` | Every setting: which model, what quality, where images go. No logic, just decisions. |
| `client.py` | The only file that talks to an AI model. Hands back bytes. |
| `prompts.py` | Style presets, building the prompt string, and the optional AI prompt-improver. |
| `gallery.py` | Turning a prompt into a good filename and writing the file. |

The dependency arrows only point one way:

```
main.py  ──►  prompts.py  ──►  client.py  ──►  config.py
   │                              ▲              ▲
   ├──────────────────────────────┘              │
   └──►  gallery.py  ─────────────────────────────┘
```

`client.py` doesn't know `main.py` exists. That's deliberate: you could delete `main.py`,
write a website or a Discord bot instead, and every other file would keep working unchanged.

## Changing the AI provider

This project is not tied to any one AI company. Open `config.py` and change **one line**:

```python
CHAT_MODEL = "openai:gpt-4.1-mini"                   # the default
# CHAT_MODEL = "anthropic:claude-haiku-4-5-20251001"
# CHAT_MODEL = "google-genai:gemini-2.5-flash"
# CHAT_MODEL = "ollama:llama3.2"                     # runs on this laptop, no key, no internet
```

Then install that provider's package (uncomment the matching line in `requirements.txt`)
and put its key in `.env`. Ollama needs no key at all.

**The honest limitation:** the *text* half of the studio — the prompt improver — works with
any of those, including a model running locally on your own laptop. The *image* half needs
a provider that can actually draw, which rules out Ollama and most text-only models. An
abstraction can unify things that really are similar; it can't invent a capability that
isn't there.

## Costs

Every image costs real money from the workshop's account.

| Quality | Time | Roughly |
|---|---|---|
| `low` (default) | ~10 s | 1 cent |
| `medium` | ~20 s | a few cents |
| `high` | ~40 s | more |

`low` is the default because you want it cheap while you're experimenting, which is most
of the time. Change `IMAGE_QUALITY` in `config.py` when you've found a prompt worth keeping.

**Before running any loop that generates images, count how many calls it makes.** Four
prompts crossed with six styles is twenty-four images, not ten.

## When it breaks

| What you see | What it means | Fix |
|---|---|---|
| `❌ No OPENAI_API_KEY found` | `.env` is missing, misnamed, or in the wrong folder | It must be called exactly `.env`, next to `main.py` |
| `ModuleNotFoundError` | venv isn't activated, or packages aren't installed | Step 3, then step 4 of Install |
| `⚠️ The model returned no image` | The model replied with words instead of drawing | Rephrase — it usually means it found the request unclear |
| `AuthenticationError` / `401` | The key is wrong, expired, or out of credit | Check `.env` character by character |
| Nothing happens for 30 seconds | Nothing is wrong | Image generation is genuinely that slow |

---

## What I added

> **Students: replace this section with your own.** Say what you built, why you picked it,
> and one thing that went wrong along the way — that last part is the most interesting bit
> for anyone reading.

Example of the shape it should take:

> I added a **`--surprise` mode**. When you type `surprise` instead of a description, it
> picks a random subject from a list of 30 I wrote, and a random style, and generates it
> without asking anything else.
>
> It lives in `main.py`, because it's about how the program talks to the person using it —
> it doesn't change how images are made. The list of subjects is in `prompts.py` next to
> `STYLES`, because that's where words live.
>
> The thing that went wrong: my first version put the random choice in `client.py`, and
> then I couldn't test it without spending money every single time. Moving it to `main.py`
> meant I could check the random picking worked without generating anything at all.
