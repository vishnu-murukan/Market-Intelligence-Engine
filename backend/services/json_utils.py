import re
import json
from typing import Any


def safe_json_parse(text: str) -> Any:
    """
    Robustly parse JSON from Gemini responses.
    Handles:
      - Markdown code fences (```json ... ```)
      - Raw control characters inside strings (\\n \\t \\r) that break json.loads
      - Leading/trailing whitespace
    """
    text = text.strip()

    # Strip markdown fences
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    text = text.strip()

    # First attempt: parse as-is (fastest path)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Second attempt: replace literal control characters INSIDE JSON strings
    # Control chars (0x00-0x1f except \t \n \r) inside strings break the parser
    # Replace \n \r \t that appear literally (not as escape sequences) inside strings
    def sanitize_string_values(s: str) -> str:
        # Replace raw newlines/tabs/carriage returns inside string values with a space
        # We do this carefully: only between quotes
        result = []
        in_string = False
        escape_next = False
        for ch in s:
            if escape_next:
                result.append(ch)
                escape_next = False
                continue
            if ch == '\\' and in_string:
                result.append(ch)
                escape_next = True
                continue
            if ch == '"':
                in_string = not in_string
                result.append(ch)
                continue
            if in_string and ch in ('\n', '\r', '\t'):
                result.append(' ')  # replace with space to keep valid JSON
                continue
            if in_string and ord(ch) < 0x20:
                continue  # drop other control chars
            result.append(ch)
        return ''.join(result)

    try:
        return json.loads(sanitize_string_values(text))
    except json.JSONDecodeError:
        pass

    # Third attempt: extract first JSON array or object with regex
    match = re.search(r'(\[.*\]|\{.*\})', text, re.DOTALL)
    if match:
        try:
            return json.loads(sanitize_string_values(match.group(1)))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse JSON from response: {text[:200]}")