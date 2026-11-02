"""Simple terminal AI assistant powered by a local Ollama model."""

import os
import sys

from dotenv import load_dotenv
import ollama
from ollama import Client, ResponseError

# Load settings from .env (if present), falling back to defaults.
load_dotenv()

DEFAULT_MODEL = "llama3.2:1b"
DEFAULT_HOST = "http://localhost:11434"

MODEL = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
HOST = os.getenv("OLLAMA_HOST", DEFAULT_HOST).strip() or DEFAULT_HOST

SYSTEM_PROMPT = (
    "You are a helpful, concise terminal assistant. "
    "Explain concepts simply, in plain language, and avoid unnecessary jargon. "
    "If you are not sure about a fact, say so honestly instead of making one up. "
    "Keep answers focused and practical."
)

EXIT_COMMANDS = {"exit", "quit"}


def installed_model_names(client: Client) -> set:
    """Return the set of model names reported by the Ollama server."""
    response = client.list()
    names = set()
    for model in getattr(response, "models", []) or []:
        name = getattr(model, "model", None) or getattr(model, "name", None)
        if name:
            names.add(name)
    return names


def model_is_installed(client: Client, model: str) -> bool:
    names = installed_model_names(client)
    if model in names:
        return True
    # Allow matching by base name when no tag was requested.
    base = model.split(":", 1)[0]
    return any(n.split(":", 1)[0] == base and ":" not in model for n in names)


def startup_check(client: Client, model: str) -> bool:
    """Verify the server is reachable and the model is installed."""
    try:
        client.list()
    except ConnectionError:
        print(
            f"Error: Ollama is not running or unreachable at {HOST}.\n"
            "Please start Ollama and try again. "
            "Download it from https://ollama.com/download if needed."
        )
        return False
    except Exception as exc:  # unexpected
        print(f"Error: Unexpected problem contacting Ollama: {exc}")
        return False

    try:
        if not model_is_installed(client, model):
            print(
                f"Error: Model '{model}' is not installed.\n"
                f"Run: ollama pull {model}"
            )
            return False
    except ResponseError as exc:
        if exc.status_code == 404:
            print(
                f"Error: Model '{model}' is not installed (HTTP 404).\n"
                f"Run: ollama pull {model}"
            )
        else:
            print(f"Ollama error while checking models: {exc}")
        return False
    except Exception as exc:
        print(f"Error: Unexpected problem checking models: {exc}")
        return False

    return True


def print_usage(response) -> None:
    prompt_tokens = getattr(response, "prompt_eval_count", None)
    completion_tokens = getattr(response, "eval_count", None)
    if prompt_tokens is None and completion_tokens is None:
        return
    parts = []
    if prompt_tokens is not None:
        parts.append(f"prompt={prompt_tokens}")
    if completion_tokens is not None:
        parts.append(f"completion={completion_tokens}")
    if prompt_tokens is not None and completion_tokens is not None:
        parts.append(f"total={prompt_tokens + completion_tokens}")
    print("Tokens: " + ", ".join(parts))


def main() -> int:
    client = Client(host=HOST)

    print(f"Terminal AI Assistant")
    print(f"Model: {MODEL}")
    print(f"Host:  {HOST}")
    print("Type your question and press Enter. Type 'exit' or 'quit' to leave.\n")

    if not startup_check(client, MODEL):
        return 1

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        user_input = user_input.strip()
        if not user_input:
            continue
        if user_input.lower() in EXIT_COMMANDS:
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat(model=MODEL, messages=messages)
        except ConnectionError:
            print(
                "Error: Ollama is not running or unreachable. "
                "Please start Ollama and try again."
            )
            # Remove the unanswered user turn so history stays consistent.
            messages.pop()
            continue
        except ResponseError as exc:
            if exc.status_code == 404:
                print(
                    f"Error: Model '{MODEL}' is not installed (HTTP 404).\n"
                    f"Run: ollama pull {MODEL}"
                )
            else:
                print(f"Ollama error: {exc}")
            messages.pop()
            continue
        except Exception as exc:
            print(f"Unexpected error: {exc}")
            messages.pop()
            continue

        answer = ""
        try:
            answer = response.message.content or ""
        except Exception:
            answer = str(response)

        print(f"Assistant: {answer}")
        print(f"Model: {getattr(response, 'model', None) or MODEL}")
        print_usage(response)
        print()

        messages.append({"role": "assistant", "content": answer})

    return 0


if __name__ == "__main__":
    sys.exit(main())
