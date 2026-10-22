"""One-call key test:  does the Anthropic key in .env work?

Run it from the repository root, after copying `.env.example` to `.env` and pasting your key:

    python scripts/check_key.py

It sends one tiny request to the Claude API and prints a short result.  It never prints the key.
Exit code:  0 = the key works; 1 = no key found; 2 = the API rejected the call; 3 = no connection.

The script uses only the Python standard library, so it needs no installed packages.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
KEY_NAME = "ANTHROPIC_API_KEY"
# The plain API model id.  LiteLLM writes the same model as "anthropic/claude-sonnet-5-5".
MODEL = "claude-sonnet-5-5"
DEFAULT_ENV = Path(__file__).resolve().parent.parent / ".env"

HINTS = {
    401: "The key was rejected.  Check .env for extra spaces or quotes.  If it still fails, ask LaNice for a new one-time link.",
    403: "The key is not allowed to use this model.  Ask LaNice.",
    404: f"The model id was not found.  Use {MODEL} here (anthropic/{MODEL} in LiteLLM).",
    429: "Rate limited.  Wait a minute and run it again.",
}


def read_env_key(path, name=KEY_NAME):
    """Return the value of `name` in a simple KEY=value file, or None."""
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        key, _, value = line.partition("=")
        if key.strip() == name:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            return value or None
    return None


def build_request(key, model=MODEL):
    body = {"model": model, "max_tokens": 32,
            "messages": [{"role": "user", "content": "Say hello in five words."}]}
    return urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={"x-api-key": key, "anthropic-version": API_VERSION, "content-type": "application/json"},
    )


def redact(text, key):
    return text.replace(key, "[key]") if key else text


def error_detail(error, key):
    """The API's own error message, with the key removed in case it is echoed."""
    try:
        detail = json.loads(error.read().decode("utf-8")).get("error", {})
        return redact(f"{detail.get('type', 'error')}: {detail.get('message', '')}".strip(), key)
    except (ValueError, OSError, AttributeError):
        return ""


def main(argv=None, opener=urllib.request.urlopen, environ=None):
    parser = argparse.ArgumentParser(description="Test the Anthropic key in .env with one tiny call.")
    parser.add_argument("--env", default=str(DEFAULT_ENV), help="path to the .env file (default: the repository .env)")
    parser.add_argument("--model", default=MODEL, help=f"model id (default: {MODEL})")
    args = parser.parse_args(argv)
    environ = os.environ if environ is None else environ

    key = read_env_key(args.env) or environ.get(KEY_NAME)
    if not key:
        print(f"No {KEY_NAME} found.  Copy .env.example to .env and paste your key after {KEY_NAME}=.")
        return 1

    try:
        with opener(build_request(key, args.model), timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
            status = response.status
    except urllib.error.HTTPError as error:
        print(f"Rejected:  HTTP {error.code}.  {HINTS.get(error.code, '')}".rstrip())
        detail = error_detail(error, key)
        if detail:
            print(detail)
        return 2
    except (urllib.error.URLError, OSError) as error:
        print(f"Could not reach the API:  {redact(str(error), key)}")
        return 3

    text = ""
    for block in payload.get("content", []):
        if block.get("type") == "text":
            text = block.get("text", "").strip()
            break
    print(f"OK:  HTTP {status} from {args.model}." + (f"  Reply:  {redact(text, key)}" if text else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
