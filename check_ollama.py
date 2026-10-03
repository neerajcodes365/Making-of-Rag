import sys

import requests

OLLAMA_URL = "http://localhost:11434"


def check_ollama(required_models: list[str]):
    """Exit with a clear message if Ollama isn't running or a model is missing."""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        sys.exit(
            "❌ Can't reach Ollama at http://localhost:11434.\n"
            "   Start it with `ollama serve` (or open the Ollama app) and try again."
        )

    installed = [m["name"] for m in response.json().get("models", [])]
    for model in required_models:
        # Installed names look like "mistral:latest", so match the prefix too.
        if not any(name == model or name.startswith(model + ":") for name in installed):
            sys.exit(f"❌ Ollama model '{model}' is not installed. Run: ollama pull {model}")