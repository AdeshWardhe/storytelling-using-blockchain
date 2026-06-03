import hashlib
import json
from datetime import datetime

def now_iso():
    """
    Return current UTC time in ISO format with 'Z' suffix.
    Example: '2025-12-09T12:34:56.789012Z'
    """
    return datetime.utcnow().isoformat() + "Z"

def sha256(s: str) -> str:
    """
    Return the hex SHA256 digest of the input string.
    Input: a Python string
    Output: 64-character hex string
    """
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def compute_hash(block: dict) -> str:
    canonical = {
        'index': block.get('index'),
        'author': block.get('author'),
        'text': block.get('text'),
        'timestamp': block.get('timestamp'),
        'prev_hash': block.get('prev_hash')
    }
    block_string = json.dumps(canonical, sort_keys=True)
    return sha256(block_string)