#!/usr/bin/env bash
# Start the Ollama server in the background if it is not already running.
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
  nohup ollama serve > /tmp/ollama.log 2>&1 &
  # Wait for the server to become ready
  for i in $(seq 1 30); do
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done
fi
