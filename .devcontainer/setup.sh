#!/usr/bin/env bash
set -e

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Ollama (Linux)
if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
fi

# Pull the model used by this project
ollama pull llama3.2:1b
