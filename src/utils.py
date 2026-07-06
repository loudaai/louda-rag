import textwrap
import re


def truncate_text(text, max_chars=300):
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "..."


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def format_source_name(file_path):
    return file_path.split("\\")[-1].split("/")[-1]


def count_tokens(text):
    return len(text.split())
