# Senpai Bot harness

This is the technical harness only: an Ollama-backed CLI chat loop, no
persona or curriculum behavior authored by the harness itself. You write
that in `persona_system_prompt.md`.

## What it does

- Reads `README.md`, `rules.md`, and `SECURITY.md` in full and injects them
  verbatim into the system prompt at the start of every fresh session
  (`senpai_bot/context.py`), so the model actually has the real current
  contract text rather than a paraphrase.
- Reads `overall_grades.md` at session start if it exists.
- Gives the model three tools it can call mid-conversation, sandboxed to
  this repository folder (`senpai_bot/tools.py`):
  - `read_file(path)` -- inspect any current file (stage grades, learner
    code, challenge instructions, etc.)
  - `list_dir(path)` -- see what exists
  - `write_file(path, content)` -- create/update tutor-owned training-state
    files. Refuses to touch `README.md`, `rules.md`, `SECURITY.md`, or
    `gitignore.txt`.
- Persists the conversation to `senpai_bot/state.json` (gitignored) so
  closing the terminal doesn't lose the session. `/reset` clears it.
- Talks to Ollama's local `/api/chat` REST endpoint over plain
  `urllib` -- no third-party dependencies, nothing to `pip install`.

## What it deliberately does not do

It does not embed any persona, tone, reward/punishment logic, or grading
behavior of its own -- that all comes from whatever you put in
`persona_system_prompt.md` plus the contract files, and is entirely up to
the model you run it against.

## Setup

1. Install and run [Ollama](https://ollama.com) yourself, then pull a model
   that supports tool calling, e.g.:

   ```bash
   ollama pull llama3.1
   ```

2. Copy the env template and fill in the model name:

   ```bash
   cp senpai_bot/.env.example senpai_bot/.env
   ```

   Edit `senpai_bot/.env` and set `OLLAMA_MODEL=llama3.1` (or whichever
   model you pulled).

3. Write your system prompt / persona content into
   `persona_system_prompt.md`.

4. Run it:

   ```bash
   python main.py
   ```

## Notes

- If the configured model doesn't support Ollama tool calling, the bot
  still runs as a plain chat client -- it just can't call `read_file` /
  `write_file` / `list_dir` mid-session, so it will only see the contract
  text injected at session start plus whatever you paste into the chat.
- Tool calls are logged to stderr as they happen (`[tool call] ...`) so you
  can see what the model actually read or wrote.
- `senpai_bot/.env` and `senpai_bot/state.json` are already in
  `gitignore.txt`.
