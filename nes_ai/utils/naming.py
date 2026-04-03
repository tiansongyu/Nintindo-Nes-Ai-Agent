import importlib
import re


def normalize_identifier(value: str) -> str:
    text = value.strip().lower()
    if text.isdigit():
        return text
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"[^a-z0-9-]+", "", text)


def parse_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise ValueError(f"Cannot parse boolean value: {value}")


def load_attr(path: str):
    module_name, attr_name = path.split(":", 1)
    module = importlib.import_module(module_name)
    return getattr(module, attr_name)

