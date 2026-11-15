"""Locale- and culture-scoped symbol registers; no cross-locale fallback."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class SymbolRegister:
    language: str
    cultural_context: str
    version: str
    colors: dict = field(default_factory=dict)
    lights: dict = field(default_factory=dict)
    thoughts: dict = field(default_factory=dict)
    symbols: dict = field(default_factory=dict)


_REGISTERS = {}


def register_symbol_context(register: SymbolRegister):
    if not register.language or not register.cultural_context:
        raise ValueError("language and cultural_context are required")
    key = (register.language.lower(), register.cultural_context.casefold())
    if key in _REGISTERS:
        raise ValueError(f"symbol register already exists for {key}; version it explicitly")
    _REGISTERS[key] = register
    return register


def get_symbol_register(language: str, cultural_context: str):
    """Return only an exact locale/context match; never borrow another culture's map."""
    if not language or not cultural_context:
        raise ValueError("language and cultural_context are required")
    key = (language.lower(), cultural_context.casefold())
    try:
        return _REGISTERS[key]
    except KeyError as exc:
        raise LookupError(
            f"no symbol register for language={language!r}, cultural_context={cultural_context!r}"
        ) from exc
