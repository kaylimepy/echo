from functools import lru_cache
from typing import Any, Dict

import yaml

CONFIG_PATH = 'config.yml'


def read(*keys: str) -> Any:
    value = __config()

    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return None

    return value


@lru_cache(maxsize=None)
def __config() -> Dict[str, Any]:
    with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
    