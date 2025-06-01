"""Utility functions for task management."""

import urllib.parse


def decode_value(value: str) -> str:
    """Decode a URL-encoded value."""
    return urllib.parse.unquote(value)


def extract_form_data(data: bytes) -> dict:
    """Extract form data from bytes."""
    decoded_data = data.decode("utf-8")
    items = decoded_data.split("&")
    return {
        item.split("=")[0]: decode_value(item.split("=")[1])
        for item in items
        if "=" in item
    }
