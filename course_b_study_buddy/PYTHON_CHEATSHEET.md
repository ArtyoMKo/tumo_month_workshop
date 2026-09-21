# Python Cheatsheet

**Keep this open in a tab for the whole workshop.** You already program — this is a
lookup table, not a lesson. Nothing here is taught in class; if you need something,
find it here or ask.

---

## Coming from JavaScript

| JavaScript | Python |
|---|---|
| `let name = "Ada";` | `name = "Ada"` |
| `const MAX = 10;` | `MAX = 10` *(capitals = "don't change me"; not enforced)* |
| `` `Hello ${name}` `` | `f"Hello {name}"` ← **forget the `f` and it prints literally** |
| `[1, 2, 3]` | `[1, 2, 3]` |
| `arr.length` | `len(arr)` |
| `arr.push(x)` | `arr.append(x)` |
| `arr.slice(0, 3)` | `arr[:3]` |
| `arr[arr.length - 1]` | `arr[-1]` |
| `{ a: 1 }` | `{"a": 1}` ← **keys need quotes** |
| `obj.a` | `obj["a"]` ← **no dot access** |
| `obj.a ?? "x"` | `obj.get("a", "x")` |
| `if (x > 3) { }` | `if x > 3:` + indent ← **indentation IS the syntax** |
| `for (const x of arr)` | `for x in arr:` |
| `function f(a, b = 2)` | `def f(a, b=2):` |
| `arr.map(x => x * 2)` | `[x * 2 for x in arr]` |
| `arr.filter(x => x > 2)` | `[x for x in arr if x > 2]` |
| `arr.join(", ")` | `", ".join(arr)` ← **glue comes first** |
| `true` / `false` / `null` | `True` / `False` / `None` |
| `&&` / `||` / `!` | `and` / `or` / `not` |
| `x || "fallback"` | `x or "fallback"` |
| `===` | `==` |
| `// comment` | `# comment` |
| `console.log(x)` | `print(x)` |

**No `await` anywhere in this workshop.** Python can do async; we don't need it.

---

## The bits you'll actually use here

### f-strings
```python
name, count = "Ada", 3
print(f"{name} has {count} notes")        # Ada has 3 notes
print(f"{3.14159:.2f}")                   # 3.14
print(f"{1234567:,}")                     # 1,234,567
print(f"{name:12}|")                      # Ada         |   (pad to width 12)
```

### Lists
```python
items = ["a", "b", "c"]
items[0]          # "a"
items[-1]         # "c"          last
items[:2]         # ["a", "b"]   first two
len(items)        # 3
items.append("d")
sorted(items)
for i, x in enumerate(items, start=1):    # 1 a / 2 b / 3 c
    print(i, x)
```

### Dictionaries
```python
d = {"name": "Ada", "score": 9}
d["name"]                 # "Ada"
d.get("missing", 0)       # 0     — safe, no crash
d["new"] = 5
d.keys() / d.values() / d.items()
for key, value in d.items():
    print(key, value)
```

### Comprehensions
```python
[x * 2 for x in nums]                       # map
[x for x in nums if x > 3]                  # filter
[x * 2 for x in nums if x > 3]              # both
{d["file"] for d in docs}                   # a SET — removes duplicates
", ".join(d["file"] for d in docs)          # join without building a list first
```

### Functions
```python
def answer(question, k=4):
    """This text is a docstring — the function explaining itself."""
    return f"{question} ({k} chunks)"

answer("hello")             # k defaults to 4
answer("hello", k=10)       # name the argument to skip ahead
```

### Strings
```python
s = "  Hello World  "
s.strip()              # "Hello World"
s.lower()              # "  hello world  "
s.replace("o", "0")
s.split()              # ["Hello", "World"]
s.startswith("  H")    # True
"cat" in s             # False    — substring test
```

### Files and paths
```python
from pathlib import Path

Path("notes/a.md").read_text(encoding="utf-8")     # always pass encoding
Path("out.txt").write_text("hi", encoding="utf-8")
Path("notes") / "a.md"                             # joins correctly on every OS
sorted(Path("notes").glob("**/*.md"))              # every .md, sub-folders too
Path("notes").exists()
```

### Multiple return values
```python
def answer_question(q):
    return "the answer", ["a.md", "b.md"]

text, sources = answer_question("hi")      # unpacked into two variables
```

### Imports
```python
import config                          # our own file, config.py
from pathlib import Path               # one name out of a module
from langchain_chroma import Chroma
```

### The `__main__` line
```python
if __name__ == "__main__":
    main()
```
"Only run this if this file was started directly." Lets other files import yours
without accidentally launching it.

---

## Reading an error

**Read the LAST line first.** Everything above it is just the trail of how it got there.

| Error | Usually means |
|---|---|
| `NameError: name 'x' is not defined` | You skipped a cell, or restarted the kernel. Run all cells from the top. |
| `ModuleNotFoundError` | Wrong kernel, or venv not activated. |
| `IndentationError` | Your spacing is inconsistent. Never mix tabs and spaces. |
| `KeyError: 'x'` | That key isn't in the dictionary. Use `.get("x", default)`. |
| `IndexError` | The list is shorter than you think. Check `len()`. |
| `TypeError: ... NoneType` | Something returned `None` — often a function with no `return`. |
| `FileNotFoundError` | Wrong folder. Check with `Path("x").exists()`. |

---

## Notebook survival

- **Shift + Enter** runs a cell.
- Cells share memory. **Run them in order, from the top.**
- A variable alone on the last line displays it — no `print` needed. Use this constantly
  to look inside things.
- When things stop making sense: **Restart kernel, then Run All.** Fixes a surprising amount.
- Every new notebook needs its kernel picked: top right → Select Kernel → Python
  Environments → the `.venv` one.

## Terminal survival

```bash
cd study_buddy                     # go into a folder
ls            (Windows: dir)       # list files
source .venv/bin/activate          # Mac/Linux — activate the venv
.venv\Scripts\activate             # Windows
python ingest.py                   # run a file
```
Your prompt shows `(.venv)` when the environment is active. **Activate it in every new
terminal** — "it worked yesterday" is almost always this.
