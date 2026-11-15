import hashlib
import json
from typing import Any

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_value(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))

def verify_sha256(data: bytes, expected: str) -> bool:
    return sha256_bytes(data) == expected
