# Terminal AI Assistant (Ollama)

A simple command-line AI assistant that runs locally using [Ollama](https://ollama.com).
No API key is required — everything runs on your machine.

## Features

- Loads settings (`OLLAMA_MODEL`, `OLLAMA_HOST`) from a `.env` file
- Uses a system prompt that keeps answers simple and honest
- Interactive question/answer loop with an `exit`/`quit` command
- Prints the answer, model name, and token usage for each reply
- Startup and runtime error handling for unreachable Ollama, missing models, etc.

## Prerequisites

1. **Python 3.9+** installed.
2. **Ollama** installed and running:
   - Download from https://ollama.com/download
   - Start the Ollama app / service.
3. **Pull the model** used by this project:
   ```bash
   ollama pull llama3.2:1b
   ```

## Setup

```bash
# 1. Create a virtual environment (optional but recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Create your local settings file
cp .env.example .env   # macOS/Linux
# On Windows (PowerShell):
Copy-Item .env.example .env
```

Edit `.env` if you want to change the model or host (defaults shown below):

```env
OLLAMA_MODEL=llama3.2:1b
OLLAMA_HOST=http://localhost:11434
```

`.env` is git-ignored so your personal configuration is never committed.

## Run

```bash
python main.py
```

Example session:

```
Terminal AI Assistant
Model: llama3.2:1b
Host:  http://localhost:11434
Type your question and press Enter. Type 'exit' or 'quit' to leave.

You: What is Python?
Assistant: Python is a programming language used for games, websites,
data analysis, automation, and more. It is easy to read and free to use.

Model: llama3.2:1b
Tokens: prompt=42, completion=48, total=90

You: exit
Goodbye!
```

## Switching models

1. Pull the new model:
   ```bash
   ollama pull <model-name>
   ```
2. Update `OLLAMA_MODEL` in your `.env` file (or set the env var).
3. Run `python main.py` again.

You can list installed models with `ollama list`.

## Troubleshooting

- **"Ollama is not running or unreachable"** — Start the Ollama app/service. Verify with `ollama list`. Check that `OLLAMA_HOST` matches where Ollama listens (default `http://localhost:11434`).
- **"Model ... is not installed (HTTP 404)"** — Run `ollama pull <model>` and confirm the name matches `ollama list`.
- **Slow first response** — The first request loads the model into memory; later replies are faster.
- **Wrong Python / missing modules** — Ensure you activated the virtual environment and ran `pip install -r requirements.txt`.
- **Port in use / custom host** — Set `OLLAMA_HOST` to the address Ollama is bound to.

## Project files

- `main.py` — application entry point
- `.env` — your local settings (git-ignored)
- `.env.example` — template for `.env`
- `requirements.txt` — Python dependencies
- `.gitignore` — ignored files
- `README.md` — this file
## Run online with GitHub Codespaces

You can test this project without installing anything locally:

1. Open the repository on GitHub and click **Code → Codespaces → Create codespace on main**.
2. Wait for the container to build (it installs Ollama and pulls `llama3.2:1b`).
3. In the terminal run:
   ```bash
   python main.py
   ```

The devcontainer (`.devcontainer/`) handles installing Ollama and the model automatically.

